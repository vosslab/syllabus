# REPO_TYPE.md

`REPO_TYPE` is the root marker that declares which shared template families a
repository consumes. It classifies a repository; it does not define repository
style. Repository conventions live in [docs/REPO_STYLE.md](../../docs/REPO_STYLE.md).

## Marker format

- Store `REPO_TYPE` at the repository root.
- Write one or more lowercase type names followed by a newline.
- Separate several names with commas and no spaces, for example `python,rust`.
- Preserve declaration order.
- Maintain the marker when the repository changes; it remains live after bootstrap.

## Available types

The available names, in canonical display order, are `python`, `pypi`,
`typescript`, `rust`, `swift`, `other`, `scripted`, `website`, `compiled`, and
`all`.

Inheritance adds the complete parent rule set:

- `pypi` -> `python` -> `scripted`
- `typescript` -> `website`
- `rust` -> `compiled`
- `swift` -> `compiled`

`scripted`, `website`, `compiled`, and `other` are root types. Every listed type
is valid as a direct marker. `all` expands to every concrete type supported by
the template.

## Multiple types

Declare several types only when a repository genuinely ships several families,
such as a Python CLI with a Rust extension. The repository receives the union of
the declared types and their inherited rule sets. Declaration order determines
which typed overlay wins if several overlays provide the same path.
