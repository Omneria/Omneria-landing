# Omneria Games — Astral Nexus (Landing Page)

Landing page statique du jeu **Astral Nexus** par Omneria Games.

## Structure du repo

```
.
├── index.html          # Page unique, autonome (GÉNÉRÉE par build.py)
├── og-image.png        # Image de partage (Open Graph)
├── build.py            # Reconstruit index.html depuis src/
├── src/                # Sources : template, styles, contenu, assets
└── .github/workflows/
    └── deploy-pages.yml  # Déploiement automatique sur GitHub Pages
```

`index.html` est un fichier unique et autonome : styles, scripts, polices et
images sont embarqués. Il se régénère avec `python3 build.py` (Python 3
standard, aucune dépendance).

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

1. Modifier les fichiers de `src/` (voir `CONTRIBUTING.md`).
2. Lancer `python3 build.py` pour régénérer `index.html`.
3. Committer `src/` et `index.html`, puis ouvrir une pull request vers `main`.
4. Une fois mergée, le déploiement se déclenche automatiquement.
