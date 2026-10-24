---
name: gsap-awwwards-website
description: SPYLT product landing with GSAP scroll animations, React 19, and Tailwind CSS 4.
---

# GSAP Awwwards Website

A stunning product landing page with GSAP scroll animations, modern React 19 architecture, and Tailwind CSS 4 styling.

## Tech Stack

- **Framework**: React 19
- **Build Tool**: Vite
- **Animation**: GSAP
- **Styling**: Tailwind CSS 4
- **Package Manager**: npm
- **Output**: `dist` directory
- **Dev Port**: 5173

## Setup

### 1. Clone the Template (always into a NEW subfolder)

> Never clone into the repo root and never delete any `.git` folder. Ask the user for a project name (e.g. the client name) and use `sites/<project-name>`.

```bash
mkdir -p sites
git clone --depth 1 https://github.com/Eng0AI/gsap-awwwards-website-template.git sites/<project-name>
rm -rf sites/<project-name>/.git   # only the template's own history, inside the new subfolder
cd sites/<project-name>
```

### 2. Adapt to the client

Replace the demo product (SPYLT) content, colors and images with the client's brand before building.

### 3. Install Dependencies

```bash
npm install
```

## Build

```bash
npm run build
```

Creates a production build in the `dist/` directory.

## Deploy

> **CRITICAL**: For Vercel, you MUST use `vercel build --prod` then `vercel deploy --prebuilt --prod`. Never use `vercel --prod` directly.

### Vercel (Recommended)

```bash
vercel pull --yes -t $VERCEL_TOKEN
vercel build --prod -t $VERCEL_TOKEN
vercel deploy --prebuilt --prod --yes -t $VERCEL_TOKEN
```

### Netlify

```bash
netlify deploy --prod --dir=dist
```

## Development

```bash
npm run dev
```

Opens at http://localhost:5173

## Notes

- Static React site - no environment variables needed
- Never run `npm run dev` in VM environment
