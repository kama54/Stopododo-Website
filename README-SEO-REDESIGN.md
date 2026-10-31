# Refonte Stopododo — prépublication

## Contenu
- 10 versions linguistiques réellement pré-rendues en HTML statique dans /fr/, /en/, /es/, /it/, /de/, /nl/, /pt/, /ar/, /ja/ et /ko/.
- 5 pages par langue : accueil, confidentialité, conditions, accessibilité et contact.
- Design immersif responsive sans JavaScript obligatoire. SVG d'ambiance nocturne original.
- Liens hreflang réciproques, URL canoniques, meta descriptions et titres par langue/page, sitemap, robots.txt, données structurées SoftwareApplication sur chaque accueil.
- Maintien des pages légales historiques à la racine pour ne pas casser les URL déjà fournies à Google Play.
- La racine index.html devient une page française avec canonical /fr/index.html; les URL de sous-dossiers sont canoniques.

## À compléter avant la mise en ligne publique
1. Le visuel Play Store original est désormais intégré sous une version WebP optimisée (380 × 186, ~3 Ko) à côté de l'illustration SVG nocturne. Ajouter ensuite les captures réelles de l'application et, pour la haute résolution, les visuels finalisés dans chaque langue.
2. Confirmer le lien officiel exact de la fiche Play Store après lancement. Ne pas mettre un lien inventé; un badge « publication à venir » est affiché.
3. Vérifier visuellement les 10 langues sur mobile (en particulier arabe RTL), les 50 pages et tous les liens.
4. Vérifier la conformité juridique du contenu de confidentialité/conditions existant avant publication.
5. Contrôler GitHub Pages dans Paramètres > Pages et soumettre sitemap.xml à Google Search Console après la mise en ligne.

## Déploiement
Cette refonte doit être fusionnée sur main uniquement après validation humaine explicite. Ne pas modifier ou retirer les anciens liens légaux de Google Play Console.
