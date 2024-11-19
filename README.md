Égaliseur Numérique - README

Description

Ce projet implémente un égaliseur numérique basé sur cinq filtres passe-bande pour modifier le spectre d'un signal audio. Chaque filtre cible une fréquence spécifique :

1000 Hz
3000 Hz
5000 Hz
7000 Hz
9000 Hz
L'objectif est d'offrir un contrôle précis sur ces bandes de fréquence en ajustant leurs gains respectifs.



Fonctionnalités

Application de cinq filtres passe-bande sur un fichier audio.
Visualisation et analyse des réponses impulsionnelles de chaque filtre.
Interface utilisateur simple pour ajuster les gains.


Algorithme
Initialisation des filtres

Les filtres passe-bande pour les fréquences cibles (1000 Hz, 3000 Hz, 5000 Hz, 7000 Hz, 9000 Hz) sont prédéfinis mais modifiables.

Chargement du fichier audio

L'utilisateur importe un fichier .wav via l'interface graphique.

Interface utilisateur

Des sliders permettent de modifier les paramètres des filtres (par exemple, le gain ou la bande passante).
Les sliders sont liés en temps réel aux coefficients des filtres.

Traitement audio en temps réel

Le signal audio est segmenté pour être traité par blocs.
Chaque bloc passe par les cinq filtres ajustés selon les réglages des sliders.
Les blocs filtrés sont recombinés et diffusés.

Visualisation

Le fichier audio modifié peut être écouté en direct

Réponse impulsionnelle
Une réponse impulsionnelle (RI) représente la réaction d'un filtre à une impulsion unitaire. Voici les RI des filtres :

Vous pouvez trouvé les réponses impulsionnelles dans le fichier 02-filtrageEx selon quel fréquence vous voulez utilisé en modifiant les valeurs définies.
