# Palette contrast audit

## Scope

This audit covers the authored text colors used by the static website and generated syllabus
documents. Material theme components also run through the browser accessibility audit.

| Surface | Foreground | Background | Ratio | Target |
| --- | --- | --- | --- | --- |
| Website body link and shared heading, light | `#007849` | `#ffffff` | 5.55:1 | PASS |
| Website body link and shared heading, dark | `#73c167` | `#1e2923` | 6.84:1 | PASS |
| Website footer copyright | `#999999` | `#171717` | 6.29:1 | PASS |
| BIOL 318/418 header text and controls | `#ffffff` | `#477427` | 5.53:1 | PASS |
| BIOL 351/451 header text and controls | `#ffffff` | `#1565c0` | 5.75:1 | PASS |
| BIOL 480 header text and controls | `#ffffff` | `#9e3d32` | 6.63:1 | PASS |
| BIOL 318/418 website accent, dark | `#a8d58a` | `#1e2923` | 8.99:1 | PASS |
| BIOL 351/451 website accent, dark | `#8ab4f8` | `#1e2923` | 7.13:1 | PASS |
| BIOL 480 website accent, dark | `#f28b82` | `#1e2923` | 6.29:1 | PASS |
| BIOL 318/418 PDF accent | `#477427` | `#ffffff` | 5.53:1 | PASS |
| BIOL 351/451 PDF accent | `#1565c0` | `#ffffff` | 5.75:1 | PASS |
| BIOL 480 PDF accent | `#9e3d32` | `#ffffff` | 6.63:1 | PASS |
| DOCX/PDF link | `#004a83` | `#ffffff` | 9.10:1 | PASS |

All measured pairs exceed the repository's 5.5:1 target. Body links are also underlined so meaning
does not depend on color. The automated browser audit checks rendered WCAG AA contrast on desktop
and mobile pages.

The initially proposed BIOL 318/418 lime, `#558b2f`, measured 4.10:1 against white. The implemented
`#477427` preserves its hue while meeting the house target. Course colors are website metadata and
provide the website and PDF heading/table accents. DOCX retains its format-native neutral styling.
