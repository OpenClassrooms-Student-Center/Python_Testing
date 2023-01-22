![Logo](images/logo.png)

# Projet 11 DA-Python OC
***Livrable forké et cloné à partir du repository [Python_Testing](https://github.com/OpenClassrooms-Student-Center/Python_Testing) d'OpenClassrooms-Student-Center.***  
Il s'agit d'une plateforme de réservation de places à des compétitions de force pour l'entreprise Güdlft.  
L'objectif du projet est de corriger les bugs et d'implémenter une nouvelle fonctionnalité décrits dans l'Issue repository du projet originel.  
Chaque correctif de bug ou fonctionnalité correspond à une branche. Il y a égélement une branche d'affinement des tests et une branche QA stable.
Les tests peuvent être éxécutés via Pytest et Locust.  
## Sommaire

**[1. Installation et lancement](#heading--1)**
  * [1.1. Windows](#heading--1-1)
  * [1.2. MacOS et Linux](#heading--1-2)

**[2. Tests](#heading--2)**
  * [2.1 Lancement des tests](#heading--2-1)
  * [2.2 Présentation des rapports](#heading--2-2)

       

<div id="heading--1"/>

### 1. Installation et lancement

<div id="heading--1-1"/>

#### 1.1 Windows :
   Depuis votre terminal, naviguez vers le dossier racine souhaité.

###### Récupération du projet
   Tapez :    

       git clone https://github.com/Cyl94700/P11_Op_Cl.git

###### Accès au dossier du projet, création et activation l'environnement virtuel
   Tapez :

       cd P11_Op_Cl
       python -m venv env 
       env\scripts\activate
    
###### Installation des paquets requis
   Tapez :

       pip install -r requirements.txt


###### Lancement du serveur Flask
   Tapez :

      $env:FLASK_APP = "server.py"
      flask run

Puis, accédez à l'adresse par défaut : [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

<div id="heading--1-2"/>

---------

####  1.2 MacOS et Linux :
   Depuis votre terminal, naviguez vers le dossier souhaité.

###### Récupération du projet
   Tapez :

       git clone https://github.com/Cyl94700/P11_Op_Cl.git

###### Accéder au dossier du projet, créer et activer l'environnement virtuel
   Tapez :

       cd P11_Op_Cl
       python3 -m venv env 
       source env/bin/activate
    
###### Installation des paquets requis
   Tapez :

       pip install -r requirements.txt


###### Lancement du serveur Flask
   Tapez :

       export FLASK_APP=server
       flask run

Puis, accédez à l'adresse par défaut : [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

<div id="heading--2"/>

### 2. Tests

<div id="heading--2-1"/>

#### 2.1 Lancement des tests

###### Tests unitaires, d'intégration et fonctionnel
###### Couvertures de Test coverage
###### Test de performances Locust
###### Flake8

<div id="heading--2-2"/>

#### 2.2 Présentation des rapports





