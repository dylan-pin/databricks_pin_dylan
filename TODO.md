# PROS
- a partir d'une liste d'URL, vérifie l'accessibilité et récupère les champs de métadonnées indiqués

# CONS
- limité à la liste d'url fournit
- si changement de site source > changement de balise pour le scrapping
- récupère les premières données par page (il peut y avoir plusisuer avis client, note, EI, etc)

# TO DO
- crawler à partir d'URL racine
- méthode robuste généraliste VS adaptation à un nombre limité de source
- implémenter une DB
- par page, récupérer l'ensemble des avis et métadonnées associées
- formater/transformer les tables 
- gestion de mise a jour, pour éviter de refaire tout et surcharger les serveurs
- vérfier que l'ensemble des urls est bien parcouru (semble limité à quelques centaines pour le moment)
- traitement NLP des avis 
- traitement stats des variables
- dashboard de flux ETL
- dashboard des analyses