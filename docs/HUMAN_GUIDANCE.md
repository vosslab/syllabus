# Human guidance

## Review priorities

- Apply "Focus on important issues" from [REPO_STYLE.md](REPO_STYLE.md): prioritize content,
  correctness, maintainability, validation, and delivery over cosmetic details.
- Keep policies and student resources independently editable and merge them into each complete
  course syllabus during the build.
- Promote accessibility through semantic source, readable output, and regular audits without
  making every accessibility heuristic a publication gate.

## Plans and validation

- Ground each release gate in a real user, archival, security, or delivery requirement.
- Separate durable publication gates, repeatable advisory audits, and one-time implementation
  evidence.
- Do not require byte, pixel, page-count, timing, or renderer equivalence unless the product has a
  documented need for that exact property.
- Apply the permanent-test checklist in [PYTEST_STYLE.md](PYTEST_STYLE.md). Prefer deleting a
  fragile test over preserving an implementation detail.
- Keep temporary experiments and rendered comparisons out of the permanent suite. Record useful
  conclusions in the changelog or an active-plan audit.

## Course identity colors

- Use course colors as a restrained web-header cue while keeping page bodies and downloaded
  documents neutral.
- Use dark lime `#477427` for BIOL 318/418, blue `#1565c0` for BIOL 351/451, brick red `#9e3d32`
  for BIOL 480, and purple `#7b1fa2` for BCHM 355.
- Preserve at least 5.5:1 contrast between course headers and white header text or controls.
