<h1 align="center">Bienvenue sur le readme de GUDLFT 👋</h1>
<p align="center">
  <a href="https://twitter.com/LaurentJouron">
    <img alt="Twitter: LaurentJouron" 
      src="https://img.shields.io/twitter/follow/LaurentJouron.svg?style=social" target="_blank" />
  </a>
  <a href="https://github.com/LaurentJouron">
    <img alt="GitHub followers" 
      src="https://img.shields.io/github/followers/LaurentJouron?style=social" />
  </a>
</p>

<p align="center">
    <img align="left"
      width="50px" 
      src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcToscdusMNjQbffwasgiLuCsbCNZisJRE95Fg&usqp=CAU" />
</p>

### ``--- Explication en français ---``
___________

Cet exercice a été réalisé dans le cadre d'une formation 
___________

<h1 align="center">But de l'application</h1>

Avant toute chose, il faut forker et installer l'application [Python_Testing](https://github.com/OpenClassrooms-Student-Center/Python_Testing). Le but étant de suivre les instructions du README qui ne sont pas à jour. Il a fallu chercher des solutions pour faire en sorte que tout fonctionne.
Ensuite, il y a des instructions sur certains bugs qu'il faut resoudre et un avancement a mettre en place. J'ai réalisé des tests avec Pytest pour être sûr que tout ce qui a été mis en place est fonctionnel selon les attentes. Pour finir j'ai testé la performance de l'application avec Locust.

___________

<h1 align="center">Langage et bibliothèques</h1>

<p align="center">L'intégralité de l'application a été développer en Python - Flask</p>


<table>
  <tr>
    <td align="center">
      <a href=https://www.python.org/">
        <img width="200px"
          src="https://www.python.org/static/img/python-logo.png" /><br />
        <sub><b>Téléchargez Python</b></sub></a><br />
      <a href=https://www.python.org/" title="Téléchargez Python" ></a> 
    </td>
    <td align="center">
      <a href="https://flask.palletsprojects.com/en/3.0.x/">
        <img width="200px"
          src="https://flask.palletsprojects.com/en/3.0.x/_images/flask-horizontal.png" /><br />
        <sub><b>Doc Flask</b></sub></a><br />
      <a href="https://flask.palletsprojects.com/en/3.0.x/" title="Doc Flask" ></a> 
    </td>
  </tr>
</table>

___

<p align="center">Les tests ont étés fait avec Pytest - Locust</p>


<table>
  <tr>
    <td align="center">
      <a href="https://docs.pytest.org/en/7.4.x/">
        <img width="100px"
          src="https://docs.pytest.org/en/7.4.x/_static/pytest_logo_curves.svg" /><br />
        <sub><b>Pytest</b></sub></a><br />
      <a href="https://docs.pytest.org/en/7.4.x/" title="Pytest" ></a> 
    </td>
    <td align="center">
      <a href="https://locust.io/">
        <img width="200px"
          src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT1fcH7bg61ntxizEMY1RcM295VMx1SMfaD7g&usqp=CAU" /><br />
        <sub><b>Locust</b></sub></a><br />
      <a href="https://locust.io/" title="Locust" ></a> 
    </td>
  </tr>
</table>

___________

<h1 align="center">EDI</h1>


<p align="left">L'EDI utilisé pour la programmation est Pycharm et Visual Studio Code.

<table>
  <tr>
    <td align="center">
      <a href=https://www.jetbrains.com/fr-fr/pycharm/download/#section=windows">
        <img width="100px"
          src="https://upload.wikimedia.org/wikipedia/commons/1/1d/PyCharm_Icon.svg" /><br />
        <sub><b>Téléchargez Pycharm</b></sub></a><br />
      <a href=https://www.jetbrains.com/fr-fr/pycharm/download/#section=windows" title="Téléchargez Pycharm" ></a> 
    </td>
    <td align="center">
      <a href="https://visualstudio.microsoft.com/fr/">
        <img width="130px"
          src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-H3CcAG7w2nXSnlqldVWR-ER4mvFfLgqYxA&usqp=CAU" /><br />
        <sub><b>Visuable Studio Code</b></sub></a><br />
      <a href="https://visualstudio.microsoft.com/fr/" title="Visuable Studio Code" ></a>
    </td>
  </tr>
</table>

___________

<h1 align="center">Installation du site </h1>

Pour commencer il faut cloner le projet grâce à l'url suivante :
  * ``git clone https://github.com/LaurentJouron/GUDLFT.git``

Il faut se déplacer dans le dossier:
  * ``cd GUDLFT``

Voici la procédure pour afficher la page d'accueil du site:

Créer un répertoire avec le nom .venv
  * ``mkdir .venv``

Installer les bibliothèques nécessaires avec
  * ``pipenv install`` ou ``pip install``

Activer l'environnement de travail (environnement virtuel) avec
  * ``pipenv shell`` ou ``pip shell``

Démarrer le serveur de développement de Flask avec
  * ``flask run``

___________


<h1 align="center">GUDLFT coverage test </h1>

Pour voir les tests dans le terminal
  * ``pytest``

Pour voir le détails des tests dans le terminal
  * ``pytest -vvv``

Pour mesurer la couverture de test d'un projet:
  * ``pytest --cov=. tests/``

Pour générer un rapport HTML automatiquement :
  * ``pytest --cov=. --cov-report html``
  
    Ouvrez le dossier htmlcov et lancer index.html dans un navigateur.


___________


<h1 align="center">GUDLFT performance test </h1>

Pour se placer dans le bon dossier
  * ``cd tests``
  * ``cd test_performance``

Lancer le test:
  * ``locust``

Se rendre dans un navigateur et rentrez l'adresse suivante:
  * ``http://localhost:8089``

___________

<h1 align="center">Auteur et collaborateurs</h1>


<table>
  <tr>
    <td align="center">
      <a href="https://github.com/LaurentJouron">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRlW-w7O7g3hQTw8qcIAy3LCRhiHg5tUPfvVg&usqp=CAU"
          width="100px;"/><br />
        <sub><b>Laurent Jouron</b></sub></a><br />
      <a href="https://openclassrooms.com/fr/" title="Étudiant">🈸</a>
      <a href="https://github.com/LaurentJouron/Books-online" title="Codeur de l'application">💻</a>
    </td>
    <td align="center">
      <a href="https://github.com/thierhost">
        <img src="https://avatars.githubusercontent.com/u/7854284?s=100&v=4"
          width="100px;"/><br />
        <sub><b>Thierno Thiam</b></sub></a><br />
      <a href="https://github.com/thierhost" title="Mentor de Laurent">👨‍🏫</a> 
      <a href="https://www.python.org/dev/peps/pep-0008/" title="Doc PEP 8">📄</a>
    </td>
  </tr>
</table>