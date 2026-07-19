# Testing Policy

## Command Matrix

| Check | Command | Status | Notes |
| --- | --- | --- | --- |
| Markdown sanity | `./.beryl/scripts/check-md.sh` | available | Unclosed fences and tabs |
| Test manifest immutability check | `./.beryl/scripts/check-tests-unchanged.sh` | available | Tracks configured test scope |
| Affected test gate | `./.beryl/scripts/check-affected.sh --worktree` | available | No project-specific tests configured yet |
| Aggregate deterministic gate | `./.beryl/scripts/check.sh` | available | Run after edits |
| Python script syntax | `python3 -m py_compile scripts/build_latex_pdf.py scripts/build_pdf.py scripts/build_site.py` | available | Use after build-script edits |
| LaTeX publication build | `python3 scripts/build_latex_pdf.py` | available when Pandoc and LaTeX engine are installed | Required for publication-impacting changes |
| HTML/site build | `uv run python scripts/build_site.py` | available when dependencies are installed | Required for website changes |
| HTML/CSS PDF build | `uv run python scripts/build_pdf.py` | dependency-sensitive | WeasyPrint/Markdown dependencies may be missing |
| Git whitespace check | `git diff --check` | available | Run before final response |

## Default Loop

1. Classify the task through `.beryl/agent/task-routing.md`.
2. Read the relevant `.beryl/agent/` context and manuscript/build files.
3. State success checks before implementation when doing feature work.
4. Edit source files, not generated artifacts, unless rebuilding.
5. Run narrow checks first.
6. Rebuild generated artifacts if source/build inputs changed.
7. Run `./.beryl/scripts/check.sh`.
8. Report unavailable checks honestly.

## Publication Verification

For publication-impacting changes, run:

```bash
python3 -m py_compile scripts/build_latex_pdf.py scripts/build_pdf.py scripts/build_site.py
python3 scripts/build_latex_pdf.py
./.beryl/scripts/check.sh
git diff --check
```

If Tectonic needs to fetch its LaTeX bundle, network access may be required. If the build cannot run, report the exact missing binary/package/network condition.

After rebuilding, scan for known publication regressions:

```bash
rg -n 'This draft|Three-theory braid|How to study this formally|Translating the Theory into Agentic Practice|\.md\)|undefined|Missing character' dist/book-latex.md dist/book.tex
```

Expected current state:

- `dist/book-latex.pdf` builds successfully.
- Citation anchors resolve in the LaTeX output.
- The generated book uses `book` class and includes author metadata.
- Remaining TeX warnings, if any, should be minor box/page-fill warnings rather than missing glyphs or unresolved references.

## Generated Output Verification

Generated artifacts matter in this repository. If these inputs change, rebuild:

- `book/**/*.md` or `book/references.md`: rebuild `dist/book-latex.*`.
- `scripts/build_latex_pdf.py` or `templates/latex-header.tex`: rebuild `dist/book-latex.*`.
- `templates/page.html` or `book/assets/style.css`: rebuild site output.
- `scripts/build_site.py`: rebuild `site/`.
- `scripts/build_pdf.py`: rebuild `dist/book.html` / `dist/book.pdf` if dependencies are available.

## Test Manifest Scope

The repository currently has no substantive test suite. Beryl installed `tests/.manifest.sha256` as the manifest for future tests. Do not claim unit-test coverage exists until actual tests are added.

If tests are added or intentionally changed:

1. Update `.beryl/agent/test-manifest.conf` if needed.
2. Run `./.beryl/scripts/update-test-manifest.sh`.
3. Explain why the manifest changed.

## Mocking Rules

When future runnable exercises or tests are added, mock external network/model APIs, clocks, randomness, and filesystem side effects outside the test sandbox. Do not mock the manuscript build scripts' core source-ordering and heading-rewrite behavior when those are under test.
