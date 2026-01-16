import yaml
import os
import time
import re
import markdown # Added markdown support

def clean_value(val):
    """Removes noise words like 'font', 'color', and commas."""
    if not isinstance(val, str): return val
    noise = ['font', 'color', ',']
    pattern = re.compile(r'\b(' + '|'.join(noise) + r')\b|[,]', re.IGNORECASE)
    return pattern.sub('', val).strip()

def render_markdown(text):
    """Converts markdown strings to HTML."""
    if not isinstance(text, str): return text
    # We use 'extras' to support things like tables or task lists if needed
    return markdown.markdown(text, extensions=['extra'])

def process_elements(elements, css_rules_list, global_library=None):
    html_buffer = ""
    if not isinstance(elements, list): return str(elements)
    
    global_library = global_library or {}

    for i, entry in enumerate(elements):
        tag_raw = list(entry.keys())[0]
        value = entry[tag_raw]
        
        if tag_raw.lower() == 'theme': continue

        tag = "section" if tag_raw.lower() == "home page" else tag_raw.lower()
        el_id = f"otl-{tag}-{i}-{id(entry) % 1000}" 
        
        content_html = ""
        style_data = {}

        if tag in global_library:
            style_data.update(global_library[tag])

        if isinstance(value, str):
            # Render markdown for simple strings
            content_html = render_markdown(value)
        elif isinstance(value, list):
            content_html = process_elements(value, css_rules_list, global_library)
        elif isinstance(value, dict):
            local_library = global_library
            if 'theme' in value:
                local_library = {**global_library, **value['theme'].get('library', {}).get('elements', {})}
            
            raw_content = value.get('content') or value.get('children')
            if isinstance(raw_content, list):
                content_html = process_elements(raw_content, css_rules_list, local_library)
            else:
                # Render markdown for dictionary content
                content_html = render_markdown(str(raw_content)) if raw_content else ""
            
            style_data.update(value.get('style', {}))

        if style_data:
            main_styles = []
            for prop, val in style_data.items():
                if isinstance(val, dict):
                    nested_rule = f".{el_id} {prop} {{\n"
                    for n_prop, n_val in val.items():
                        nested_rule += f"  {n_prop.replace(' ', '-')}: {clean_value(n_val)};\n"
                    nested_rule += "}"
                    css_rules_list.append(nested_rule)
                else:
                    main_styles.append(f"  {prop.replace(' ', '-')}: {clean_value(val)};")
            
            if main_styles:
                css_rules_list.append(f".{el_id} {{\n" + "\n".join(main_styles) + "\n}")
            html_buffer += f"<{tag} class='{el_id}'>{content_html}</{tag}>\n"
        else:
            html_buffer += f"<{tag}>{content_html}</{tag}>\n"
            
    return html_buffer

def compile_outline():
    try:
        with open("template.html", "r") as f: template_str = f.read()
        with open("site.otl", "r") as f: data = yaml.safe_load(f)
        
        global_library = {}
        for item in (data or []):
            for key, val in item.items():
                if isinstance(val, dict) and 'theme' in val:
                    lib_elements = val['theme'].get('library', {}).get('elements', {})
                    global_library.update(lib_elements)

        css_rules = []
        body_content = process_elements(data or [], css_rules, global_library)
        
        output = template_str.replace("{{ CSS }}", "\n".join(css_rules)).replace("{{ CONTENT }}", body_content)
        with open("index.html", "w") as f: f.write(output)
        print("Done! Markdown rendered.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    last_mtime = 0
    while True:
        try:
            mtime = os.path.getmtime("site.otl")
            if mtime != last_mtime:
                compile_outline()
                last_mtime = mtime
        except: pass
        time.sleep(1)