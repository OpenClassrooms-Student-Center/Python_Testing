# gudlift-registration

1. Why

    This is a proof of concept (POC) project to show a light-weight version of our competition booking platform.  
    The aim is the keep things as light as possible, and use feedback from the users to iterate.

2. Getting Started

    This project uses the following technologies:

    * Python v3.x+

    * [Flask](https://flask.palletsprojects.com/en/1.1.x/)  
        Whereas Django does a lot of things for us out of the box, Flask allows us to add only what we need.

    * [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)  
        This ensures you'll be able to install the correct packages without interfering with Python on your machine.  


3. Installation

    - After cloning, change into the directory and type `python -m venv env`.  
    This will then set up a a virtual python environment within that directory.

    - Next, type `source env/bin/activate`.  
    You should see that your command prompt has changed to the name of the folder.  
    This means that you can install packages in here without affecting affecting files outside.  
    *To deactivate, type `deactivate`*

    - Rather than hunting around for the packages you need, you can install in one step.  
    Type `pip install -r requirements.txt`.  
    This will install all the packages listed in the respective file. If you install a package, make sure others know by updating the requirements.txt file.  
    An easy way to do this is `pip freeze > requirements.txt`

    - To launch the server, you can set an environmental variable to the python file.  
    Type `export FLASK_APP=server.py`  
    Check [here](https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application) for more details

    - If you had set the environmental variable, you would launch the server with the command :  
    `flask run`  
    If you hadn't set the variable, you would use the command :  
        `flask --app server run`

    - Now open your browser with this address to test the application :  
    http://127.0.0.1:5000


4. Current Setup

    The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm).  
    This is to get around having a DB until we actually need one.  
    These files are stored inside the *database* folder.  

    - competitions.json - list of competitions  

    - clubs.json - list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.  


5. Testing

    Pytest and pytest-flask have been installed with the file requirements.txt.
    To run a test, open a terminal, move to the folder Python_Testing/, active the virtual environment and enter the command :  
    `pytest -v`
