# SunshineCTF 2025 - Hail Mary Write-up

## Introduction

Le challenge "Hail Mary" nous demande d'aider le Dr. Ryland Grace à optimiser le code génétique de "taumoebas" pour assurer leur survie. Nous devons atteindre un taux de survie moyen de 95% en 100 générations.

## Connexion et Analyse

La première étape a été de se connecter au service distant via `nc chal.sunshinectf.games 25201`. Le serveur nous a accueilli avec un message expliquant les règles : nous devons soumettre des populations de 100 échantillons de gènes, chaque échantillon étant une liste de 10 floats (entre 0 et 1), le tout au format JSON.

## Développement du Solver

Face à un problème d'optimisation sans fonction de score connue, l'approche la plus adaptée est un algorithme génétique. J'ai donc développé un script Python en utilisant la librairie `pwntools` pour gérer la communication avec le serveur.

L'algorithme fonctionne comme suit :

1.  **Initialisation :** Une population de 100 individus est créée, chaque individu ayant 10 gènes (floats) initialisés aléatoirement entre 0 et 1.
2.  **Évaluation :** La population est envoyée au serveur, qui nous retourne le score de chaque individu.
3.  **Sélection :** Les 10 meilleurs individus (ceux avec les scores les plus élevés) sont sélectionnés pour être les "parents" de la génération suivante.
4.  **Reproduction (Mutation) :** Une nouvelle population de 100 individus est créée. Chaque nouvel individu est une copie d'un parent choisi au hasard, auquel on applique une légère mutation (ajout d'une petite valeur aléatoire à chaque gène).
5.  **Itération :** Le processus est répété pour 100 générations, ou jusqu'à ce que le flag soit obtenu.

## Capture du Flag

Le script a été lancé, et nous avons pu observer le score moyen de la population augmenter progressivement à chaque génération. Après 29 générations, le score a dépassé le seuil requis, et le serveur nous a renvoyé le flag au lieu du JSON habituel.

Le flag est : `sun{wh4t_4_gr34t_pr0j3ct}`

## Conclusion

Ce challenge était une excellente introduction aux algorithmes génétiques. En partant d'une population aléatoire et en appliquant des principes de sélection et de mutation, nous avons pu "faire évoluer" une solution optimale pour un problème dont nous ne connaissions pas la fonction de score.