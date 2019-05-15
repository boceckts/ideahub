# IdeaHub
[![Build Status](https://travis-ci.com/boceckts/ideahub.svg?token=peqtbSMtxkonhsy4FdNH&branch=master)](https://travis-ci.com/boceckts/ideahub)
[![codecov](https://codecov.io/gh/boceckts/ideahub/branch/master/graph/badge.svg?token=2iHhFVNnIr)](https://codecov.io/gh/boceckts/ideahub)

Practical project for the agile web development lecture [CITS5505](http://teaching.csse.uwa.edu.au/units/CITS3403/index.php?fname=projects&project=yes)

ToC:
1. [Main Idea](#main-Idea)
2. [Concept](#concept)
3. [Architecture](#Architecture)
4. [Development](#development)
    1. [Clone The Project](#clone-the-project)
    2. [Install Virtual Environment](#install-virtual-environment)
    3. [Initialize and Migrate new Database Schema](#initialize-and-migrate-new-database-schema)
    4. [Start the Web Application](#start-the-web-application)
    5. [Run Tests](#run-tests)
        1. [Test Coverage](#test-coverage)
    6. [Update Python Requirements](#update-python-requirements)
    7. [Database Initialization](#database-initialization)
    8. [Docker](#docker)


## Main Idea:
Ideas can be submitted by any registered user and other logged in users can then voted on them

## Concept
Users login and will be presented by a dashboard showing them their submitted ideas and their scores.
They have the option to submit new ideas, edit the idea to a new revision or delete their idea.
Users can also change their view to a stack of submitted ideas and vote on them.
Ideas could be revealed depending on tags or categories or at random.
Users not logged in can see all ideas but can not vote.


## Architecture
The following diagram visualizes the architecture of the ideahub application.
We followed the principle that all the database communication should only be done by using the respective services.
View and API should also not interfere or call each other.
While the view uses the internal model directly our API uses models from its own namespaces to easily marshall and un-marshall response and request objects.
![IdeaHub](ideahub-architecture.jpg)

## Development
In order to develop on this project you need to set up your local development environment.
The following steps need to performed in your terminal.
Python 3.x is required to be installed before proceeding with the next steps.

Install the python virtual environment packages by opening a **terminal** **(Linux/Mac)** or **command prompt** **(Windows)** and typing the following commands.
```
pip3 install virtualenv
```

### Clone the Project
Get the project code on your local computer to start developing.

1. Clone the git project

    with **ssh**
    ```
    git clone git@github.com:boceckts/ideahub.git
    ```
    or else with **https**
    ```
    git clone https://github.com/boceckts/ideahub.git
    ```

2. change into the newly created directory
    ```
    cd ideahub
    ```

### Install Virtual Environment
Inside the project folder create a virtual environment for the flask project and install all required dependencies for this project.

1. Create a folder for a virtual environment
    ```
    python -m venv flask
    ```

2. Activate your virtual environment
    
    on **Windows**
    ```
    flask\Scripts\activate
    ```
    - if you need to deactivate the virtual environent use
        ```
        flask\Scripts\deactivate
        ```
    or else on **Linux/Mac**
    ```
    source flask/bin/activate
    ```
    - if you need to deactivate the virtual environent just type
        ```
        deactivate
        ```

3. Install all requirements to run the project

    on **Windows**
    ```
    pip install -r requirements.txt
    ```
    or else on **Linux/Mac**
    ```
    pip install -r requirements.txt
    ```

### Initialize and Migrate new Database Schema
from within your virtual environment run the following scripts to init, migrate and upgrade your database.
1. Create a database
    ```
    flask db init
    ```
2. Migrate the database
    ```
    flask db migrate
    ```
3. Upgrade the database to use the latest table definitions
    ```
    flask db upgrade
    ```


### Start the Web Application
Run the flask web application on your localhost by either using the **Windows** command prompt or the terminal on **Linux/Mac**.
from within your virtual environment run the following commands to start your flask application.

on **Windows**
```
set FLASK_APP=app
set FLASK_ENV=development
flask run
```
or else on **Linux/Mac**
```
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

The web application should now be up and running at http://127.0.0.1:5000/.
The documentation of the REST API of the application will be available on http://127.0.0.1:5000/api/v1/docs.

### Run Tests
The project includes a test directory where any tests are located. In order to run them we use the unittest module of python.
Type the following commands within your virtual environment to run
all tests
```
python -m unittest test -vvv
```
specific unittests
```
python -m unittest test.unittests.<package>[.<module_name>] -vvv
```


#### Test Coverage
In order to see the test coverage of the project we can install and use the package `coverage` by typing `pip install coverage` into a terminal within your virtual environment.
Use the following commands to generate a test coverage report which can be viewed by opening the [index](htmlcov/index.html) file in a browser.
```
coverage run --source=app -m unittest discover -s test/
coverage html
```
Alternatively you can also view the report right in the terminal by using the command `coverage report -m`.


### Update Python Requirements
If you need to install new python packages or update existing ones, do so within your virtual environment.
Afterwards run the following command in a command prompt or terminal from within your virtual environment to ensure the new requirements will be versioned and available to others.
```
pip freeze > requirements.txt
```


### Database Initialization
We have added a database initialization command to flask that allows us to initialize the database with example data for demonstration and testing purposes.
This will make the following list of users available `users = ["Initial","Liam","William","James","Logan","Benjamin","Mason","Elijah","Oliver","Jacob","Lucas","Michael","Alexander","Ethan","Daniel","Matthew","Aiden","Henry","Joseph","Jackson","Samuel","Sebastian","David","Carter","Wyatt","Jayden","John","Owen","Dylan","Luke","Gabriel","Anthony","Isaac","Grayson","Jack","Julian","Levi","Christopher","Joshua","Andrew","Lincoln","Mateo","Ryan","Jaxon","Nathan","Aaron","Isaiah","Thomas","Charles","Caleb"]`.
Each user is created with a username following the pattern of lower anme of user followed by a `1` with the password `123456`.

E.g. username `logan1`, password `123456`.

If you need to initialize the database, type the following command from within your virtual environment.
```
flask initdb
```

### Docker
A dockerfile is available which can be used to quickly create a production container of the app.
For demonstration purposes we also initialize and fill the database inside the container with sample data.
In order to manually start the application in production mode you need to set the environment variable `FLASK_ENV=production` and pass `--host=0.0.0.0` as command args to the flask `run` command.
This will be automatically done by the docker container which can be build and run by typing the following commands in a command prompt or terminal.
```
docker build -t ideahub:latest .
docker run --name ideahub -p 5000:5000 ideahub:latest
```