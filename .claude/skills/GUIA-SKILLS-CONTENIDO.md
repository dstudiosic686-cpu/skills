# Guía rápida — Skills de contenido (D Studios)

Instaladas el 24 oct 2026. Úsalas abriendo **Claude Code** dentro de este repo.

## 0. Diseñador gráfico (investiga, analiza y crea desde un brief)
| Skill | Para qué | Cómo pedirlo |
|---|---|---|
| `disenador-grafico` | Brief → referencias → análisis → 2–3 direcciones creativas → pieza final con crítica. Posts, carruseles, feeds, portadas de reels/videos, logos, branding y webs | `/disenador-grafico Carrusel para Dental Studio Group sobre blanqueamiento, entrega en Canva` |

Dile el formato de entrega en la petición: **PNG**, **Figma editable** o **Canva**.

## 1. Carruseles y posts
| Skill | Para qué | Cómo pedirlo |
|---|---|---|
| `carousel-lite` | Tema → copy (hook, slides, CTA) → PNGs 1080x1440 | `/carousel-lite 5 errores al cuidar tus brackets` |
| `threads-carousel` | Texto → carrusel en 6 formatos (IG 1:1, 4:5, Stories/TikTok 9:16, LinkedIn PDF, 16:9) | "Haz un carrusel de Instagram con este texto: …" |

Primera vez: `cd .claude/skills/carousel-lite && npm install`

## 2. Animaciones para tus videos (Remotion)
`remotion-create`, `remotion-markup`, `remotion-captions`, `remotion-render`, `remotion-studio`, `remotion-best-practices` y más.

- Ejemplo: `/remotion-create Lower third animado "Dra. Laura Yan Ruiz — Otorrino" con colores de marca, fondo transparente, 5 s`
- Pide siempre **fondo transparente (ProRes 4444 o WebM)** para encimarlo en CapCut/Premiere.
- Primera vez en un proyecto nuevo: `npx create-video@latest mi-animacion`

## 3. Edición de video en crudo
Flujo recomendado: **cut-video → add-zooms → clipify**

| Skill | Para qué |
|---|---|
| `cut-video` | Quita silencios, muletillas, tomas malas y repeticiones |
| `add-zooms` | Punch-zooms en palabras clave y Ken Burns suave |
| `clipify` | Corta clips, reencuadra 16:9 → 9:16, subtítulos palabra por palabra |
| `net-new-video-editor` | Video recién grabado (talking head) → borrador vertical con hook card, subtítulos y audio normalizado |
| `short-form-pipeline` | Video largo (podcast, live, entrevista) → 2–5 clips de 30–60 s con mejor gancho |

Requisitos en tu Mac (una sola vez, en Terminal):
```bash
brew install ffmpeg python@3.12 node
pip3 install openai-whisper
```

Ejemplo: "Limpia este video con /cut-video y luego ponle zooms: ~/Desktop/crudo.mov"

## Notas
- Las skills de video corren mejor en Claude Code **en tu Mac** (cut-video y clipify usan aceleración de Apple).
- Las skills de ericosiu traen un aviso de telemetría opcional; si te pregunta, puedes decir que no.
- Fuentes: tenfoldmarc/carousel-lite, itchernetski/threads-carousel-claude-skill, remotion-dev/skills, louisedesadeleer/{cut-video,add-zooms,clipify}, ericosiu/ai-marketing-skills.

---

# Skills para páginas web (agregadas 24 oct 2026)

| Skill | Para qué | Cómo pedirlo |
|---|---|---|
| `gsap-core`, `gsap-scrolltrigger`, `gsap-timeline`, `gsap-plugins`, `gsap-react`, `gsap-performance`… | Animaciones web: scroll, pinning, texto que se revela, transiciones | "Anima el hero con GSAP: el título entra letra por letra y las tarjetas aparecen al hacer scroll" |
| `gsap-awwwards-website` | Plantilla de landing animada (React + Tailwind + GSAP) | "Crea la landing de [cliente] con la plantilla gsap-awwwards-website" (se crea en `sites/<cliente>`) |
| `landing-page-optimizer` | Hero, CTAs, CTA fijo en celular, GA4, SEO | "Optimiza los CTAs de esta landing para convertir más" |
| `responsive-craft` | Celular / tablet / laptop / escritorio | `/responsive-craft preview` para ver los 4 tamaños lado a lado; `/responsive-craft audit` para corregir |

Combo recomendado para cada sitio de cliente:
1. `ui-ux-pro-max` → estilo y paleta
2. `gsap-*` → animaciones
3. `landing-page-optimizer` → CTA visible en el hero + botón fijo de WhatsApp/Agendar en celular
4. `responsive-craft audit` → que se vea perfecto en todos los tamaños

Fuentes: greensock/gsap-skills (MIT), eng0ai/eng0-template-skills, onewave-ai/claude-skills, kylezantos/responsive-craft.
