# 🚀 Outline Project Commit Convention

We use the **Conventional Commits** standard. This makes the history readable and allows for automated changelog generation.

> **IMPORTANT NOTE:**
> **💡 Use Beginner-Friendly Language:** Write descriptions so that someone **without a coding background** can understand. Use "taught the computer to read emojis" instead of "implemented UTF-8 encoding support."

## 1. Commit Message Format
Each message consists of a header, a body, and a footer.

```text
✨ <Type>: <Short Description>
- <Detail 1>
- <Detail 2>

<Negative Header Category>:
- <Negative Detail 1>

📅 To Do:
- <Next Step 1>
```

## 2. Category Types
Select the most appropriate header for each section based on the nature of the update.

### Positive Categories (Header Icons)
Choose one for your main header:

* ✨ **Feat**: New functionality.
* 🐛 **Fix**: Bug resolutions.
* 📝 **Docs**: Documentation only.
* 🎨 **Style**: Visual/CSS changes.
* ♻️ **Refactor**: Code cleanup.
* ⚡ **Perf**: Speed improvements.
* 🔧 **Chore**: Maintenance/Deps.

### Negative Categories (Footer Options)
Use one of these headers to describe issues, limits, or risks:

* ⚠️ **Negative**: General limitations or drawbacks.
* 🚧 **Limits**: Technical constraints or unfinished parts.
* 🛑 **Errors**: Known bugs or crashes remaining.
* 💥 **Breaking**: Changes that break backward compatibility.
* 🚩 **Issues**: Logic flaws or unexpected behavior.

## 3. Scopes (<scope>)
Scopes help identify which part of the project changed. Common scopes for Outline:

* **core**: The main `outline.py` logic.
* **markdown**: The markdown rendering engine.
* **theme**: Dictionary and library logic.
* **tutorial**: The documentation files.
* **cli**: Command line interactions or watcher logic.

## 4. Examples

### Adding a new feature with limitations:
```text
✨ Feat: Implemented Design System with Library & Dictionary
- Design Tokens: Introduced a dictionary section for colors using YAML anchors.
- Component Library: Elements like button now have default styles.

🚧 Limits:
- Hover states on buttons are currently flickering in Safari.
- No "shortcut" names for complex styles yet.

📅 To Do:
- Create reusable "Components" (save a card style and reuse it by name).
```

### Fixing a bug with a breaking change:
```text
🐛 Fix: Support for nested layouts and grouped content
- Boxes inside Boxes: You can now place elements inside one another.

💥 Breaking:
- The 'children' tag is deprecated; use 'content'.
- Images still require manual web links.

📅 To Do:
- Add automatic image handling.
```

## 💡 Pro Tips
* **Imperative Mood**: Always start the description with a verb like "add", "fix", or "change" (e.g., `Feat: add` instead of `Feat: added`).
* **Short Headers**: Keep the first line under 50 characters if possible.
* **Breaking Changes**: If a change breaks previous .otl files, note it in the breaking section and add `!` after the type: `Feat!: Change dictionary syntax`.
        `