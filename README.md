# 📝 Welcome to Outline!

Outline is a simple language that turns your ideas into a website instantly. You write in a list format, and Outline handles the heavy lifting of building the code.

## 1. The Basics

To add text, just type the tag name (like `h1` for big headers or `p` for paragraphs) followed by your text.

```yaml
- h1: This is a big title
- p: This is a normal paragraph.
```

## 2. Flexible Writing

Outline is smart. You can write your content in different ways depending on what feels natural. Here are the common patterns you can use:

**Simple Text:**
```yaml
- H1: hey
- P: hey
```

**Styled Elements:**
```yaml
- H2:
     content: hey
     style:
             background-color: yellow
```

**Direct Nesting (The "Quick" Way):**
```yaml
- Home Page:
       - H1: hey
       - H2:
                content: hey
                style:
                        background-color: red
```

**Labeled Content (The "Organized" Way):**
```yaml
- Home Page:
     content:
          - h1: hey
          - h2:
                  content: hey
                  style:
                          background-color: red
```

**Combined Layout (Styles + Content):**
```yaml
- Home Page:
     style:
          background-color: "#f0f0f0"
          padding: "20px"
     content:
          - h1: hey
          - h2:
                  content: hey
                  style:
                          background-color: red
```

## 3. Adding Style

If you want to make things look fancy, you can add a `style` block. You can change colors, sizes, and spacing.

```yaml
- h1:
    content: I am a orange title
    style:
      color: "#ff4400"
      font size: 50px
```

*Note: You can write `font size` with a space; Outline will fix it for you!*

## 4. Images

Adding pictures is easy. You can just provide the link, or add styles to it.

```yaml
- img: "https://example.com/photo.jpg"

- img:
    src: "https://example.com/photo.jpg"
    style:
      width: 100px
      border-radius: 50%
```

## 5. Boxes inside Boxes (Nesting)

You can group elements together inside a "container" (like a `box`, `div`, or a `section`). This is great for making cards or sidebars.

```yaml
- box:
    style:
      background: "#eeeeee"
      padding: 20px
    children:
      - h1: I am inside a grey box!
      - p: I am here too.
```

## 6. Smart Reach-Inside Styling (Intermediate)

You can style elements inside a box from the parent. This is much faster than styling every single item one by one.

```yaml
- Home Page:
     style:
         background-color: "#f0f0f0"
         padding: "40px"
         h1:
            color: "#ff4400"
            text-transform: uppercase
         h2:
            color: "blue"
     content:
          - h1: This header is red because of the parent style!
          - h2: This subheader is blue!
```

## 7. Global Themes & Library (Advanced)

You can define a "Dictionary" of colors and sizes at the top of your page. This creates a "Library" where your elements (like buttons) automatically know how to look using reusable tokens.

```yaml
- Home Page:
      theme:
             dictionary:
                    colors:
                          primary: &primary "#8b5cf6"
                          black: &black "#1a1a1a"
                    font_sizes:
                          base: &base "1rem"
             
             library:
                     elements:
                          button: 
                               background: *primary
                               color: white
                               padding: "10px 20px"

      content:
             - h1: My Themed Site
             - button: Click Me
```

## 💡 Quick Tips for Beginners

1. **The Dash `-`**: Always start a new element with a dash and a space.
2. **Indentation**: Use **two spaces** to show that something is "inside" another element.
3. **Colors**: You can use names like `red` or codes like `#000000`.
4. **Live View**: Just save your `.otl` file, and your browser will update automatically!

Happy Building! 🚀
        `;