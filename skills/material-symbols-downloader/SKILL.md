---
name: material-symbols-downloader
description: Search and download Material Symbols (Material Icons, Google icons, Material Design icons) from Google Fonts as SVG, Android Vector Drawable XML (ic_*.xml in res/drawable), Jetpack Compose Kotlin ImageVector, or Apple/Xcode symbol SVG. Supports outlined, rounded, and sharp styles plus fill, weight, and grade variants. Use when the user needs an icon, asks for a Material icon by name, or wants to add an icon to an Android, Compose, web, or iOS project.
---

# Material Symbols Downloader

This skill provides tools to search and download Material Symbols icons from Google Fonts for Android, web, and Apple development. Icons can be downloaded as Android Vector Drawable XML, SVG, Android Compose Kotlin, or Apple symbol SVG.

## Workflow

Follow these steps when the user needs an icon:

1. **Pick the format from the project type**, unless the user asked for one:

   | Project | Format | Where to save |
   |---------|--------|---------------|
   | Android with XML views or `painterResource` | `xml` | `app/src/main/res/drawable/` |
   | Jetpack Compose, icons as code | `compose` | a package such as `.../java/<package>/ui/icons/` |
   | Web, Flutter, React Native, design files | `svg` | the project's assets folder (`public/icons/`, `assets/icons/`, ...) |
   | iOS / macOS (SwiftUI, UIKit, AppKit) | `apple` | `Assets.xcassets/<name>.symbolset/` |

2. **Match the existing icons.** Look at icons already in the project before downloading. Reuse their style (outlined, rounded, sharp), fill, file naming (`ic_` prefix, suffixes), and folder. If the project already has the icon, use it instead of downloading a duplicate.
3. **Find the icon name.** Search by meaning, not only by exact name: `--search "trash"` finds `delete`, `--search gear` finds `settings`. Results are ordered by relevance and popularity, so the first result is usually the right choice. Use `--json` to see tags when choosing between candidates.
4. **Download** all needed icons in one run, straight into the target folder:
   `python3 scripts/download_icon.py --name home settings --style rounded --output app/src/main/res/drawable/`
   If a name is wrong, the script exits with an error and suggests similar names.
5. **Wire it up** if the user asked for it to be used in the UI: see the usage sections below. Always set a meaningful `contentDescription` / accessibility label.
6. **Report** which icons were added, in which style and format, and where.

## Overview

Material Symbols are Google's icon set (3,900+ icons), available in three styles:
- **Outlined** (default): Standard corners and stroke ends
- **Rounded**: Rounded corners and stroke ends
- **Sharp**: Square corners and stroke ends

Stroke thickness is controlled by the Weight axis, not by the style. Variable axes:
- **Fill**: `0` for outlined, `1` for filled
- **Weight**: `100`, `200`, `300`, `400`, `500`, `600`, `700`
- **Grade**: `-25`, `0`, `200`

Formats: `xml` (Android Vector Drawable), `svg`, `compose` (Kotlin `ImageVector`), and `apple` (SF Symbols template). The script uses only the Python standard library and works on Linux, macOS, and Windows.

## Script Parameters

| Parameter | Short | Description | Default |
|-----------|-------|-------------|---------|
| `--search` | `-q` | Search icons by name and tags, best matches first | - |
| `--name` | `-n` | Icon name(s) to download; with several names `--output` must be a directory | - |
| `--style` | `-s` | Icon style: `outlined`, `rounded`, `sharp` | `outlined` |
| `--size` | `-sz` | Size in px: `20`, `24`, `40`, `48` (not used by `apple`) | `24` |
| `--format` | `-f` | Output format: `xml`, `svg`, `compose`, `apple` | `xml` |
| `--fill` | - | Fill axis: `0` or `1` | `0` |
| `--weight` | - | Weight axis: `100`-`700` in steps of 100 (not used by `apple`) | `400` |
| `--grade` | - | Grade axis: `-25`, `0`, `200` | `0` |
| `--output` | `-o` | Output file or directory; a wrong extension is replaced with a warning | `./ic_<name>.<ext>` |
| `--limit` | - | Maximum number of search results | `20` |
| `--json` | - | Print search results as JSON (name, categories, tags, popularity) | `False` |
| `--package` | - | Kotlin package for `compose` (inferred from a `java/` or `kotlin/` output path) | - |
| `--refresh` | - | Force refresh metadata cache (refreshed automatically every 7 days) | `False` |

## Examples

```bash
# Search by name or meaning
python3 scripts/download_icon.py --search "arrow back"
python3 scripts/download_icon.py --search trash --json --limit 5

# Android Vector Drawable (outlined, 24px)
python3 scripts/download_icon.py --name home --output app/src/main/res/drawable/ic_home.xml

# Several rounded icons into a directory
python3 scripts/download_icon.py --name home settings delete --style rounded --output app/src/main/res/drawable/

# Filled, bold SVG
python3 scripts/download_icon.py --name favorite --format svg --fill 1 --weight 700 --output public/icons/favorite.svg

# Compose ImageVector -> .../icons/ArrowBack.kt, package com.example.app.icons, val ArrowBack
python3 scripts/download_icon.py --name arrow_back --format compose --output app/src/main/java/com/example/app/icons/

# Apple SF Symbols template
python3 scripts/download_icon.py --name toggle_on --format apple --fill 1 --output toggle_on.svg
```

## Using Downloaded Icons in Android

```kotlin
// Vector Drawable (--format xml)
Icon(
    painter = painterResource(R.drawable.ic_home),
    contentDescription = "Home"
)

// ImageVector (--format compose)
Icon(
    imageVector = ArrowBack,
    contentDescription = "Back"
)
```

```xml
<!-- XML layout -->
<ImageView
    android:layout_width="24dp"
    android:layout_height="24dp"
    android:contentDescription="@string/home"
    android:src="@drawable/ic_home" />
```

## Using Downloaded Icons in Xcode

Icons downloaded with `--format apple` are **SF Symbols custom symbol templates**, not plain images. One file contains the icon in several weights and scales, so the `--weight` option is ignored for this format and `--size` does not apply.

To add one to an iOS or macOS project:
1. Download it with the name you want to use in code, for example `--output toggle_on.svg`.
2. Add it to the asset catalog. In Xcode, drag the file into `Assets.xcassets`. Without Xcode, create the symbol set by hand:

```text
Assets.xcassets/toggle_on.symbolset/toggle_on.svg
Assets.xcassets/toggle_on.symbolset/Contents.json
```

```json
{
  "info": { "author": "xcode", "version": 1 },
  "symbols": [{ "filename": "toggle_on.svg", "idiom": "universal" }]
}
```

3. Use it like any SF Symbol. It follows the current font weight and scale:

```swift
// SwiftUI
Image("toggle_on")
    .font(.title2.weight(.semibold))
    .foregroundStyle(.tint)

// UIKit
let image = UIImage(named: "toggle_on")
```

Custom symbols require iOS 13 / macOS 11 or later. Use `--format svg` instead if you need a plain image asset.

## Icon Naming Convention

- Follow the naming already used in the project. Otherwise:
- Android drawables use the `ic_` prefix (e.g., `ic_home.xml`), with a style or size suffix when needed (`ic_home_rounded.xml`, `ic_home_48.xml`)
- Compose files and properties use PascalCase (`ArrowBack.kt`, `val ArrowBack`)
- Apple symbols and web SVGs keep the icon name (`toggle_on.svg`)

## Reference

Download URL patterns and implementation details: [references/google-fonts-urls.md](references/google-fonts-urls.md).
