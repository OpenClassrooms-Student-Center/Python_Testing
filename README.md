![badge](https://img.shields.io/static/v1?label=Project&nbsp;OC&message=11&color=blueviolet&style=for-the-badge)
![badge](https://img.shields.io/static/v1?label=Status&message=in_progress&color=blue&style=for-the-badge)

# ocrp11

Enhance a Python Web Application With Testing and Debugging

![Logo gudlift](https://raw.githubusercontent.com/FLinguenheld/Python_Testing/master/logos/gudlift.png "Logo")

****
### Description
The project purpose is to fix errors and add features using Git.  
This repository has been forked from [Python_Testing](https://github.com/OpenClassrooms-Student-Center/Python_Testing) which contains a flask application  
You can find here the flask application with a branch per bug / improvement / feature.  

This is a proof of concept project to show a light-weight version of a strongman competition booking platform.  
It allows to :  
- Book places in a competition
- See the clubs list

****
### Installation

Open your terminal and navigate to the folder where you want to install the API.  
Then, clone this repository :

    git clone https://github.com/FLinguenheld/Python_Testing

Navigate into the *Python_Testing/* folder and create a virtual environment :

    python -m venv env

Activate it :

    source env/bin/activate

Necessary packages are listed in the file *requirement.txt*.  
Install them :

    pip install -r requirement.txt

****
### Launch

Navigate into the *Python_Testing/* folder and activate the virtual environment.  
Launch the server with the command :

    python -m server

*⚡ The terminal will display all requests, you can stop it with **Ctrl-C***

Then, you can use your browser and open the page :

    http://localhost:5000/

The database is simulated with two json files *(in the folder ./database/)*. They contain three clubs which you 
can use to login :

    john@simplylift.co
    admin@irontemple.com
    kate@shelifts.co.uk

****
### Testing

According to the [fuctional specifications](http://course.oc-static.com/projects/Python+FR/P9+Python+Testing+FR/Spe%CC%81cifications+fonctionnelles.pdf), 
this code is covered by unit and integration tests. The framework used here is [Pytest](https://docs.pytest.org/en/7.2.x/).  
To launch a new test, open a terminal, navigate into the *Python_Testing/* folder and activate the virtual environment.  
Then launch the command :

    pytest -v

If you want more informations, you can move into the folder *Python_Testing/tests/report/* and open the file *pytest_html_report.html*. 
This file is updated each time pytest is used *(see [pytest-html-reporter](https://pypi.org/project/pytest-html-reporter/))*

****
### Performances

[Locust](https://locust.io) is used to test the server load.  
To generate a new test, open two terminals, go into the folder *Python_Testing/* and activate the virtual environment on both.  
Then you have to launch the server, you can launch it as usual or use this command :

    python -m locustfile

*⚡ This command will launch the server without the restrition of 12 maximum places per competition per club.*

Inside the second terminal, launch the command :

    locust

Then, you can use your browser and open the page :

    http://localhost:8089

Enter the number of users and the local server address : http://localhost:5000/  
The locust file will create a temporary club and competition then try to book places until you stop the test.
