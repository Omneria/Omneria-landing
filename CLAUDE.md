# CLAUDE.md

Contexte pour Claude Code sur ce repo — le lire évite de ré-explorer le repo
à chaque session.

## Ce que c'est

Landing page statique du launcher **Omnéria Games Launcher** (serveur Minecraft
**Astral Nexus**, Omneria Games).

- `index.html` : page unique et **autonome** (~0,4 Mo), **générée** par
  `python3 build.py` à partir de `src/`. Ne pas l'éditer à la main.
- `src/` : sources éditables.
  - `template.html` : markup + composant (format DC : `<sc-if>`, `<sc-for>`,
    `{{ }}`, classe `Component extends DCLogic` en fin de fichier).
  - `styles.css` : CSS partagé (shell pré-rendu + template).
  - `content.json` : fonctionnalités et prérequis (texte unique, utilisé par le
    composant ET par le pré-rendu statique).
  - `meta.html` : title, description, Open Graph, favicon, JSON-LD.
  - `bootstrap.js` : décompresse le bundle et remplace le document (patché pour
    conserver les polices du shell).
  - `assets/` : logos WebP, polices latin (woff2), runtime DC et React.
- `build.py` : assemble le tout (stdlib Python uniquement, pas de dépendances).
  Les assets sont embarqués en base64/gzip ; le contenu critique est pré-rendu
  en HTML statique dans le `<body>` (affichage immédiat, SEO, sans JS).
- `og-image.png` : image de partage (1200×630), seul fichier publié à côté de
  `index.html` (les crawlers sociaux ne lisent pas les data URI).
- `.github/workflows/deploy-pages.yml` : copie `index.html` + `og-image.png`
  dans `_site/` et déploie sur GitHub Pages à chaque push sur `main`.
- `README.md` / `CONTRIBUTING.md` : docs utilisateur/contributeur.
- `LICENSE` : propriétaire, tous droits réservés (Omneria Games).

## Repo

- Remote : `Omneria/Omneria-landing`
- Branche par défaut : `main`
- Site publié : https://omneria.github.io/Omneria-landing/
- Réglage GitHub Pages : Settings → Pages → Source = "GitHub Actions" (déjà fait)

## Points importants

- Workflow : modifier `src/`, lancer `python3 build.py`, **committer `src/` ET
  `index.html`** (le déploiement publie `index.html` tel quel, il ne rebuild pas).
- Pas de lint/tests. Prévisualiser : ouvrir `index.html` ou `python3 -m http.server`.
- Runtime : le composant appelle l'API GitHub Releases (`Omneria/ALlauncher`) et
  `api.mcsrvstat.us` ; réponses mises en cache dans `sessionStorage`.
- Pas de section captures/screenshots (supprimée) ; `<image-slot>` n'est plus utilisé.
- Ne pas casser le caractère autonome : pas d'assets externes référencés en dur
  (hors `og-image.png` et les APIs ci-dessus).
- Un nouvel export du bundle depuis l'outil de design écraserait ces sources :
  reporter les changements dans `src/template.html` plutôt que remplacer `index.html`.
