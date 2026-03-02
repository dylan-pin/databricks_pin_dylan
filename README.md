# databrick
Mini projet Pipeline de données interne

## 1. Objectif

Ce TP a pour objectif de comprendre :

- le rôle de Databricks dans le traitement de données
- le rôle de Airflow dans l’orchestration
- la construction d’un pipeline simple bronze silver gold
- les bonnes pratiques professionnelles
- les conventions de nommage

---

## 2. Rôle des outils

### Databricks

Plateforme de traitement de données.

Responsable de :
- ingestion
- transformation
- agrégation
- exécution de jobs Spark
- gestion des tables Delta

Databricks exécute la logique métier.

---

### Airflow

Orchestrateur de workflows.

Responsable de :
- planification
- gestion des dépendances
- monitoring
- retries et alertes

Airflow organise l’ordre d’exécution mais ne contient pas la logique métier.

---

## 3. Différences clés

Databricks = moteur de traitement  
Airflow = orchestrateur  

Databricks transforme la donnée  
Airflow coordonne les tâches  

Les deux outils sont complémentaires.

---

## 4. Contexte métier fictif

Entreprise fictive DataCorp.

Objectif :
Analyser les ventes quotidiennes afin de suivre :
- chiffre d’affaires
- nombre de commandes
- panier moyen
- top produits

Les données proviennent d’un fichier interne simulé.

---

## 5. Architecture du mini projet

Pipeline type medallion :

bronze  
données brutes

silver  
données nettoyées et structurées

gold  
données agrégées prêtes pour analyse

Flux :

source interne  
ingestion bronze  
transformation silver  
agrégation gold  

---

## 6. Étapes du TP

### Étape 1 Ingestion
- lecture fichier CSV
- création table bronze_sales_orders

### Étape 2 Transformation
- nettoyage données
- gestion valeurs nulles
- création table silver_sales_orders

### Étape 3 Agrégation
- calcul chiffre_affaires
- calcul panier_moyen
- agrégation par date
- création table gold_sales_kpi_daily

---

## 7. Conventions de nommage

### Principes généraux
- minuscules uniquement
- snake_case
- noms explicites
- inclure le domaine métier
- inclure environnement si nécessaire dev stg prod
- pas de date dans les noms
- pas de version dans les noms
- versionnement via Git

---

### Databricks

Jobs  
env_domain_pipeline_frequency  

Exemple  
dev_sales_etl_daily  

Tasks  
ordre_action_objet  

Exemple  
01_extract_orders  
02_transform_orders  
03_load_orders  

Notebooks  
nb_domain_action_objet  

Exemple  
nb_sales_transform_orders  

---

### Airflow

DAG  
env_domain_pipeline_dag  

Exemple  
dev_sales_etl_dag  

Tasks  
action_objet  

Exemple  
extract_orders  
transform_orders  
load_orders  

---

## 8. Bonnes pratiques

### Architecture
- séparer orchestration et transformation
- éviter la logique métier dans Airflow
- centraliser la logique dans Databricks

### Code
- structurer les notebooks
- ajouter des logs clairs
- gérer les erreurs
- documenter chaque étape

### Organisation
- définir un owner
- définir un SLA
- tester en dev avant prod
- documenter le pipeline

---

## 9. Livrables attendus

- notebooks ingestion transformation agrégation
- job Databricks orchestrant les notebooks
- respect des conventions de nommage
- documentation claire

---

## 10. Compétences développées

- compréhension architecture data moderne
- structuration pipeline
- bonnes pratiques data engineering
- organisation projet
- documentation technique

---

Règle d’or  
La cohérence d’équipe est plus importante que la convention parfaite.
