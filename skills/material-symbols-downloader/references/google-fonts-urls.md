# Google Fonts URLs and Implementation Notes

## Notes

- The script caches metadata in a user-specific system temporary directory (`google-fonts-<username>`) to avoid permission conflicts on multi-user systems.
- Metadata is fetched from `https://fonts.google.com/metadata/icons`
- XML icons use the default Google asset URL for default axes and switch to the Google variant path `.../{icon}/{variant}/{size}px.xml` for custom `fill`, `weight`, or `grade`
- SVG icons use the default Google asset URL for default axes and switch to the Google variant path `.../{icon}/{variant}/{size}px.svg` for custom `fill`, `weight`, or `grade`
- Compose icons are downloaded from `https://fonts.gstatic.com/render/v1/Material+Symbols+{Style}/{size}dp/{icon}.kt?...`
- Apple symbol SVGs are downloaded from `https://fonts.gstatic.com/s/i/short-term/release/{style}/{icon}/{variant}/{icon}_{variant}_symbol.svg`
- The Apple `_symbol.svg` response is a Google symbol sheet, not the same single-icon asset returned by `--format svg`
- The script uses only Python standard library modules and is portable across Linux, macOS, and Windows

## URL Patterns

Icons are downloaded using these patterns:
```
https://fonts.gstatic.com/s/i/short-term/release/{style_folder}/{icon_name}/default/{size}px.xml
https://fonts.gstatic.com/s/i/short-term/release/{style_folder}/{icon_name}/{variant_segments}/{size}px.xml
https://fonts.gstatic.com/s/i/short-term/release/{style_folder}/{icon_name}/default/{size}px.svg
https://fonts.gstatic.com/s/i/short-term/release/{style_folder}/{icon_name}/{variant_segments}/{size}px.svg
https://fonts.gstatic.com/render/v1/{compose_family}/{size}dp/{icon_name}.kt?var=opsz,wght,FILL,GRAD,ROND@{size},400,0,0,50
https://fonts.gstatic.com/s/i/short-term/release/{style_folder}/{icon_name}/{variant_folder_or_default}/{icon_name}{suffix}_symbol.svg
```

Where `style_folder` is one of:
- `materialsymbolsoutlined` (for outlined style)
- `materialsymbolsrounded` (for rounded style)
- `materialsymbolssharp` (for sharp style)

And `compose_family` is one of:
- `Material+Symbols+Outlined`
- `Material+Symbols+Rounded`
- `Material+Symbols+Sharp`

For XML and SVG variant folders:
- only non-default axis segments are included
- negative grades are encoded with `N`, for example `gradN25`
- examples: `fill1`, `wght700`, `grad200`, `wght700grad200fill1`

For Apple symbol SVGs:
- the folder name is `default` for default axes, otherwise it uses the same variant segment naming
- the file name repeats the icon name, followed by `_{variant}` if custom axes are used, and ends with `_symbol.svg` (e.g. `toggle_on_symbol.svg` or `toggle_on_grad200fill1_symbol.svg`)
