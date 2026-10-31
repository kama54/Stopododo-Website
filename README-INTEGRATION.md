# Stopododo — V6 SEO de prépublication

Cette archive contient la V5 et ses corrections, plus un enrichissement SEO. **Elle n'a pas été envoyée sur GitHub et ne doit pas être publiée sans validation explicite.**

## Contenu

- 11 pages d'accueil (racine + FR/EN/ES/IT/DE/NL/PT/AR/JA/KO), V5 conservée avec lien supplémentaire vers les guides et pages vidéo.
- 10 vidéos intégrées (MP4 optimisés hérités de la V5) + 10 miniatures tirées des vrais films.
- 10 pages de lecture dédiées : `LANG/video-stopododo.html`.
- 3 nouveaux guides pratiques français : `fr/assombrir-ecran-android.html`, `fr/minuteur-sommeil-android.html` et `fr/arreter-video-automatiquement.html`.
- Feuilles CSS `styles-v3.css` et `seo-v6.css`, `robots.txt`, `sitemap.xml`, `video-sitemap.xml`.
- `SEO-PLAN-V6.md` : stratégie, limitations, liste de vérifications, références et suivi de résultats.
- `mots-cles-seo-a-valider.csv` : hypothèses pour Google Ads Keyword Planner, **sans faux volumes**.
- Build reproductible : `tools/build.py`, `tools/build_seo_v6.py`, `tools/check_seo_v6.py`.

## IMPORTANT : ne pas remplacer les pages légales existantes

La V6 est destinée à être intégrée sur la branche `redesign-immersive-seo` du dépôt `kama54/Stopododo-Website` **sans écraser** les documents légaux existants ni les pages légales multilingues présentes dans cette branche. Les liens légaux de la V6 ciblent les pages déjà connues du site. L'archive ne les embarque volontairement pas : les conserver à l'intégration.

## Avant publication : points incomplets

1. **URL Google Play** non confirmée : badge informatif non cliquable.
2. **Droits musicaux** : contrôler spécifiquement les droits des enregistrements dans les MP4.
3. **Date de première publication vidéo** inconnue : propriété `uploadDate` omise volontairement. Fournir une vraie date ISO 8601 à `STOPODODO_VIDEO_PUBLICATION_DATE` lors de la publication, puis régénérer les vidéos/JSON-LD.
4. **Domaine définitif** non arrêté : tous les canonical/sitemaps utilisent `https://kama54.github.io/Stopododo-Website`. Adapter si `gogostudio.com/stopododo` est retenu.
5. **Indexation** : aucune indexation ou performance Google n'est garantie ; connecter Search Console après publication.
6. **Contrôle navigateurs** : vérifier lecture vidéo, plein écran, 10 langues, orientation mobile et liens légaux avec une version intégrée du dépôt complet.

## Tests réalisés

- 24 pages HTML uniques analysées (11 accueils + 10 vidéos + 3 guides) ; une balise H1 par page, titres et méta descriptions présents.
- 10 fichiers MP4 et 10 vignettes contrôlés ; 2 sitemaps XML analysés.
- 27 URL canoniques listées au sitemap (10 accueils, 10 vidéos, 3 guides, 4 pages légales historiques).
- Préviews de la page guide contrôlés sur ordinateur et mobile via Chromium avec injection locale des styles et des images. Test de lecture vidéo non effectué.
- Javascript V5 vérifié (`node --check`).

Voir `SEO-PLAN-V6.md` pour toutes les étapes de finalisation.
