# Contributing to SIAP

Thank you for helping make **Structure and Interpretation of Agentic Patterns** more rigorous, more useful, and more delightful. This repository contains both a book and the small publication machine that lets the book travel.

## Start Here

1. Read the [Code of Conduct](CODE_OF_CONDUCT.md), [Security Policy](SECURITY.md), and [license guide](LICENSES.md).
2. Search existing issues before opening a new one.
3. For a substantial change, open an issue first so the argument, interface, or visual direction can be discussed before anyone builds a cathedral around a footnote.
4. Fork the repository, create a focused branch, and open a pull request against `main`.

## Choose the Right Surface

| You want to change | Start here | Important boundary |
| --- | --- | --- |
| Book prose, references, diagrams, or cartoons | `book/` | Edit sources, never generated publication output. |
| Reader-facing site behavior | `scripts/build_site.py`, `templates/`, `book/assets/style.css` | Rebuild and inspect the generated site. |
| Print/PDF behavior | `scripts/build_latex_pdf.py`, `templates/latex-header.tex` | Rebuild through the script; never hand-edit `dist/`. |
| Tests and checks | `tests/`, `.beryl/scripts/` | Preserve or strengthen deterministic coverage. |

`book/publication.toml` declares the reader-facing order. Companion `*-notes.md` files and `book/continuity-ledger.md` are editorial support, not published prose.

## Set Up a Working Copy

```bash
git clone https://github.com/Praneeth-Suresh/SIAP.git
cd SIAP
uv venv
uv pip install -r requirements.txt
```

Run the baseline gate before changing anything:

```bash
./.beryl/scripts/check.sh
```

## Make a Focused Change

- Keep one pull request to one purpose.
- Preserve the book's explanatory, witty, slightly grandiose voice. Teach agentic ideas by construction: state, transitions, contracts, and executable consequences beat slogans.
- Cite external claims using the repository's clickable numeric citation style and add sources to `book/references.md`.
- For manuscript or publication-build changes, run `python3 scripts/build_latex_pdf.py`; for site changes, run `uv run python scripts/build_site.py`.
- Do not commit generated `site/` output or hand-edit generated `dist/` files. Rebuild tracked publication artifacts only when their source inputs require it.
- Do not commit credentials, tokens, or private data.

## Test and Verify

Run the narrowest relevant check first, then the aggregate gate:

```bash
uv run python -m unittest discover -s tests
./.beryl/scripts/check.sh
git diff --check
```

If you intentionally add or change a test, regenerate the test manifest and include it in the same pull request:

```bash
./.beryl/scripts/update-test-manifest.sh
```

## Open a Pull Request

Use the pull-request template. Explain the problem, the changed public behavior, the checks you ran, and whether generated artifacts changed. Maintainers may ask for a smaller scope, stronger evidence, or a source-level change in place of a generated-file edit. That is not ceremony; it is how the machine stays inspectable.

## Contributor License Agreement

By submitting a contribution, you agree to license it under the license that applies to the path you change, as described in [LICENSES.md](LICENSES.md). If you cannot make that grant, please say so before opening the pull request.
