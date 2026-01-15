import yaml
import os
import time

def compile_outline():
    # 1. Load the Template
    try:
        with open("template.html", "r") as f:
            template = f.read()
    except FileNotFoundError:
        print("Error: template.html not found!")
        return

    # 2. Load the .otl Content
    try:
        with open("site.otl", "r") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"YAML Error: {e}")
        return

    html_elements = []
    css_rules = []

    # 3. Process tags
    for i, entry in enumerate(data or []):
        tag = list(entry.keys())[0]
        value = entry[tag]
        class_name = f"el-{i}"
        
        if isinstance(value, str):
            html_elements.append(f"<{tag}>{value}</{tag}>")
        elif isinstance(value, dict):
            content = value.get('content', '')
            style = value.get('style', {})
            html_elements.append(f"<{tag} class='{class_name}'>{content}</{tag}>")
            
            css_rule = f".{class_name} {{\n"
            for prop, val in style.items():
                css_rule += f"  {prop.replace(' ', '-')}: {val};\n"
            css_rule += "}"
            css_rules.append(css_rule)

    # 4. Inject into Template
    final_output = template.replace("{{ CSS }}", "\n".join(css_rules))
    final_output = final_output.replace("{{ CONTENT }}", "\n        ".join(html_elements))

    with open("index.html", "w") as f:
        f.write(final_output)
    print("Compiled successfully!")

if __name__ == "__main__":
    last_mtime = 0
    while True:
        try:
            current_mtime = os.path.getmtime("site.otl")
            if current_mtime != last_mtime:
                compile_outline()
                last_mtime = current_mtime
        except FileNotFoundError:
            pass
        time.sleep(1)