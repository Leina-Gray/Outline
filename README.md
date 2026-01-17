# 📝 Welcome to Outline!

Outline is a simple language that turns your ideas into a website instantly. You write in a list format, and Outline handles the heavy lifting of building the code.

## 1. The Basics

To add text, just type the tag name (like `h1` for big headers or `p` for paragraphs) followed by your text.

```yaml
- h1: This is a big title
- p: This is a normal paragraph.
```

## 2. Markdown Support

You can use standard Markdown syntax directly inside any tag. This allows for rich text formatting without complex HTML.

```yaml
- h1: This is **Bold** and this is *Italic*
- p: |
    ### You can even do:
    - Lists
    - [Links](https://google.com)
    - `Code snippets`
    - > Blockquotes
```

## 3. Instant Tables (New!)

Outline now supports creating tables using simple CSV (commas) or TSV (tabs) data. You can even use spaces in your code to align columns visually so it stays organized while you work.

**CSV Example:**

```yaml
- table: |
    Item,       Quantity,  Status
    Apples,     10,        ✨ Fresh
    Bananas,    5,         🍌 Ripe
```

**TSV (Tabs) Example:**
*Great for copy-pasting from Excel or Google Sheets!*

```yaml
- table: |
    Name	Role	Department
    John Doe	Developer	Product
    Jane Smith	Designer	Creative
```

## 4. Flexible Writing

Outline is smart. You can write your content in different ways depending on what feels natural.

**Simple Text:**
```yaml
- H1: hey
```

**Styled Elements:**
```yaml
- H2: 
     content: hey
     style: 
            background-color: yellow
```

**Combined Layout (Styles + Content):**
```yaml
- Home Page:
     style:
          background-color: "#f0f0f0"
          padding: "20px"
     content:
          - h1: hello **world**
```

## 5. Adding Style

If you want to make things look fancy, you can add a `style` block. You can change colors, sizes, and spacing.

```yaml
- h1:
    content: I am a orange title
    style:
      color: "#ff4400"
      font size: 50px
```

## 6. Boxes & Nesting

You can group elements together inside a "container" (like a `box` or `section`).

```yaml
- box:
    style:
      background: "#eeeeee"
      padding: 20px
    children:
      - h1: I am inside a grey box!
      - p: I am here too.
```

## 7. Smart Reach-Inside Styling (Intermediate)

Style elements inside a box from the parent.

```yaml
- Home Page:
     style:
         background-color: "#f0f0f0"
         h1:
            color: "#ff4400"
     content:
          - h1: This header is red!
```

## 8. Global Themes & Library (Advanced)

Define a "Dictionary" of colors and sizes. This creates a "Library" where your elements automatically inherit styles.

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

## 9. Smart Adaptive Themes (New!)

Outline now supports **Multi-Themes**. This allows your website to automatically change based on the user's device or settings (like Dark Mode).

You define these in a `Themes` block. Use quotes for names with parentheses.

```yaml
- Themes:
    Brightness:
      - Dark:
          dictionary:
            colors:
              bg: "#1a1a1a"
              text: "#ffffff"
          library:
            elements:
              section:
                background: "#1a1a1a"
                color: "#ffffff"

    Device Size:
      - "Phone":
          typography:
            h1:
              font-size: "1.8rem"
      - "Tablet (min-width: 700px)":
          typography:
            h1:
              font-size: "3rem"
```

**Available Presets:**
- **Brightness:** `Light`, `Dark`
- **Device Size:** `Phone`, `Tablet`, `Laptop`, `Desktop`
- **Orientation:** `Portrait`, `Landscape`

## 💡 Quick Tips

1. **The Dash `-`**: Always start a new element with a dash and a space.
2. **Indentation**: Use **two spaces** for nesting.
3. **Markdown**: Use the pipe `|` for multi-line content.
4. **Table Alignment**: Don't worry about extra spaces in your table code; Outline cleans them up for the final site!
5. **Theme Quotes**: If a theme name has a colon or parentheses, wrap it in "quotes" to keep the computer happy.

Happy Building! 🚀
        `