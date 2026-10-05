# Course color preferences

## Stated preferences

Neil's presentation preferences are recorded in [HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md):

- Use Roosevelt University's green palette for the main website and favicon.
- Use subtle course colors across headings and tables.
- Provide a student-accessible light and dark theme toggle.
- Keep Genetics quiz coverage color-coded, with the quiz number repeated as the non-color cue.

Neil also accepts the hidden `.meta.yml` files because they follow MkDocs Material's metadata
convention. Keep course palette configuration there.

## Course identity palette

The earlier guidance names four course identities. The three Fall 2026 courses use those same
header colors today; Biochemistry is a recorded future-course preference. The linked metadata
files remain the editable source of truth for active courses.

| Course | Color family | Header and light accent | Dark content accent |
| --- | --- | --- | --- |
| Biostatistics, BIOL 318/418 | Dark lime | `#477427` | `#a8d58a` |
| Genetics, BIOL 351/451 | Blue | `#1565c0` | `#8ab4f8` |
| Biotechnology, BIOL 480 | Brick red | `#9e3d32` | `#f28b82` |
| Biochemistry, BCHM 355 | Purple | `#7b1fa2` | Not recorded |

Biochemistry has no active Fall 2026 metadata file. Choose and review its dark-theme companion
when that course is added. No additional course identity colors were found in the reviewed Git
history; do not infer colors for other courses from this palette.

Edit the corresponding course metadata:

- Biostatistics: [site_docs/fall_2026/biostats/.meta.yml](../site_docs/fall_2026/biostats/.meta.yml)
- Genetics: [site_docs/fall_2026/genetics/.meta.yml](../site_docs/fall_2026/genetics/.meta.yml)
- Biotechnology: [site_docs/fall_2026/biotech/.meta.yml](../site_docs/fall_2026/biotech/.meta.yml)

`course_color` supplies the website header, light-theme content accents, and PDF accents.
`course_color_dark` supplies dark-theme content accents. DOCX retains neutral styling.
See [FILE_FORMATS.md](FILE_FORMATS.md#course-metadata) for the field format and contrast targets.
Schedule quiz colors are separate supplementary cues, not these course-wide accents.

Plain `rg` skips hidden files. To find the palette definitions:

```bash
rg --hidden 'course_color' site_docs/fall_2026
```

## Recovered historical guidance

Commit `dc5ed31` (2026-08-25) records all four course colors under "Course identity colors" in
[HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md). Commit `af0cc01` (2026-08-26) removed that section during
a broader cleanup of owner guidance. The original palette audit also recorded the future BCHM 355
purple header. This reference restores the mapping that was missing from the current guidance.

Inspect the original entry with:

```bash
git show dc5ed31:docs/HUMAN_GUIDANCE.md
```

The old restriction to web headers and neutral downloaded documents was superseded by the later
heading/table styling work. Preserve the current website and PDF accent behavior described above.
The [palette_contrast_audit.md](active_plans/audits/palette_contrast_audit.md) also explains why
Biostatistics uses dark lime `#477427` instead of the initially proposed `#558b2f`.

## Reviewing palette changes

After changing metadata, rebuild and inspect course pages in both themes and the generated PDF.
Check heading, table, link, and header readability in their actual backgrounds. Update the table
above when the configured palette changes.

Exact RGB comparisons and pairwise course-color comparisons are one-time presentation checks.
Use `tests/_temp/` for temporary verification and remove those checks when the work is complete.
Apply the permanent-test checklist in [PYTEST_STYLE.md](PYTEST_STYLE.md) before retaining any test;
theme switching, persistence, and accessibility behavior have lasting value independent of shades.
