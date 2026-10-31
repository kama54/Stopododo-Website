# Stopododo V6 SEO — intégration en attente du ZIP

Cette branche `integration-v6-seo` part de `redesign-immersive-seo`.
Elle **n'est pas publiée** et ne modifie pas `main`.

## Procédure dans GitHub Codespaces

1. Ouvrir un Codespace sur la branche `integration-v6-seo`.
2. Glisser dans l'explorateur de fichiers le ZIP validé `Stopododo_Site_V6_SEO_10_Langues.zip`, à la racine du projet, **sans l'extraire avant**.
3. Exécuter à la racine du dépôt :
   ```bash
   python3 scripts/import_v6.py Stopododo_Site_V6_SEO_10_Langues.zip --push
   ```
4. Contrôler les fichiers mis à jour sur cette branche. Ne fusionner vers `main` qu'après validation explicite.

Le script refuse de s'exécuter sur `main`, vérifie les pages et médias, refuse les chemins dangereux, conserve les 44 pages légales déjà présentes et pousse seulement vers `integration-v6-seo`.

## Checklist avant une publication ultérieure
- Vérifier la lecture et le plein écran des 10 vidéos dans un navigateur réel
- Contrôler l'affichage mobile et RTL arabe
- Vérifier la politique de confidentialité et les liens légaux historiques
- Ajouter l'URL officielle de Google Play une fois disponible
- Vérifier les droits de diffusion des enregistrements musicaux des vidéos
- Choisir l'URL canonique définitive avant de soumettre le sitemap
- Ne pas inventer de date de publication vidéo dans `VideoObject`
