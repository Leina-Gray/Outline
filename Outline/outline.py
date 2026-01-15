# import yaml
# import os
# import time

# def process_elements(elements, css_rules_list):
#     html_buffer = ""
    
#     for i, entry in enumerate(elements):
#         tag = list(entry.keys())[0]
#         value = entry[tag]
#         el_id = f"otl-{tag}-{i}-{id(entry) % 1000}" 
        
#         content_html = ""
#         style_data = {}
#         attributes = "" # New: for things like src="..."

#         if tag == "img":
#             # Image logic
#             if isinstance(value, str):
#                 attributes = f' src="{value}"'
#             elif isinstance(value, dict):
#                 src = value.get('src') or value.get('url') or ""
#                 attributes = f' src="{src}"'
#                 style_data = value.get('style', {})
#             html_buffer += f"<img class='{el_id}'{attributes}>\n"
        
#         elif isinstance(value, list):
#             content_html = process_elements(value, css_rules_list)
#         elif isinstance(value, dict):
#             style_data = value.get('style', {})
#             children = value.get('children', [])
#             content_html = process_elements(children, css_rules_list) if children else value.get('content', '')
#         else:
#             content_html = str(value)

#         # Handle normal tags (non-images)
#         if tag != "img":
#             if style_data:
#                 html_buffer += f"<{tag} class='{el_id}'>{content_html}</{tag}>\n"
#             else:
#                 html_buffer += f"<{tag}>{content_html}</{tag}>\n"

#         # Always process styles if they exist
#         if style_data:
#             css_rule = f".{el_id} {{\n"
#             for prop, val in style_data.items():
#                 css_rule += f"  {prop.replace(' ', '-')}: {val};\n"
#             css_rule += "}"
#             css_rules_list.append(css_rule)
            
#     return html_buffer

# def compile_outline():
#     try:
#         with open("template.html", "r") as f: template_str = f.read()
#         with open("site.otl", "r") as f: data = yaml.safe_load(f)
        
#         css_rules = []
#         # We start the recursion here
#         body_content = process_elements(data or [], css_rules)
        
#         output = template_str.replace("{{ CSS }}", "\n".join(css_rules))
#         output = output.replace("{{ CONTENT }}", body_content)

#         with open("index.html", "w") as f: f.write(output)
#         print("Done! Site updated.")
#     except Exception as e:
#         print(f"Error: {e}")

# if __name__ == "__main__":
#     print("Outline is watching for changes... (Press Ctrl+C to stop)")
#     last_mtime = 0
#     while True:
#         try:
#             mtime = os.path.getmtime("site.otl")
#             if mtime != last_mtime:
#                 compile_outline()
#                 last_mtime = mtime
#         except: pass
#         time.sleep(1)

import yaml
import os
import time

def process_elements(elements, css_rules_list):
    html_buffer = ""
    
    if not isinstance(elements, list):
        return str(elements)

    for i, entry in enumerate(elements):
        # Identify the tag (e.g., "H1" or "Home Page")
        tag_raw = list(entry.keys())[0]
        value = entry[tag_raw]
        
        # Convert "Home Page" to a valid HTML tag like <section>
        tag = "section" if tag_raw.lower() == "home page" else tag_raw.lower()
        el_id = f"otl-{tag}-{i}-{id(entry) % 1000}" 
        
        content_html = ""
        style_data = {}

        # TYPE 1: Simple String (- H1: Hello)
        if isinstance(value, str):
            content_html = value
            
        # TYPE 2: List of children (- Home Page: [ - H1: hey ])
        elif isinstance(value, list):
            content_html = process_elements(value, css_rules_list)
            
        # TYPE 3: Dictionary (- H2: { content: hey, style: {...} })
        elif isinstance(value, dict):
            # Check for content in 'content', 'children', or the value itself
            raw_content = value.get('content') or value.get('children')
            if isinstance(raw_content, list):
                content_html = process_elements(raw_content, css_rules_list)
            else:
                content_html = str(raw_content) if raw_content else ""
            
            style_data = value.get('style', {})

        # Generate HTML and CSS
        if style_data and isinstance(style_data, dict):
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
        body_content = process_elements(data or [], css_rules)
        output = template_str.replace("{{ CSS }}", "\n".join(css_rules)).replace("{{ CONTENT }}", body_content)
        with open("index.html", "w") as f: f.write(output)
        print("Done! Outline refreshed.")
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