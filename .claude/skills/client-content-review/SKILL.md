---
name: client-content-review
description: Genera un archivo HTML de revisión de contenido para que un cliente no técnico revise y corrija TODO el texto y las imágenes de un sitio web antes de publicarlo — es un solo archivo autocontenido (sin necesitar cuenta, login ni internet especial) donde cada texto es editable y cada imagen tiene un botón para subir una nueva desde el celular o computadora del cliente; al guardar, descarga el mismo archivo con las correcciones incluidas y resaltadas, listo para regresarlo. Usa esta skill siempre que el usuario pida "un archivo de revisión para el cliente", "que el cliente revise/corrija el contenido del sitio", "mandar la página para aprobación", un "formulario editable" del contenido de un sitio, o algo similar a "el archivo que hiciste para ISEBCA" — aunque no lo pida con esas palabras exactas, cualquier intención de "que el cliente vea y edite/apruebe el contenido de su página web antes de publicarla" aplica aquí.
---

# Revisión de contenido para cliente

## Qué es y quién lo usa

El usuario de esta skill (típicamente una agencia o freelancer haciendo sitios web para terceros) necesita que SU cliente — el dueño del negocio, sin conocimientos técnicos — revise todo el contenido de una página web antes de que se publique, y pueda corregir texto e imágenes sin necesitar una cuenta, sin depender de internet especial, y sin que tú tengas que interpretar comentarios sueltos por WhatsApp sobre "el segundo párrafo de la página de servicios".

La solución es un único archivo `.html` que el cliente abre en cualquier navegador: ve cada texto en una caja editable y cada imagen con un botón "Cambiar imagen" (selector de archivos normal del sistema — nada de subir a ningún servidor). Al terminar, un botón descarga ese mismo archivo con sus ediciones ya incluidas y resaltadas en amarillo, para que se lo regrese a quien se lo mandó (por WhatsApp, correo, etc.) y esa persona te lo suba a ti para aplicar los cambios reales al sitio.

Este patrón ya se probó y funciona (extracción de contenido real, edición de texto, carga de imágenes en base64, descarga y reapertura con los cambios resaltados) — no hace falta reinventarlo ni pedir permiso para el enfoque técnico, solo ejecutar los pasos de abajo.

## Paso 1 — Reunir el contenido real del sitio

No inventes ni resumas el contenido: extrae el texto TAL CUAL aparece en las páginas reales (HTML, Docs, lo que el usuario te dé) y la URL o ruta de archivo de cada imagen real. Si el usuario no te ha dado los archivos del sitio todavía, pídeselos (o la ruta del proyecto) antes de seguir.

Cubre TODAS las páginas del sitio, no solo el inicio — el objetivo es que el cliente vea "toda la información que va a tener la página web", incluyendo páginas legales/informativas si las hay (privacidad, términos, etc.), no solo el copy de marketing.

Para cada pieza de contenido decide su tipo:
- **text** — una línea corta: títulos, nombres, etiquetas, cifras.
- **textarea** — un párrafo o lista de varias líneas (usa `\n` para separar puntos si es una lista dentro de un mismo campo, p. ej. viñetas de un párrafo).
- **image** — cualquier foto/ilustración real de contenido (hero, equipo, proyectos, testimonios). No es necesario incluir iconos puramente decorativos sin valor informativo, pero ante la duda, inclúyela — es preferible que sobre a que falte.

## Paso 2 — Construir `fields.json`

Arma un arreglo JSON de campos con esta forma (el script agrega automáticamente `original` y `changed`, no los incluyas):

```json
[
  {"id": "hero_title", "section": "1. Inicio", "label": "Título principal", "type": "text", "value": "Texto real actual"},
  {"id": "hero_sub", "section": "1. Inicio", "label": "Subtítulo", "type": "textarea", "value": "Párrafo real actual..."},
  {"id": "hero_img", "section": "1. Inicio", "label": "Foto del hero", "type": "image", "value": "https://.../foto.jpg"}
]
```

Reglas:
- `id`: único, solo letras/números/guión bajo — es la clave que usarás después para saber qué campo cambió cuando el cliente te regrese el archivo.
- `section`: agrupa visualmente los campos; el orden de aparición en el JSON define el orden de las secciones en el formulario. Usa un nombre de sección por página del sitio (p. ej. "1. Inicio", "2. Servicios", "3. Proyectos"...) para que el cliente entienda dónde está parado.
- `type: "image"`: el `value` puede ser una URL (se deja tal cual, más liviano) o una ruta de archivo local (el script la convierte a base64 automáticamente).
- Incluye al final una sección tipo "Comentarios generales" con un campo `textarea` vacío (`"value": ""`) para que el cliente pueda anotar cualquier cosa que no encaje en un campo específico.

Guarda esto como un archivo `fields.json` (en el directorio de trabajo o donde prefieras).

## Paso 3 — Generar el archivo

Ejecuta el script incluido en esta skill:

```bash
python3 <ruta-de-esta-skill>/scripts/generate_review_tool.py \
  --fields fields.json \
  --output revision-cliente-NOMBRE.html \
  --client-name "Nombre del Cliente" \
  --logo /ruta/al/logo.png \
  --file-prefix NOMBRE
```

- `--logo` es opcional (si no hay logo, se usa un ícono neutro) — si el proyecto tiene uno, pásalo para que el archivo se vea con su marca; se embebe como base64 automáticamente, así el archivo sigue siendo 100% autocontenido (sin depender de ninguna carpeta junto a él).
- `--file-prefix` controla el nombre del archivo que se descarga cuando el cliente guarda sus cambios (por defecto se deriva de `--client-name`).
- Lee el docstring del script (`--help` o el encabezado del archivo) si necesitas más detalle del formato — es la referencia autoritativa, no la repitas de memoria.

## Paso 4 — Verificación rápida (recomendado, no bloqueante)

Si tienes Playwright disponible, abre el archivo generado y confirma que: renderiza todos los campos esperados, que editar un campo lo resalta y sube el contador, y que el botón de guardar dispara una descarga con el JSON embebido actualizado. Esto detecta typos en `fields.json` (ids duplicados, tipos inválidos) antes de mandárselo al usuario. Si no tienes Playwright a mano, no bloquees la entrega por esto — el script ya valida la estructura del JSON al generar.

## Paso 5 — Entregar

Manda el archivo `.html` generado al usuario (con la herramienta de envío de archivos que tengas disponible). Recuérdale en una línea: que se lo mande a su cliente por el medio que prefiera (WhatsApp, correo), que cuando se lo regresen te lo suba de vuelta, y que tú vas a leer el JSON embebido en `<script id="content-data" type="application/json">` de ese archivo para ver exactamente qué campos cambiaron (comparando `value` contra `original`, y `changed: true` en las imágenes) y aplicar las correcciones al sitio real.

## Notas de mantenimiento

- La plantilla visual/JS vive en `assets/template.html` — es HTML+CSS+JS puro sin dependencias externas de build. Si el usuario pide cambios de diseño o comportamiento a la herramienta misma (no al contenido de un cliente en particular), edita esa plantilla, no la regeneres desde cero cada vez.
- El motor de guardado reconstruye el archivo completo a partir del HTML `<head>` (estático), el `<script id="content-data">` (con los datos actualizados) y el propio script de arranque — evita clonar el DOM en vivo (`outerHTML` de inputs/textareas no refleja ediciones del usuario, es un error fácil de cometer si se reescribe esta lógica).
