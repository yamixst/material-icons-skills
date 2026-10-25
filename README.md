# Material Icons Skills

[![skills.sh](https://skills.sh/b/yamixst/material-icons-skills)](https://skills.sh/yamixst/material-icons-skills)

Agent skill for searching and downloading **Material Icons** (Google Material Symbols) from Google Fonts. Your AI coding agent can grab any of the 3,000+ icons and save it as an **SVG**, an **Android Vector Drawable XML** (`ic_*.xml`), a **Jetpack Compose `ImageVector`** Kotlin file, or an **Apple / Xcode symbol SVG**, ready to use in your project.

Works with Claude Code and other AI coding agents supported by the [skills CLI](https://skills.sh) (Cursor, Codex, Gemini CLI, and more).

## Why

- No more manually browsing fonts.google.com/icons, downloading, and renaming files.
- Outlined, Rounded, and Sharp styles, with custom Fill, Weight, and Grade axes.
- One Python script using only the standard library. Runs on Linux, macOS, and Windows.

## Install

```bash
npx skills@latest add yamixst/material-icons-skills
```

## Usage

Once installed, just ask your agent:

> Add a settings icon to the toolbar in my Compose screen

> Download the `home` Material icon as a rounded SVG for the website

> I need filled `favorite` and `share` vector drawables for my Android app

The agent searches the Material Symbols catalog, picks a matching icon, and saves it in the right format and location (for example, `res/drawable/ic_settings.xml` or `SettingsIcon.kt`).

## Skill

- `material-symbols-downloader`: Search and download Material Symbols in multiple output formats.

## Repository Layout

```text
skills/material-symbols-downloader/SKILL.md
skills/material-symbols-downloader/scripts/download_icon.py
```

## Supported Formats

- `xml`: Android Vector Drawable XML
- `svg`: Standard SVG asset
- `compose`: Kotlin `ImageVector`
- `apple`: Apple / Xcode symbol SVG (Google `_symbol.svg` export)

## Example Commands

The script can also be run directly, without an agent:

```bash
python3 scripts/download_icon.py --search toggle_on
python3 scripts/download_icon.py --name toggle_on --format xml --output ic_toggle_on.xml
python3 scripts/download_icon.py --name toggle_on --format svg --fill 1 --weight 700 --grade 200 --output toggle_on.svg
python3 scripts/download_icon.py --name toggle_on --format compose --fill 1 --weight 700 --grade 200 --output ToggleOn.kt
python3 scripts/download_icon.py --name toggle_on --format apple --fill 1 --grade 200 --output toggle_on_symbol.svg
```

## Notes

- Icons are fetched from the official Google Fonts Material Symbols source.
- Material Symbols are licensed by Google under the Apache License 2.0.
- Skill instructions live in `SKILL.md` for agent consumption.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
