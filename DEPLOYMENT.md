# Deployment and Publishing Instructions

## 1. Local setup

```bash
uv venv
uv pip install -r requirements.txt
```

## 2. Build website HTML

```bash
uv run python scripts/build_site.py
```

The generated website is in `site/`.

## 3. Build PDF book

```bash
uv run python scripts/build_pdf.py
```

Outputs:
- `dist/book.html`
- `dist/book.pdf`

If PDF generation fails, install system dependencies required by WeasyPrint:

```bash
sudo apt-get update
sudo apt-get install -y libcairo2 libpango-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
```

## 4. Deploy to GitHub Pages

1. Push to `main`.
2. In repository settings, enable **Pages** with **GitHub Actions** source.
3. The workflow `.github/workflows/deploy-pages.yml` builds and deploys `site/`.

## 5. Suggested release flow

1. Run local build (`build_site.py`, `build_pdf.py`).
2. Review generated `site/` and `dist/book.pdf`.
3. Commit markdown source and scripts.
4. Push to `main` to trigger GitHub Pages deploy.
