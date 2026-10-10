#!/usr/bin/env python3
"""Reconstruit `index.html` (page autonome) à partir de `src/`.

Usage :  python3 build.py

Bibliothèque standard uniquement : aucune dépendance à installer.

Ce que fait le script :
  1. lit `src/template.html` (markup + composant) et `src/styles.css` ;
  2. empaquette les assets (logos, runtime DC, React) dans un manifest
     base64/gzip lu par `src/bootstrap.js` ;
  3. pré-rend le contenu critique (hero, fonctionnalités, prérequis…) en HTML
     statique dans le <body>, pour un affichage et un SEO immédiats sans JS ;
  4. écrit le tout dans `index.html`.
"""
import base64
import gzip
import html
import json
import re
import urllib.parse
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
SITE_URL = "https://omneria.github.io/Omneria-landing/"
FALLBACK_URL = "https://github.com/Omneria/ALlauncher/releases/latest/download/AL.Launcher.exe"

# (nom, fichier, mime, gzip, URL externe remplacée par l'asset, le cas échéant)
ASSETS = [
    ("logo-omneria", "assets/logo-omneria.webp", "image/webp", False, None),
    ("logo-astral-nexus", "assets/logo-astral-nexus.webp", "image/webp", False, None),
    ("dc-runtime", "assets/vendor/dc-runtime.js", "text/javascript", True, None),
    ("react", "assets/vendor/react.production.min.js", "text/javascript", True,
     "https://unpkg.com/react@18.3.1/umd/react.production.min.js"),
    ("react-dom", "assets/vendor/react-dom.production.min.js", "text/javascript", True,
     "https://unpkg.com/react-dom@18.3.1/umd/react-dom.production.min.js"),
]

# Polices embarquées dans le shell (sous-ensemble latin uniquement ; polices variables
# pour Inter et JetBrains Mono, d'où les plages de graisses).
FONTS = [
    ("Chakra Petch", "600", "assets/fonts/chakra-petch-600.woff2"),
    ("Chakra Petch", "700", "assets/fonts/chakra-petch-700.woff2"),
    ("Inter", "100 900", "assets/fonts/inter-variable.woff2"),
    ("JetBrains Mono", "100 800", "assets/fonts/jetbrains-mono-variable.woff2"),
]

FAVICON_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
    '<polygon points="10,4 60,4 60,54 54,60 4,60 4,10" fill="#00E5C7"/>'
    '<text x="32" y="41" font-family="monospace" font-weight="700" font-size="24" '
    'text-anchor="middle" fill="#06080F">OG</text></svg>'
)


def read(path):
    return (SRC / path).read_text(encoding="utf-8")


def asset_id(name):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "omneria-landing/" + name))


def data_uri(path, mime):
    return "data:%s;base64,%s" % (mime, base64.b64encode((SRC / path).read_bytes()).decode())


# ── Pré-rendu statique (sous-ensemble du DSL <sc-if>/<sc-for>/{{ }}) ──────────

def resolve(expr, scope):
    expr = expr.strip()
    if expr.startswith("!"):
        return not resolve(expr[1:], scope)
    if expr in ("true", "false"):
        return expr == "true"
    cur = scope
    for part in expr.split("."):
        cur = cur.get(part) if isinstance(cur, dict) else None
    return cur


def interpolate(text, scope):
    def sub(m):
        v = resolve(m.group(1), scope)
        if isinstance(v, bool):
            v = "true" if v else "false"
        return html.escape("" if v is None else str(v), quote=True)
    return re.sub(r"\{\{(.+?)\}\}", sub, text)


def attr(attrs, name):
    m = re.search(r'\b%s="\{\{(.+?)\}\}"' % name, attrs)
    return m.group(1) if m else None


def expand(src, scope):
    open_re = re.compile(r"<(sc-for|sc-if)\b([^>]*)>")
    tag_re = re.compile(r"<(/?)(sc-for|sc-if)\b[^>]*>")
    out, pos = [], 0
    while True:
        m = open_re.search(src, pos)
        if not m:
            out.append(interpolate(src[pos:], scope))
            return "".join(out)
        out.append(interpolate(src[pos:m.start()], scope))
        depth, i = 1, m.end()
        while depth:
            t = tag_re.search(src, i)
            depth += -1 if t.group(1) else 1
            i = t.end()
        inner = src[m.end():t.start()]
        if m.group(1) == "sc-if":
            if resolve(attr(m.group(2), "value"), scope):
                out.append(expand(inner, scope))
        else:
            name = re.search(r'\bas="([^"]+)"', m.group(2)).group(1)
            for item in resolve(attr(m.group(2), "list"), scope) or []:
                out.append(expand(inner, dict(scope, **{name: item})))
        pos = t.end()


