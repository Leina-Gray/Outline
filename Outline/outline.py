import yaml
import os
import time
import re
import markdown
import csv
import io

def clean_value(val):
    """Removes noise words like 'font', 'color', and commas."""
    if not isinstance(val, str): return val
    noise = ['font', 'color', ',']
    pattern = re.compile(r'\b(' + '|'.join(noise) + r')\b|[,]', re.IGNORECASE)
    return pattern.sub('', val).strip()

def render_markdown(text):
    """Converts markdown strings to HTML with UTF-8 support."""
    if not isinstance(text, str): return text
    return markdown.markdown(text, extensions=['extra'])

def render_table(data_str):
    """Converts CSV/TSV string into an HTML table and strips extra padding."""
    # Detect delimiter: if tab exists, use TSV, else CSV
    delimiter = '\t' if '\t' in data_str else ','
    
    html = ["<table style='width:100%; border-collapse: collapse;'>"]
    try:
        # We use skipinitialspace for CSV, but manual stripping is safer for both
        reader = csv.reader(io.StringIO(data_str.strip()), delimiter=delimiter)
        rows = list(reader)
        if not rows: return ""
        
        # Header
        html.append("<thead><tr>")
        for cell in rows[0]:
            # .strip() handles the visual alignment whitespace from the OTL
            html.append(f"<th style='border: 1px solid #ddd; padding: 8px; text-align: left; background: #f4f4f4;'>{cell.strip()}</th>")
        html.append("</tr></thead>")
        
        # Body
        html.append("<tbody>")
        for row in rows[1:]:
            html.append("<tr>")
            for cell in row:
                html.append(f"<td style='border: 1px solid #ddd; padding: 8px;'>{cell.strip()}</td>")
            html.append("</tr>")
        html.append("</tbody></table>")
    except Exception as e:
        return f"<p>Error rendering table: {e}</p>"
        
    return "".join(html)

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

        # Feature: Auto Table Rendering
        if tag == 'table' and isinstance(value, str):
            content_html = render_table(value)
        elif isinstance(value, str):
            content_html = render_markdown(value)
        elif isinstance(value, list):
            content_html = process_elements(value, css_rules_list, global_library)
        elif isinstance(value, dict):
            local_library = global_library
            if 'theme' in value:
                local_library = {**global_library, **value['theme'].get('library', {}).get('elements', {})}
            
            raw_content = value.get('content') or value.get('children')
            
            if tag == 'table' and isinstance(raw_content, str):
                 content_html = render_table(raw_content)
            elif isinstance(raw_content, list):
                content_html = process_elements(raw_content, css_rules_list, local_library)
            else:
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
        with open("template.html", "r", encoding="utf-8") as f: 
            template_str = f.read()
        with open("site.otl", "r", encoding="utf-8") as f: 
            data = yaml.safe_load(f)
        
        global_library = {}
        for item in (data or []):
            for key, val in item.items():
                if isinstance(val, dict) and 'theme' in val:
                    lib_elements = val['theme'].get('library', {}).get('elements', {})
                    global_library.update(lib_elements)

        css_rules = []
        body_content = process_elements(data or [], css_rules, global_library)
        
        output = template_str.replace("{{ CSS }}", "\n".join(css_rules)).replace("{{ CONTENT }}", body_content)
        
        with open("index.html", "w", encoding="utf-8") as f: 
            f.write(output)
        print("Done! Table support with visual alignment added.")
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