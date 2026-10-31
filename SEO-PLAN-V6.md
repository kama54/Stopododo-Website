# Stopododo — stratégie SEO V6 (prépublication)

Date de préparation : 31 octobre 2026. Ce document n'implique aucune mise en ligne.

## Objectif

Faire découvrir Stopododo à des internautes qui ne connaissent pas encore son nom, via leurs problèmes concrets sur smartphone ou tablette Android : écran trop lumineux, minuterie, son, pause des vidéos compatibles. Ne pas promettre de compatibilité Android TV ou d'arrêt de tous les lecteurs.

## Pages livrées

- 10 pages d'accueil localisées déjà présentes en V5 ; textes, vidéos et visuels préservés.
- 10 nouvelles pages de lecture de vidéo (une par langue), chacune avec un MP4 d'origine et une miniature issue du film.
- 3 guides français approfondis : assombrissement, minuterie sommeil, vidéo automatique.
- `sitemap.xml`, `video-sitemap.xml`, `robots.txt` et balises hreflang vidéo.
- Préchargement adapté à la taille de l'écran ; lien direct à la page vidéo dans chaque page d'accueil.

## Priorités des requêtes (hypothèses, non statistiques)

| Cible | Mots-clés à tester | Page |
| --- | --- | --- |
| Luminosité trop forte | écran Android trop lumineux, assombrir écran Android, luminosité sous minimum | /fr/assombrir-ecran-android.html |
| Timer | minuteur sommeil Android, minuterie arrêt son | /fr/minuteur-sommeil-android.html |
| Vidéos | arrêter vidéo automatiquement, minuterie pause vidéo | /fr/arreter-video-automatiquement.html |
| Découverte | Stopododo vidéo, filtre écran Android | /fr/video-stopododo.html et accueil |

Ne pas présenter ces expressions comme un classement Google Trends ou Google Ads : nous n'avons pas de volumes de recherches, de CPC ni de scores de concurrence extraits d'un compte.

## À mesurer avec Google Trends

1. Pays = France ; catégorie = Toutes ; recherche Web ; période = 12 mois puis 5 ans.
2. Comparer « luminosité écran Android », « minuteur sommeil », « filtre écran », « filtre lumière bleue » ; retester leurs variantes exactes et leurs sujets associés.
3. Répéter pour les marchés prioritaires : Allemagne, Espagne, États-Unis/Royaume-Uni, Brésil, etc.
4. Ne pas assimiler l'indice relatif 0–100 de Trends à un volume de recherches.

## À mesurer avec Google Ads Keyword Planner

1. Dans un compte configuré, choisir « Découvrir de nouveaux mots-clés ».
2. Coller les expressions du CSV joint par pays et par langue.
3. Exporter estimations de recherche mensuelle, concurrence annonceurs, fourchettes d'enchères.
4. Privilégier intention et pertinence avant volume. Aucun achat de publicité nécessaire pour cette étape ; ne lancer de campagne qu'après mesure de la conversion en installation et achats.

## Avant une publication réelle

1. **Préserver les pages légales** et ne pas écraser `confidentialite.html`, `accessibilite.html`, `conditions.html`, `contact.html` du site existant ; reprendre les versions traduites déjà présentes dans `redesign-immersive-seo`. Le paquet V6 n'inclut pas les textes légaux.
2. Confirmer les droits d'utilisation commerciale des **enregistrements** musicaux des vidéos (la composition de Chopin et un enregistrement particulier sont deux objets de droits distincts).
3. Remplacer l'adresse canonique de base si le domaine est personnalisé (`BASE` dans `tools/build.py` et `tools/build_seo_v6.py`), puis régénérer. La base actuelle reste `https://kama54.github.io/Stopododo-Website`.
4. Ajouter `STOPODODO_VIDEO_PUBLICATION_DATE` au moment de la **première publication effective** des vidéos et régénérer le JSON-LD VideoObject. Exemple de commande **uniquement le jour de la publication** : `STOPODODO_VIDEO_PUBLICATION_DATE=AAAA-MM-JJTHH:MM:SS+01:00 python tools/build_seo_v6.py`. Ne pas inventer cette date. Google exige `uploadDate` pour certaines améliorations Video rich results ; elle est volontairement absente du brouillon.
5. Confirmer le lien Play Store public avant de rendre le badge « Get it on Google Play » cliquable.
6. Vérifier les pages à différentes largeurs, la lecture et le plein écran dans un navigateur normal. Les captures de contrôle V6 utilisent une injection HTML hors réseau ; elles ne constituent pas un test de lecture vidéo.
7. Publier uniquement après autorisation explicite ; conserver les liens et pages légales fournis dans Google Play Console.
8. Ajouter et soumettre les sitemaps à Search Console après publication. Mesurer impressions, clics, CTR et pages indexées sans garantir un classement.

## Technique

Reconstruction locale (requiert Jinja2, ffmpeg/ffprobe pour les miniatures nouvelles) :

```sh
python tools/build.py
python tools/build_seo_v6.py
python tools/check_seo_v6.py
```

Pour tester la navigation, utiliser un serveur local (ne pas ouvrir uniquement les fichiers via `file://`) :

```sh
python -m http.server 8000
# puis http://localhost:8000/fr/index.html
```

## Références documentaires publiques

- Google Search Central : https://developers.google.com/search/docs/appearance/video
- Données structurées vidéo : https://developers.google.com/search/docs/appearance/structured-data/video
- Sitemaps : https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- Versions localisées : https://developers.google.com/search/docs/specialty/international/localized-versions
- Google Ads Keyword Planner : https://support.google.com/google-ads/answer/7337243?hl=fr
- Android Extra Dim : https://support.google.com/accessibility/android/answer/11183305?hl=fr
