# Palette contrast audit

## Scope

This audit covers the authored text colors used by the static website and generated syllabus
documents. Material theme components also run through the browser accessibility audit.

| Surface | Foreground | Background | Ratio | Target |
| --- | --- | --- | --- | --- |
| Website body link | `#4051b5` | `#ffffff` | 6.86:1 | PASS |
| Website footer copyright | `#999999` | `#171717` | 6.29:1 | PASS |
| BIOL 318/418 header text and controls | `#ffffff` | `#477427` | 5.53:1 | PASS |
| BIOL 351/451 header text and controls | `#ffffff` | `#1565c0` | 5.75:1 | PASS |
| BIOL 480 header text and controls | `#ffffff` | `#9e3d32` | 6.63:1 | PASS |
| Future BCHM 355 header text and controls | `#ffffff` | `#7b1fa2` | 8.20:1 | PASS |
| DOCX/PDF link | `#004a83` | `#ffffff` | 9.10:1 | PASS |
| DOCX/PDF title | `#17365d` | `#ffffff` | 12.19:1 | PASS |

All measured pairs exceed the repository's 5.5:1 target. Body links are also underlined so meaning
does not depend on color. The automated browser audit checks rendered WCAG AA contrast on desktop
and mobile pages.

The initially proposed BIOL 318/418 lime, `#558b2f`, measured 4.10:1 against white. The implemented
`#477427` preserves its hue while meeting the house target. Course colors are website metadata and
do not enter the neutral PDF or DOCX styles.
