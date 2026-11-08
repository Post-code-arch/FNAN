# FNAN — National Cultural Festival of Plastic and Visual Arts (Digital Edition)

Site statique du festival (19–22 novembre 2026, Alger). Pages : accueil (hero KV), About, Programme, Artists, Experts, Visit, Press & Media. Anglais uniquement.

## Modifier le contenu
Le contenu et les gabarits sont dans `build.py` ; ne pas éditer les `.html` générés.

```bash
python3 build.py        # régénère les 7 pages .html
python3 -m http.server  # aperçu sur http://localhost:8000
```

## Vidéo du KV
Le hero utilise `assets/kv.webp` (placeholder). Pour passer à la vidéo animée, déposer `assets/kv.mp4`
au même cadrage vertical 2:3 que l'image : elle prend automatiquement le relais (fondu), sans autre changement.

## Identité visuelle
Appliquée d'après `VISUAL_IDENTITY_FAN` : fond Noir #050403, texte Chaux #EFEBE3, accents Sable #D9A45F, Palmier #2E6A4B, Sauge #93B49C, Brique #B5382B ; Syne (titres et textes, sans italique) et Geist Mono (dates, lieux, libellés, capitales, interlettrage +18 %). Le logo (arche + ruban) est extrait du PDF en vectoriel puis détouré : `assets/logo-mark.webp` et `assets/logo-mark-small.webp` (dessin « petite taille », pour le header et le favicon). Le dégradé du ruban est réservé au logo et aux filets.

## À remplacer
- Logo du Ministère de la Culture (pastille pointillée « Logo M. Culture »).
- Liens Instagram / Facebook / Contact / Politique de confidentialité / Mentions légales (`#` pour l'instant).
- Profils artistes et intervenants (cartes « Profile coming soon »).

Déploiement : Vercel (`vercel.json`, URLs propres), à chaque push.

## Page Press & Media
Documents dans `assets/press/` (communiqué et dossier de presse en arabe, affiche officielle en JPG, vignettes). Pour les mettre à jour, remplacer les fichiers en gardant les mêmes noms.
