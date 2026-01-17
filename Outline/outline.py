import yaml
import os
import time
import re
import markdown
import csv
import io

# Preset mappings for human-friendly names
PRESETS = {
    "phone": "(max-width: 599px)",
    "tablet": "(min-width: 600px) and (max-width: 1023px)",
    "laptop": "(min-width: 1024px)",
    "desktop": "(min-width: 1200px)",
    "dark": "(prefers-color-scheme: dark)",
    "light": "(prefers-color-scheme: light)",
    "portrait": "(orientation: portrait)",
    "landscape": "(orientation: landscape)"
}

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
    """Converts CSV/TSV string into an HTML table."""
    delimiter = '\t' if '\t' in data_str else ','
    html = ["<table style='width:100%; border-collapse: collapse;'>"]
    try:
        reader = csv.reader(io.StringIO(data_str.strip()), delimiter=delimiter)
        rows = list(reader)
        if not rows: return ""
        html.append("<thead><tr>")
        for cell in rows[0]:
            html.append(f"<th style='border: 1px solid #ddd; padding: 8px; text-align: left; background: #f4f4f4;'>{cell.strip()}</th>")
        html.append("</tr></thead><tbody>")
        for row in rows[1:]:
            html.append("<tr>")
            for cell in row:
                html.append(f"<td style='border: 1px solid #ddd; padding: 8px;'>{cell.strip()}</td>")
            html.append("</tr>")
        html.append("</tbody></table>")
    except Exception as e:
        return f"<p>Error rendering table: {e}</p>"
    return "".join(html)

def generate_css_for_library(library, typography=None):
    """Generates CSS block from a theme's library and typography."""
    rules = []
    # Process Typography (Global tag styles)
    if typography:
        for tag, styles in typography.items():
            if isinstance(styles, dict):
                css_block = f"{tag} {{\n"
                for prop, val in styles.items():
                    css_block += f"  {prop.replace(' ', '-')}: {clean_value(val)};\n"
                css_block += "}"
                rules.append(css_block)
    
    # Process Library Elements
    if library:
        elements = library.get('elements', {})
        for tag, styles in elements.items():
            if isinstance(styles, dict):
                css_block = f"{tag} {{\n"
                for prop, val in styles.items():
                    css_block += f"  {prop.replace(' ', '-')}: {clean_value(val)};\n"
                css_block += "}"
                rules.append(css_block)
    return rules

def process_elements(elements, css_rules_list, global_library=None):
    html_buffer = ""
    if not isinstance(elements, list): return str(elements)
    global_library = global_library or {}

    for i, entry in enumerate(elements):
        tag_raw = list(entry.keys())[0]
        value = entry[tag_raw]
        if tag_raw.lower() in ['theme', 'themes']: continue

        tag = "section" if tag_raw.lower() == "home page" else tag_raw.lower()
        el_id = f"otl-{tag}-{i}-{id(entry) % 1000}" 
        content_html = ""
        style_data = {}

        if tag in global_library:
            style_data.update(global_library[tag])

        if tag == 'table' and isinstance(value, str):
            content_html = render_table(value)
        elif isinstance(value, str):
            content_html = render_markdown(value)
        elif isinstance(value, list):
            content_html = process_elements(value, css_rules_list, global_library)
        elif isinstance(value, dict):
            local_library = global_library
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
        with open("template.html", "r", encoding="utf-8") as f: template_str = f.read()
        with open("site.otl", "r", encoding="utf-8") as f: data = yaml.safe_load(f) or []
        
        css_rules = []
        global_library = {}
        themes_data = None

        # 1. Extraction of Default Theme and Multi-Themes
        for item in data:
            key = list(item.keys())[0].lower()
            if key == 'themes':
                themes_data = item[list(item.keys())[0]]
            elif isinstance(item[list(item.keys())[0]], dict) and 'theme' in item[list(item.keys())[0]]:
                theme_block = item[list(item.keys())[0]]['theme']
                global_library.update(theme_block.get('library', {}).get('elements', {}))
                # Generate default global styles
                css_rules.extend(generate_css_for_library(theme_block.get('library', {}), theme_block.get('typography')))

        # 2. Process Responsive Themes (Brightness first, then Device Size for priority)
        if themes_data:
            categories = ["brightness", "device size", "orientation"]
            for cat in categories:
                cat_data = None
                for k, v in themes_data.items():
                    if k.lower() == cat: cat_data = v
                
                if cat_data:
                    for theme_wrapper in cat_data:
                        name = list(theme_wrapper.keys())[0]
                        content = theme_wrapper[name]
                        
                        # Determine Media Query
                        query = ""
                        clean_name = name.split('(')[0].strip().lower()
                        if '(' in name and ')' in name:
                            query = name[name.find("(")+1:name.find(")")]
                        elif clean_name in PRESETS:
                            query = PRESETS[clean_name]
                        
                        if query:
                            sub_rules = generate_css_for_library(content.get('library', {}), content.get('typography'))
                            if sub_rules:
                                css_rules.append(f"@media {query} {{\n" + "\n".join(sub_rules) + "\n}")

        body_content = process_elements(data, css_rules, global_library)
        output = template_str.replace("{{ CSS }}", "\n".join(css_rules)).replace("{{ CONTENT }}", body_content)
        with open("index.html", "w", encoding="utf-8") as f: f.write(output)
        print("Done! Multi-theme and responsive support live.")
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