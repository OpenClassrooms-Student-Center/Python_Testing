# OC-PROJET 11: Améliorez une application Web Python par des tests et du débogage
#
### Présentation:
Nous sommes chargés par la société Güdlft d'améliorer leur application de gestion des reservation
pour que des clubs de liftings puissent réserver des places en compétitions.

Cette application est écrite avec **Python** accompagné du framework **Flask** et plusieurs libraries de tests
telles que **coverage**, **pytest**, **flake8** et **locust**

Nous devons donc débugger et tester l'application.

Le projet originel se trouve ici : https://github.com/OpenClassrooms-Student-Center/Python_Testing
#
### Installation:
Vous devez tout d'abord vous doter de la dernière version de python, vous pouvez la télécharger ici:
https://www.python.org/downloads/

Du fait que ce projet est un **fork** (nouveau logiciel créé à partir d'un logiciel existant), 
vous devrez cloner mon **fork**, pour ce faire : 
1. Ouvrez un terminal de commande
2. Entrez : ``git clone https://github.com/thomas-barbato/projet-11``
3. Créer un environnement virtuel:
`python3 -m venv /path/to/new/virtual/environment`
 Ou `python -m virtualenv venv`
4. Activer l'environnement virtuel:
```
cd Venv\Scripts\ ; .\activate.bat ;
cd .. 
cd ..
```
5. Installez les prérequis au bon fonctionnement du projet avec la commande suivante:
   - Version "normale": ``pip install -r requirements.txt``
   - Version "testing": ``pip install -r requirements-testing.txt``
#
### Démarrage de l'application:
Pour faire fonctionner l'application, vous aurez besoin de démarrer Flask, pour cela:
1. Ouvrez un terminal **externe** à votre IDE *( integrated development environment)*
dans le dossier du projet.
2. Définissez une variable d'environnement :
    - Sous windows: ``set FLASK_APP=server.py``
    - sous linux: ``export FLASK_APP=server``
3. Démarrez avec la commande suivante :
    - ``flask run``
4. Vous pouvez maintenant accéder à l'application, via l'url suivante :
    - http://127.0.0.1:5000/
#
### La phase de tests:
Pour ce projet, nous effectuons trois phases de tests, pour cela nous utiliserons quatre
outils différents, leur utilisation est expliquée ci-dessous:

##### *Pytest*
Les tests qui ont étés rédigés pour ce projet se trouvent dans le répertoire **tests**
Pour lancer pytest veuillez entrer la commande suivante dans votre terminal:

- `pytest .\tests\`

Cette commande exécutera tous les tests qui se trouvent dans le répertoire tests, vous pouvez
choisir vos tests en ajoutant directement le nom du fichier test ciblé, exemple:
- ``pytest .\tests\test_clubs.py``

##### *Locust*

Concernant Locust, vous pouvez consulter le rapport généré dans le dossier **locust_report**, 
il s'ouvre dans un navigateur.

Cependant, si vous voulez lancer vous-même le test locust, entrez la commande suivante dans votre terminal:

- ``locust -f .\tests\locustfile.py``

Vous aurez alors l'url suivante générée : 
 - http://0.0.0.0:8089

**CEPENDANT** si cette url ne fonctionne pas, alors vous devez utiliser l'url suivante : 
 - http://localhost:8089/

##### *Coverage*

Vous pouvez consulter le rapport coverage situé dans:
- ``htmlcov/index.html``

Il s'ouvre avec votre navigateur web, **les spécifications fonctionnelles exigent d'avoir un taux
de couverture de 60% , ici nous sommes à 88%.**

!["Résultats de coverage en image"](coverage_results.PNG)

Pour exécuter coverage, vous devrez entrer la commande suivante dans votre terminal:
- ``coverage run -m pytest .\tests\``

Pour sauvegarder ensuite le rapport en html:
- ``coverage html``

##### *Flake8*

Vous pouvez consulter le rapport flake8 dans le répertoire suivant:
- ``flake-report/index.html``

Pour générer vous-même un test, entrez la commande suivante dans votre terminal:
- ``flake8``

Aucun argument n'est nécessaire, car nous avons déjà un fichier de configuration ici:
- ``setup.cfg``
