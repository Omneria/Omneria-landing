# Omneria Games — Astral Nexus (Landing Page)

Landing page statique du jeu **Astral Nexus** par Omneria Games.

## Structure du repo

```
.
├── index.html                      # Page unique, autonome (assets embarqués)
└── .github/workflows/
    └── deploy-pages.yml            # Déploiement automatique sur GitHub Pages
```

Le site est un fichier `index.html` unique et autonome : toutes les ressources
(styles, scripts, polices, images) sont embarquées directement dans le fichier.
Il n'y a pas d'étape de build ni de dépendances à installer.

## Prévisualiser en local

Aucune installation n'est nécessaire. Il suffit d'ouvrir le fichier directement
dans un navigateur, ou de servir le dossier avec un petit serveur HTTP :

```bash
python3 -m http.server 8000
# puis ouvrir http://localhost:8000
```

## Déploiement

Le site est déployé automatiquement sur **GitHub Pages** à chaque push sur la
branche `main`, via le workflow `.github/workflows/deploy-pages.yml`
(`actions/upload-pages-artifact` + `actions/deploy-pages`).

Il peut aussi être déclenché manuellement depuis l'onglet **Actions** du repo
(`workflow_dispatch`).

Réglage nécessaire une seule fois côté repo GitHub :
**Settings → Pages → Source = "GitHub Actions"**.

URL du site publié : https://omneria.github.io/Omneria-landing/

## Mettre à jour le site

1. Remplacer `index.html` par la nouvelle version.
2. Ouvrir une pull request vers `main`.
3. Une fois mergée, le déploiement se déclenche automatiquement.
