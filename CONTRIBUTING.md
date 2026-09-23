# Contribuer

Ce repo est volontairement minimal : un unique fichier `index.html` autonome,
sans build ni dépendances.

## Workflow

1. Créer une branche à partir de `main`.
2. Modifier `index.html` (ou régénérer/exporter la nouvelle version du bundle).
3. Vérifier localement en ouvrant le fichier dans un navigateur (voir le
   [README](README.md#prévisualiser-en-local)).
4. Ouvrir une pull request vers `main`.
5. Après le merge, le déploiement sur GitHub Pages se fait automatiquement
   (voir `.github/workflows/deploy-pages.yml`).

## Bonnes pratiques

- Ne pas casser la structure autonome du fichier (pas de dépendances externes
  non embarquées) : le site doit continuer à fonctionner sans build.
- Garder les commits et PR ciblés sur le contenu du site ou le pipeline de
  déploiement.
