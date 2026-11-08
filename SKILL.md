---
name: web-edicion-incremental
description: "Usar al modificar o mejorar una página web existente: editar solo lo necesario sobre el archivo más reciente, sin releer ni reescribir todo el código."
---

# Edición incremental de páginas web (ahorro de tokens)

Objetivo: mejorar o agregar a una página web existente gastando el mínimo de tokens. Nunca regenerar la página completa.

## Reglas de oro

1. **Trabajar siempre sobre el archivo más reciente.** Si hay varias versiones (index.html, index-v2.html, etc.), usar la de fecha de modificación más reciente (`ls -t`). No crear un archivo nuevo salvo que el usuario lo pida.
2. **No leer el archivo completo.** Localizar primero la zona a cambiar con búsqueda (Grep: id, clase, texto visible, nombre de sección) y leer solo ese rango de líneas (Read con offset/limit, ~20–60 líneas alrededor).
3. **No reescribir.** Usar Edit con reemplazos puntuales o inserciones. Prohibido usar Write sobre un archivo existente para cambiar unas cuantas líneas.
4. **Agregar en vez de rehacer.** Nuevas secciones se insertan antes/después de un ancla existente (ej. antes de `</main>` o después de `<section id="servicios">...`). CSS nuevo va al final del bloque `<style>` o del archivo CSS; JS nuevo al final del script existente.
5. **No mostrar el código completo en la respuesta.** Responder solo con: qué cambió, en qué sección y, si acaso, el fragmento nuevo (máx. ~30 líneas).
6. **Contexto mínimo.** Usar solo las últimas 2–3 instrucciones del usuario y la bitácora (abajo). No releer conversaciones o versiones anteriores.

## Bitácora de cambios (reemplaza al historial del chat)

Mantener un archivo `CAMBIOS-WEB.md` en la misma carpeta de la página, con SOLO los últimos 3 cambios:

```
# Últimos cambios — <nombre del proyecto>
Archivo actual: index.html

1. [fecha] Sección hero: nuevo botón WhatsApp (líneas ~45-60)
2. [fecha] Agregada sección testimonios antes de </main>
3. [fecha] Colores: --primario cambiado a #0B3D5C
```

- Al iniciar: leer `CAMBIOS-WEB.md` (si existe) en vez del archivo completo o del historial.
- Al terminar: agregar el cambio nuevo arriba y borrar el más viejo para dejar solo 3.

## Flujo

1. Leer `CAMBIOS-WEB.md` (si existe) y ubicar el archivo actual.
2. Si la instrucción es ambigua (qué sección, qué texto, qué color), preguntar antes de editar.
3. Grep para encontrar el ancla → Read solo ese rango.
4. Edit puntual (o varias Edit pequeñas). Nunca Write completo.
5. Verificar solo la zona editada (re-leer ese rango o abrir preview si está disponible).
6. Actualizar `CAMBIOS-WEB.md`.
7. Responder en 2–4 líneas: qué se cambió y dónde.

## Excepciones

- Si el usuario pide explícitamente "rehacer", "rediseñar todo" o "versión nueva", entonces sí se puede reescribir.
- Si el archivo está roto (HTML sin cerrar, errores graves), avisar antes de hacer una corrección amplia.
