# 🤝 Guía de contribución a EyeSafe

¡Gracias por querer mejorar EyeSafe! Toda contribución suma: código, documentación, ideas, pruebas en campo o reportes de errores.

## 🐛 Reportar un bug
1. Busca en los [issues](../../issues) por si ya fue reportado.
2. Abre uno nuevo con la plantilla **Bug report** e incluye pasos para reproducirlo, comportamiento esperado, versión y entorno.

## 💡 Proponer una mejora
Abre un issue con la plantilla **Feature request** o inicia una conversación en [Discussions](../../discussions).

## 🔧 Flujo de trabajo
```bash
git clone https://github.com/<tu-usuario>/EyeSafe.git
cd EyeSafe
git checkout -b feature/mi-mejora
# ... haz tus cambios ...
git commit -m "feat: descripción corta del cambio"
git push origin feature/mi-mejora
```
Luego abre un **Pull Request** hacia `main`.

## 📏 Convenciones
- Commits siguiendo [Conventional Commits](https://www.conventionalcommits.org/es/) (`feat:`, `fix:`, `docs:`, `refactor:`...).
- PRs pequeños y enfocados en un solo tema.
- Documenta los cambios relevantes en el README o en comentarios.
- Prueba tu cambio con un video de ejemplo antes de enviarlo.

## 📜 Código de conducta
Al participar aceptas respetar el [Código de Conducta](./CODE_OF_CONDUCT.md).
