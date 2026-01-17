# 📝 Welcome to Outline!

Outline is a simple language that turns your ideas into a website instantly. You write in a list format, and Outline handles the heavy lifting of building the code.

---

## 🟢 Beginner: Getting Started

### 1. The Basics
To add text, just type the tag name (like `h1` for big headers or `p` for paragraphs) followed by your text.
```yaml
- h1: This is a big title
- p: This is a normal paragraph.
```

### 2. Markdown Support
You can use standard Markdown syntax directly inside any tag for rich formatting.
```yaml
- h1: This is **Bold** and this is *Italic*
- p: |
    ### You can even do:
    - Lists
    - [Links](https://google.com)
    - `Code snippets`
```

### 3. Adding Style
Use a `style` block to change colors, sizes, and spacing.
```yaml
- h1:
    content: I am an orange title
    style:
      color: "#ff4400"
      font-size: 50px
```

### 4. Instant Tables
Create tables using simple CSV (commas) or TSV (tabs).
```yaml
- table: |
    Item,       Quantity,  Status
    Apples,     10,        ✨ Fresh
    Bananas,    5,         🍌 Ripe
```

---

## 🟡 Intermediate: Layouts & Interaction

### 5. Boxes & Nesting
Group elements together inside a "container" (like a `box` or `section`).
```yaml
- box:
    style:
      background: "#eeeeee"
      padding: 20px
    children:
      - h1: I am inside a grey box!
      - p: I am here too.
```

### 6. Flexible Writing Styles
You can write your content in different ways depending on what feels natural:
```yaml
# Styled Elements:
- H2: 
     content: hey
     style: 
            background-color: yellow

# Combined Layout (Styles + Content):
- Home Page:
     style:
          background-color: "#f0f0f0"
          padding: "20px"
     content:
          - h1: hello **world**
```

### 7. Reach-Inside Styling
Style elements inside a box directly from the parent container.
```yaml
- Home Page:
     style:
         background-color: "#f0f0f0"
         h1:
            color: "#ff4400"
     content:
          - h1: This header is red!
```

### 8. Interactive States
Define how an element looks when a user interacts with it using the `states` property.
```yaml
- button:
    content: Click here
    style: 
          background-color: blue
    states:
          on-hover:
                 background-color: darkblue
```
**Available States:** `on-hover`, `on-pressed`, `on-focus`, `on-disabled`, `on-success`, `on-error`.

---

## 🔴 Advanced: Design Systems

### 9. Global Themes & Library
Define a "Dictionary" of colors to create a "Library" where elements automatically inherit styles.
```yaml
- Home Page:
      theme:
             dictionary:
                    colors:
                          primary: &primary "#8b5cf6"
             library:
                     elements:
                          button: 
                               background: *primary
                               color: white
      content:
             - button: **Click Me**
```

### 10. Smart Adaptive Themes
Support **Multi-Themes** so your site changes based on device or "Dark Mode" settings.
```yaml
- Themes:
    Brightness:
      - Dark:
          dictionary:
            colors:
              bg: "#1a1a1a"
          library:
            elements:
              section:
                background: "#1a1a1a"
                color: "#ffffff"

    Device Size:
      - "Phone":
          typography:
            h1: { font-size: "1.8rem" }
```

---

## 💡 Quick Tips

1. **The Dash `-`**: Always start a new element with a dash and a space.
2. **Indentation**: Use **two spaces** for nesting.
3. **Markdown**: Use the pipe `|` for multi-line content.
4. **Table Alignment**: Don't worry about extra spaces in your table code; Outline cleans them up for the final site!
5. **Theme Quotes**: If a theme name has a colon or parentheses, wrap it in "quotes".
6. **Transitions**: Add `transition: 0.2s` to your style to make state changes look smooth!

Happy Building! 🚀
        `