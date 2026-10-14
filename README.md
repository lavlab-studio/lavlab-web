# LavLab — web con panel de proyectos

Este proyecto conserva la **versión 7** de LavLab: intro negra con PNG original y portada con `lavlab.` gigante.

## Ver la demo
Abre `dist/index.html` en Chrome o Safari. Los seis proyectos actuales son **ejemplos**, no trabajos reales.

## Publicar y activar el panel
1. Crea una cuenta de GitHub (si no la tienes) y un repositorio privado o público para LavLab.
2. Sube **todo el contenido de esta carpeta** al repositorio, incluidos `.pages.yml`, `template.html`, `build.py`, `data/` y `media/`.
3. En [Cloudflare Pages](https://dash.cloudflare.com/), conecta el repositorio de GitHub. Configura **Build command:** `python3 build.py` y **Build output directory:** `dist`. No hace falta instalar dependencias.
4. Entra en [Pages CMS](https://app.pagescms.org/), inicia sesión con GitHub y autoriza la aplicación para el repositorio. Abre **Proyectos LavLab**.
5. Añade/edita/elimina proyectos, sube una imagen de portada y guarda. El cambio se guarda en GitHub; el despliegue de Cloudflare Pages conectado al repositorio reconstruirá la web.
6. Conecta el dominio propio desde Cloudflare Pages cuando esté listo.

## Campos del panel
- Nombre del proyecto
- Categoría
- Descripción
- Imagen de portada (subida al repositorio)
- Enlace externo (Spotify, Bandcamp, YouTube, web del proyecto...)
- Visible en la web (sí/no)

**Orden:** el orden de la lista JSON es el orden de las tarjetas. Si el panel no permite reordenar la lista cómodamente, se puede añadir un campo de orden en una siguiente iteración.

## Notas importantes
- `hola@lavlab.studio` es **provisional**: sustituidlo por vuestro correo real antes de publicar.
- La introducción usa el PNG original incrustado en la plantilla.
- El panel de Pages CMS funciona online, con cuenta y permisos GitHub. No se activa simplemente abriendo el HTML local.
- La web sigue siendo estática, sin base de datos ni formulario de contacto backend. El enlace actual de contacto abre la aplicación de correo del visitante.
- El contenido de muestra debe sustituirse por proyectos reales antes del lanzamiento.
- No pongáis contraseñas ni tokens en este repositorio.

## Desarrollo local
`python3 build.py` y abrir `dist/index.html`.
