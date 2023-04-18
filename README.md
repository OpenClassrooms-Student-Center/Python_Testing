# gudlift-registration

1. **Why**

    This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is the keep things as light as possible, and use feedback from the users to iterate.

2. **Getting Started**

    This project uses the following technologies:

    * Python v3.x+

    * [Flask](https://flask.palletsprojects.com/en/1.1.x/)

        Whereas Django does a lot of things for us out of the box, Flask allows us to add only what we need. 
     

    * [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

        This ensures you'll be able to install the correct packages without interfering with Python on your machine.

        Before you begin, please ensure you have this installed globally. 


3. **Installation**

    - After cloning, change into the directory and type <code>virtualenv .</code>. This will then set up a a virtual python environment within that directory.

    - Next, type <code>source bin/activate</code>. You should see that your command prompt has changed to the name of the folder. This means that you can install packages in here without affecting affecting files outside. To deactivate, type <code>deactivate</code>

    - Rather than hunting around for the packages you need, you can install in one step. Type <code>pip install -r requirements.txt</code>. This will install all the packages listed in the respective file. If you install a package, make sure others know by updating the requirements.txt file. An easy way to do this is <code>pip freeze > requirements.txt</code>

    - Flask requires that you set an environmental variable to the python file. However you do that, you'll want to set the file to be <code>server.py</code>. Use this line code in vscode :
    `$env:FLASK_APP = "server.py"`
    or in windows terminal : 
    `C:\path\to\app>set FLASK_APP=server.py`

    - You should now be ready to test the application. In the directory, type either <code>flask run</code> or <code>python -m flask run</code>. The app should respond with an address you should be able to go to using your browser.

4. **Current Setup**

    The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). This is to get around having a DB until we actually need one. The main ones are:
     
    * competitions.json - list of competitions
    * clubs.json - list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.
    

5. **Testing**
    Here is the command line for execute the tests :
    #### Tests
    * **Coverage tests** 
        - simple test : 
        `pytest --cov=.`
        - test with html report : 
        `pytest --cov=. --cov-report html`
    * **Globals tests**
        - test all : 
        `pytest`
    * **Unit and functional tests**
        - unit tests only : 
        `pytest -m "not integtest"`
    * **Integration tests**
        - integration test only : 
        `pytest -m integtest`

    #### Locust test
    Here is how to run a Locust test :
    - run your flaks server : `flask run`
    - run locust server : `locust --locustfile=tests\test_performance\locustfile.py`
    - in your web browser, enter this url : `http://localhost:8089/`
    - set up your locust test and run it
    - once the test is done, you can generate its report


6. PEP8
    For generate the PEP8 report, we use the 'pycodestyle' librairie. Use this line in the console for create it : 
    `pycodestyle --exclude=env --statistics --count . > report_pycodestyle.txt`
    He will generate a .txt file named **report_pycodestyle.txt**. If this file is empty, it means there are no errors.
