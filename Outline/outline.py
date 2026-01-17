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

# State mappings for CSS pseudo-classes
STATE_MAPPING = {
    "on-hover": ":hover",
    "on-pressed": ":active",
    "on-active": ".active",
    "on-selected": ".selected",
    "on-focus": ":focus",
    "on-disabled": ":disabled",
    "on-success": ".success",
    "on-error": ".error",
    "on-warning": ".warning",
    "on-information": ".info"
}

def clean_value(val):
    if not isinstance(val, str): return val
    noise = ['font', 'color', ',']
    pattern = re.compile(r'\b(' + '|'.join(noise) + r')\b|[,]', re.IGNORECASE)
    return pattern.sub('', val).strip()

def render_markdown(text):
    if not isinstance(text, str): return text
    return markdown.markdown(text, extensions=['extra'])

def render_table(data_str):
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

def generate_css_block(selector, styles):
    """Utility to generate a CSS string block."""
    if not styles: return ""
    css_block = f"{selector} {{\n"
    for prop, val in styles.items():
        css_block += f"  {prop.replace(' ', '-')}: {clean_value(val)};\n"
    css_block += "}"
    return css_block

def detect_list_marker(items):
    """
    Advanced detection for:
    1. Unicode symbols (◦, •, →, ✓, ❉, ●, ○, ■)
    2. Nested numbering (1.1., 1.2.)
    3. Prefixes (Slide 1., Task A.)
    4. Suffixes (1), 2), a))
    """
    if not items or not isinstance(items[0], str): return None, None
    
    first_item = items[0].strip()
    
    # Pattern 1: Alphanumeric prefix/suffix (Slide 1., 1.1., 1), (a))
    pattern_complex = r'^([A-Za-z0-9\s.()-]+[.)]\s+)'
    # Pattern 2: Pure Unicode symbols (non-alphanumeric, non-whitespace)
    pattern_unicode = r'^([^\w\s\d]\s*)'
    
    match = re.match(pattern_complex, first_item)
    if match:
        marker = match.group(1)
        return marker, lambda s: re.match(pattern_complex, s).group(1) if re.match(pattern_complex, s) else ""
        
    match = re.match(pattern_unicode, first_item)
    if match:
        marker = match.group(1)
        return marker, lambda s: re.match(pattern_unicode, s).group(1) if re.match(pattern_unicode, s) else ""
        
    return None, None

def generate_css_for_library(library, typography=None):
    rules = []
    if typography:
        for tag, styles in typography.items():
            if isinstance(styles, dict):
                rules.append(generate_css_block(tag, styles))
    
    if library:
        elements = library.get('elements', {})
        for tag, styles in elements.items():
            if isinstance(styles, dict):
                base_styles = {k:v for k,v in styles.items() if k != 'states'}
                rules.append(generate_css_block(tag, base_styles))
                
                if 'states' in styles:
                    for state_name, state_styles in styles['states'].items():
                        pseudo = STATE_MAPPING.get(state_name.lower())
                        if pseudo:
                            rules.append(generate_css_block(f"{tag}{pseudo}", state_styles))
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
        states_data = {}

        if tag in global_library:
            lib_style = global_library[tag]
            style_data.update({k:v for k,v in lib_style.items() if k != 'states'})
            if 'states' in lib_style: states_data.update(lib_style['states'])

        # Smart List Logic with Spacing Fix
        if tag == 'list' and isinstance(value, dict) and 'content' in value:
            items = value['content']
            marker_str, extractor = detect_list_marker(items)
            
            if marker_str:
                # Reset standard UL padding, use relative positioning for alignment
                style_data.update({'list-style': 'none', 'padding-left': '0'})
                list_html = []
                for idx, item_text in enumerate(items):
                    found_marker = extractor(item_text) if extractor else ""
                    clean_text = item_text[len(found_marker):] if found_marker else item_text
                    item_id = f"{el_id}-item-{idx}"
                    
                    # Calculate indent based on marker length (approx 0.7em per char)
                    indent_size = max(1.5, len(found_marker.strip()) * 0.7)
                    
                    marker_css = {
                        'content': f'"{found_marker.strip()}"',
                        'position': 'absolute',
                        'left': '0',
                        'font-weight': 'bold',
                        'color': 'inherit'
                    }
                    # Ensure the list item has room for the absolute marker
                    item_css = {
                        'position': 'relative',
                        'padding-left': f'{indent_size}em',
                        'margin-bottom': '0.5em',
                        'list-style': 'none'
                    }
                    css_rules_list.append(generate_css_block(f".{item_id}", item_css))
                    css_rules_list.append(generate_css_block(f".{item_id}::before", marker_css))
                    list_html.append(f"<li class='{item_id}'>{render_markdown(clean_text)}</li>")
                content_html = "".join(list_html)
                tag = "ul" 
            else:
                content_html = "".join([f"<li>{render_markdown(it)}</li>" for it in items])
                tag = "ul"

        elif tag == 'table' and isinstance(value, str):
            content_html = render_table(value)
        elif isinstance(value, str):
            content_html = render_markdown(value)
        elif isinstance(value, list):
            content_html = process_elements(value, css_rules_list, global_library)
        elif isinstance(value, dict):
            raw_content = value.get('content') or value.get('children')
            if tag == 'table' and isinstance(raw_content, str):
                 content_html = render_table(raw_content)
            elif isinstance(raw_content, list):
                content_html = process_elements(raw_content, css_rules_list, global_library)
            else:
                content_html = render_markdown(str(raw_content)) if raw_content else ""
            
            style_data.update(value.get('style', {}))
            states_data.update(value.get('states', {}))

        if style_data:
            css_rules_list.append(generate_css_block(f".{el_id}", style_data))
        
        for state_name, state_styles in states_data.items():
            pseudo = STATE_MAPPING.get(state_name.lower())
            if pseudo:
                css_rules_list.append(generate_css_block(f".{el_id}{pseudo}", state_styles))

        html_buffer += f"<{tag} class='{el_id}'>{content_html}</{tag}>\n"
    return html_buffer

def compile_outline():
    try:
        with open("template.html", "r", encoding="utf-8") as f: template_str = f.read()
        if not os.path.exists("site.otl"): return
        with open("site.otl", "r", encoding="utf-8") as f: data = yaml.safe_load(f) or []
        
        css_rules = []
        global_library = {}
        themes_data = None

        for item in data:
            key = list(item.keys())[0].lower()
            if key == 'themes':
                themes_data = item[list(item.keys())[0]]
            elif isinstance(item[list(item.keys())[0]], dict) and 'theme' in item[list(item.keys())[0]]:
                theme_block = item[list(item.keys())[0]]['theme']
                global_library.update(theme_block.get('library', {}).get('elements', {}))
                css_rules.extend(generate_css_for_library(theme_block.get('library', {}), theme_block.get('typography')))

        if themes_data:
            categories = ["brightness", "device size", "orientation"]
            for cat in categories:
                cat_data = themes_data.get(cat) or themes_data.get(cat.capitalize())
                if cat_data:
                    for theme_wrapper in cat_data:
                        name = list(theme_wrapper.keys())[0]
                        content = theme_wrapper[name]
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
        print("Done! Smart lists with overlap fixes compiled.")
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