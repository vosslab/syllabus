# Design decisions

<!-- VENDORED HEADER: START -->
Record each durable decision about how this code and repository are shaped, once it is settled, with
the reasoning a later reader needs. Guidance Neil Voss states belongs in
[HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md), dated history in `docs/CHANGELOG.md`, open discussion in
`docs/active_plans/decisions/`. [PROPAGATED HEADER - ENTRIES BELOW ARE YOURS]
<!-- VENDORED HEADER: END -->

Write each decision as a level-three heading with these four fields. `Owner` names the
authoritative code or contract document, rather than a person.

```markdown
### <decision title>

**Decision.** <the durable direction>

**Why.** <the reason it was chosen>

**Consequence.** <the constraint a future change preserves>

**Owner.** <the authoritative code or contract doc>
```

## Software design

## Dependencies

## Generated artifacts

### Use one instructor image source with a website-only dark-theme substitution

**Decision.** Keep one accessible Markdown image in the shared instructor-contact fragment. It
references the light-background portrait used by the light website theme, PDF, and DOCX. When the
Material website uses its `slate` scheme, CSS replaces only the rendered image content with the
matching dark-background portrait.

**Why.** One source image keeps the shared fragment portable across MkDocs, Pandoc, and
WeasyPrint, gives the portrait one text alternative and one semantic table position, and avoids
duplicating theme-specific markup in every generated document. PDF and DOCX have light pages and
therefore do not need the dark variant.

**Consequence.** Preserve both tracked portrait assets, the canonical light-image reference, and
the website's scoped dark-theme substitution as one unit. A future presentation change must still
embed only the light portrait in PDF and DOCX, expose one meaningful text alternative, and avoid
duplicating the portrait in document source.

**Owner.** `docs/FILE_FORMATS.md`,
`site_docs/fall_2026/shared/fragments/INSTRUCTOR_CONTACT_DETAILS.md`, and
`site_docs/assets/stylesheets/site.css`.
