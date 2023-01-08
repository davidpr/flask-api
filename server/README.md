## Python environment
    Create env:
        python3 -m venv server/autoserver
    Activate env:
        source server/autoserver/bin/activate
    python3 -m pip list

*install the requirements to the local virtual env.*

    pip3 install -r server/requirements.txt

*packages to install:* 

    pip3 install Flask 
    pip3 install uuid
    pip3 install pymongo
    pip3 install python-dotenv

    others: Flask-Cors



    pip3 install Flask pymongo uuid  

---
## Running the app/server
    flask run
    python3 app.py # to run it from the virtual environment

    annotations:
        configuration of environments
        - https://apiflask.com/configuration/

---
## Unit testing in local environment
    docs:
        - https://docs.python.org/3/library/unittest.html

    annotations:
        - test file names should start with 'test'
        - the create_app() in app/__init__.py loads the instance/config-testing.py when TESTING is True (config/testing.py)
        - instance folder is for secret variables

    inside of the flask-server/server folder do:
        - export APP_SETTINGS_MODULE=testing
        - python3 -m unittest

---
## Docker
    pip3 freeze > server/requirements.txt
    pip3 install -rserver/requirements.txt


    docker  build -t datapta/server_docker .
    docker login
    docker push datapta/server_docker


    docker run -p 5000:5000 -d datapta/server_docker

    docker ps
    docker stop xxx

    troubleshooting:
        not being able to reach the server when running with flask run
        https://stackoverflow.com/questions/7023052/configure-flask-dev-server-to-be-visible-across-the-network

## Skaffold
    skaffold dev
    to ignore files just use the .dockerignore
---