import yaml
import os
import time

def process_elements(elements, css_rules_list):
    """This function 'recurses' - it calls itself to handle nested tags."""
    html_buffer = ""
    
    for i, entry in enumerate(elements):
        tag = list(entry.keys())[0]
        value = entry[tag]
        # Unique ID for this specific element's style
        el_id = f"otl-{tag}-{i}-{id(entry) % 1000}" 
        
        content_html = ""
        style_data = {}

        if isinstance(value, list):
            # Direct nesting: - div: [ - h1: hey ]
            content_html = process_elements(value, css_rules_list)
        elif isinstance(value, dict):
            # Complex nesting: - div: { children: [...], style: {...} }
            style_data = value.get('style', {})
            children = value.get('children', [])
            content_html = process_elements(children, css_rules_list) if children else value.get('content', '')
        else:
            # Simple text: - h1: hey
            content_html = str(value)

        if style_data:
            css_rule = f".{el_id} {{\n"
            for prop, val in style_data.items():
                css_rule += f"  {prop.replace(' ', '-')}: {val};\n"
            css_rule += "}"
            css_rules_list.append(css_rule)
            html_buffer += f"<{tag} class='{el_id}'>{content_html}</{tag}>\n"
        else:
            html_buffer += f"<{tag}>{content_html}</{tag}>\n"
            
    return html_buffer

def compile_outline():
    try:
        with open("template.html", "r") as f: template_str = f.read()
        with open("site.otl", "r") as f: data = yaml.safe_load(f)
        
        css_rules = []
        # We start the recursion here
        body_content = process_elements(data or [], css_rules)
        
        output = template_str.replace("{{ CSS }}", "\n".join(css_rules))
        output = output.replace("{{ CONTENT }}", body_content)

        with open("index.html", "w") as f: f.write(output)
        print("Done! Site updated.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Outline is watching for changes... (Press Ctrl+C to stop)")
    last_mtime = 0
    while True:
        try:
            mtime = os.path.getmtime("site.otl")
            if mtime != last_mtime:
                compile_outline()
                last_mtime = mtime
        except: pass
        time.sleep(1)