def prerender(template, content):
    page = re.search(r"<x-dc>(.*)</x-dc>", template, re.S).group(1)
    page = re.sub(r"<helmet>.*?</helmet>", "", page, flags=re.S)
    # État initial du composant (avant réponse des API) : chargement en cours.
    scope = {
        "showHalos": True, "downloadUrl": FALLBACK_URL,
        "versionLabel": "Dernière version", "versionShort": "",
        "assetMeta": "Windows 10/11 · ~65 Mo · .exe",
        "features": content["features"], "requirements": content["requirements"],
        "statusLabel": "VÉRIFICATION…", "statusClass": "is-unknown", "playersLabel": "–/8",
        "relLoading": True, "relDone": False, "relError": False, "relEmpty": False,
        "skeletonRows": [1, 2, 3], "releases": [], "copyLabel": "COPIER",
        "navClass": "", "navExpanded": False, "stickyClass": "",
    }
    out = expand(page, scope)
    out = re.sub(r'\s(?:style-[a-z]+|hint-[a-z-]+|on[a-z]+)="[^"]*"', "", out)
    for name, path, mime, _, _ in ASSETS:
        if mime.startswith("image/"):
            out = out.replace("%%asset:" + name + "%%", data_uri(path, mime))
    return out


# ── Assemblage ────────────────────────────────────────────────────────────────

def build():
    content = json.loads(read("content.json"))
    styles = read("styles.css").strip()
    meta = (read("meta.html")
            .replace("%%SITE_URL%%", SITE_URL)
            .replace("%%FAVICON%%", "data:image/svg+xml," + urllib.parse.quote(FAVICON_SVG, safe="")))

    template = (read("template.html")
                .replace("%%META%%", meta)
                .replace("%%STYLES%%", styles)
                .replace("%%CONTENT%%", json.dumps(content, ensure_ascii=False)))
    shell_page = prerender(template, content)
    for name, *_ in ASSETS:
        template = template.replace("%%asset:" + name + "%%", asset_id(name))
    left = re.findall(r"%%[A-Za-z:_-]+%%", template + shell_page)
    if left:
        raise SystemExit("Marqueurs non résolus : %s" % sorted(set(left)))

    manifest, ext = {}, []
    for name, path, mime, compress, ext_url in ASSETS:
        raw = (SRC / path).read_bytes()
        if compress:
            raw = gzip.compress(raw, 9, mtime=0)
        manifest[asset_id(name)] = {"mime": mime, "compressed": compress,
                                    "data": base64.b64encode(raw).decode()}
        if ext_url:
            ext.append({"id": ext_url, "uuid": asset_id(name)})

    # `</` et `<!--` neutralisés pour ne pas fermer/échapper le <script> porteur.
    def js_json(obj):
        return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\u002F").replace("<!--", "<\\u0021--")

    fonts_css = "".join(
        "@font-face{font-family:'%s';font-style:normal;font-weight:%s;font-display:swap;"
        "src:url(%s) format('woff2')}\n" % (family, weight, data_uri(path, "font/woff2"))
        for family, weight, path in FONTS)

    out = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{meta}
<style id="shell-fonts">
{fonts}</style>
<style>
{styles}
</style>
</head>
<body>
{page}
<script>
{bootstrap}
</script>
<script type="__bundler/manifest">
{manifest}
</script>
<script type="__bundler/ext_resources">
{ext}
</script>
<script type="__bundler/page_order">
[]
</script>
<script type="__bundler/template">
{template}
</script>
</body>
</html>
""".format(meta=meta, fonts=fonts_css, styles=styles, page=shell_page,
           bootstrap=read("bootstrap.js").strip(), manifest=js_json(manifest),
           ext=js_json(ext), template=js_json(template))

    (ROOT / "index.html").write_text(out, encoding="utf-8")
    print("index.html : %.0f Ko" % (len(out.encode("utf-8")) / 1024))


if __name__ == "__main__":
    build()
