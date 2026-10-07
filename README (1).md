# 🌐 Sitio web de EyeSafe

Landing page estática (HTML + CSS + JS, sin dependencias) con simulador interactivo.

## Ver en local
```bash
cd docs
python -m http.server 8000   # abre http://localhost:8000
```

## Publicar en GitHub Pages
1. Sube el repositorio a GitHub.
2. Ve a **Settings → Pages → Build and deployment → Source: GitHub Actions**.
3. Haz push a `main`: el workflow `.github/workflows/pages.yml` publicará la carpeta `docs/`.
4. Tu sitio quedará en `https://<tu-usuario>.github.io/EyeSafe/`.

> Recuerda reemplazar `<tu-usuario>` en los enlaces de `index.html`.
