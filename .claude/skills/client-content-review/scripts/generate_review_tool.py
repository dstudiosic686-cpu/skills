#!/usr/bin/env python3
"""
Generate a self-contained, offline HTML "content review" tool for a client.

Given a JSON list of content fields (text/textarea/image) pulled from a
website's real pages, this produces ONE .html file the client can open in
any browser with no login and no internet dependency: every text field is
editable inline, every image has a "Cambiar imagen" button that swaps it
in via the browser's normal file picker (base64-embedded, no server
needed), and a "Guardar cambios y descargar" button re-downloads the same
file with the client's edits baked in (and highlighted), so it can be
opened again later and read directly.

Usage:
    python3 generate_review_tool.py \
        --fields fields.json \
        --output revision-cliente-ACME.html \
        --client-name "ACME Corp" \
        --logo path/to/logo.png \
        --file-prefix ACME

fields.json format — a JSON array of objects:
    {"id": "hero_title", "section": "1. Inicio", "label": "Título principal", "type": "text", "value": "..."}
    {"id": "hero_sub",   "section": "1. Inicio", "label": "Subtítulo",        "type": "textarea", "value": "..."}
    {"id": "hero_img",   "section": "1. Inicio", "label": "Foto del hero",    "type": "image", "value": "https://.../foto.jpg"}

- "id": unique, stable key (letters/numbers/underscore) — this is what you'll
  look for again in the returned file to know which field changed.
- "section": groups fields visually, in the order they first appear in the list.
- "type": "text" (single line), "textarea" (paragraph), or "image" (URL or local
  path to the CURRENT image — for local paths, this script embeds them as
  base64 automatically so the file stays self-contained).
- "value": the current live copy — this becomes both the pre-filled field
  and the baseline the tool diffs the client's edits against.

Do NOT include "original" or "changed" keys — this script adds them.
"""
import argparse
import base64
import json
import mimetypes
import os
import re
import sys
import urllib.parse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(os.path.dirname(SCRIPT_DIR), "assets", "template.html")

ALLOWED_TYPES = {"text", "textarea", "image"}
ID_RE = re.compile(r"^[a-zA-Z0-9_]+$")


def load_fields(path):
    with open(path, encoding="utf-8") as f:
        fields = json.load(f)
    if not isinstance(fields, list) or not fields:
        sys.exit("fields.json must be a non-empty JSON array of field objects.")

    seen_ids = set()
    for i, f in enumerate(fields):
        for key in ("id", "section", "label", "type", "value"):
            if key not in f:
                sys.exit(f"Field #{i} is missing required key '{key}': {f}")
        if not ID_RE.match(f["id"]):
            sys.exit(f"Field id '{f['id']}' must be letters/numbers/underscore only.")
        if f["id"] in seen_ids:
            sys.exit(f"Duplicate field id: '{f['id']}'")
        seen_ids.add(f["id"])
        if f["type"] not in ALLOWED_TYPES:
            sys.exit(f"Field '{f['id']}' has invalid type '{f['type']}' (must be text/textarea/image)")
        # Normalize: the tool tracks "original" (to diff against) and
        # "changed" (images only, since a re-typed-then-reverted text
        # field should NOT count as changed, but a swapped image always
        # should — there's no cheap way to diff binary content).
        f["original"] = f["value"]
        f["changed"] = False
        if f["type"] == "image":
            f["value"] = resolve_image(f["value"], f["id"])
            f["original"] = f["value"]
    return fields


def resolve_image(value, field_id):
    """Local paths get embedded as base64 so the tool stays self-contained
    offline; remote http(s) URLs are left as-is (lighter file, and the
    client will have internet when opening it)."""
    if value.startswith(("http://", "https://", "data:")):
        return value
    if not os.path.isfile(value):
        print(f"WARNING: image path for '{field_id}' not found on disk: {value} "
              f"— leaving value as-is (will be a broken image if it isn't a real URL).",
              file=sys.stderr)
        return value
    return to_data_uri(value)


def to_data_uri(path):
    mime, _ = mimetypes.guess_type(path)
    mime = mime or "application/octet-stream"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def resolve_logo(logo_arg):
    if not logo_arg:
        # Tiny neutral placeholder (a filled circle) so the header always
        # has something to show instead of a broken image icon.
        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40">'
            '<circle cx="20" cy="20" r="20" fill="%230047d4"/></svg>'
        )
        return "data:image/svg+xml," + urllib.parse.quote(svg)
    if logo_arg.startswith(("http://", "https://", "data:")):
        return logo_arg
    if not os.path.isfile(logo_arg):
        sys.exit(f"--logo path not found: {logo_arg}")
    return to_data_uri(logo_arg)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fields", required=True, help="Path to fields.json")
    ap.add_argument("--output", required=True, help="Path to write the generated .html review tool")
    ap.add_argument("--client-name", required=True, help='e.g. "ACME Corp" — used in the page title, alt text and footer')
    ap.add_argument("--logo", default=None, help="Path or URL to the client's logo (optional; embedded as base64 if it's a local file)")
    ap.add_argument("--file-prefix", default=None, help="Prefix for the downloaded filename (default: derived from --client-name)")
    ap.add_argument("--intro-text", default=None, help="Override the intro paragraph under the title")
    args = ap.parse_args()

    fields = load_fields(args.fields)
    logo_uri = resolve_logo(args.logo)

    file_prefix = args.file_prefix or re.sub(r"[^a-zA-Z0-9]+", "-", args.client_name).strip("-") or "revision"
    page_title = f"Revisión de Contenido — Sitio Web {args.client_name}"
    intro_text = args.intro_text or (
        "Este documento reúne todos los textos e imágenes que tendrá el sitio web. "
        "Revísalo con calma y haz los cambios directo aquí."
    )

    with open(TEMPLATE_PATH, encoding="utf-8") as f:
        template = f.read()

    out = (
        template
        .replace("__LOGO_DATA_URI__", logo_uri)
        .replace("__CLIENT_NAME__", args.client_name)
        .replace("__PAGE_TITLE__", page_title)
        .replace("__INTRO_TEXT__", intro_text)
        .replace("__FILE_PREFIX__", file_prefix)
        .replace("__FIELDS_JSON__", json.dumps(fields, ensure_ascii=False))
    )

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(out)

    n_text = sum(1 for f in fields if f["type"] == "text")
    n_textarea = sum(1 for f in fields if f["type"] == "textarea")
    n_image = sum(1 for f in fields if f["type"] == "image")
    print(f"Wrote {args.output}")
    print(f"  {len(fields)} fields total — {n_text} text, {n_textarea} textarea, {n_image} image")
    print(f"  {len(set(f['section'] for f in fields))} sections")


if __name__ == "__main__":
    main()
