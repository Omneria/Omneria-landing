# CLAUDE.md

Contexte pour Claude Code sur ce repo — le lire évite de ré-explorer le repo
à chaque session.

## Ce que c'est

Landing page statique du jeu **Astral Nexus** (Omneria Games).

- `index.html` : page unique et **autonome** (~1,2 Mo). Tous les assets
  (CSS, JS, polices, images) sont embarqués inline/base64 dans ce fichier —
  export d'un bundler. Il n'y a **pas de source séparée**, pas de build,
  pas de `package.json`, pas de dépendances npm.
- `.github/workflows/deploy-pages.yml` : déploie automatiquement `index.html`
  (racine du repo) sur GitHub Pages à chaque push sur `main`.
- `README.md` / `CONTRIBUTING.md` : docs utilisateur/contributeur.
- `LICENSE` : propriétaire, tous droits réservés (Omneria Games).

## Repo

- Remote : `Omneria/Omneria-landing`
- Branche par défaut : `main`
- Site publié : https://omneria.github.io/Omneria-landing/
- Réglage GitHub Pages : Settings → Pages → Source = "GitHub Actions" (déjà fait)

## Points importants

- Pas de build à lancer, pas de lint/tests configurés. Pour prévisualiser :
  ouvrir `index.html` dans un navigateur ou `python3 -m http.server`.
- Toute modification du site consiste à remplacer `index.html` en entier
  (nouvel export du bundle), pas à l'éditer ligne par ligne à la main.
- Ne pas casser le caractère autonome du fichier (pas d'assets externes
  non embarqués référencés en dur).
- Après un merge sur `main`, le déploiement Pages est automatique — pas
  d'action manuelle nécessaire à part le réglage Pages déjà fait ci-dessus.
