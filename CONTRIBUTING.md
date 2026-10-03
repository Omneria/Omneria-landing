# Contribuer

Le site est un unique `index.html` autonome, **généré** depuis `src/` par un
script Python sans dépendances.

## Workflow

1. Créer une branche à partir de `main`.
2. Modifier les sources dans `src/` :
   - `template.html` : structure, composant et logique ;
   - `styles.css` : styles partagés ;
   - `content.json` : fonctionnalités et prérequis ;
   - `meta.html` : SEO / Open Graph.
3. Lancer `python3 build.py` pour régénérer `index.html`.
4. Vérifier localement en ouvrant `index.html` (voir le
   [README](README.md#prévisualiser-en-local)), y compris en mobile (≤ 720 px).
5. Committer `src/` **et** `index.html`, puis ouvrir une pull request vers `main`.
6. Après le merge, le déploiement sur GitHub Pages est automatique.

## Bonnes pratiques

- Ne pas éditer `index.html` à la main : il serait écrasé au prochain build.
- Rester autonome : pas de dépendance externe non embarquée.
- Accessibilité : garder le focus clavier visible, des textes ≥ 12 px et
  respecter `prefers-reduced-motion` pour toute animation.
- Garder les commits et PR ciblés.
