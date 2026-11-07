# FNAN — National Festival of Digital Art

Site statique du festival (19–22 novembre 2026, Alger). Pages : accueil (hero KV), About, Programme, Artists, Speakers, Visit. Anglais uniquement.

## Modifier le contenu
Le contenu et les gabarits sont dans `build.py` ; ne pas éditer les `.html` générés.

```bash
python3 build.py        # régénère index.html, about.html, programme.html, artists.html, speakers.html, visit.html
python3 -m http.server  # aperçu sur http://localhost:8000
```

## Vidéo du KV
Le hero utilise `assets/kv.webp` (placeholder). Pour passer à la vidéo animée, déposer `assets/kv.mp4`
au même cadrage vertical 2:3 que l'image : elle prend automatiquement le relais (fondu), sans autre changement.

## À remplacer
- Logos FNAN et Ministère de la Culture (pastilles pointillées « Logo … »).
- Liens Instagram / Facebook / Contact / Politique de confidentialité / Mentions légales (`#` pour l'instant).
- Profils artistes et intervenants (cartes « Profile coming soon »).

Déploiement : Vercel (`vercel.json`, URLs propres), à chaque push.
