# Trivia API

This project is a full-stack web app with API's first design. Users can add questions with categories and difficulty levels, Search questions, See a list of questions based on categories and play quiz games.

## Getting Started

### Pre-requisites and Local Development
You should already have Python 3.8, Pipenv for managing dependencies and isolated virtual environments, and node installed on your local machine. The project is using a PostgreSQL database, and you also need one or two PostgreSQL database servers. 
- For development, you can use Postgres server installed locally, built in a docker container, or setup and hosted on a PaaS cloud service such as Heroku. You need to have your PostgreSQL server up and running somewhere and its credentials to connect to it. In this project, we use Heroku Postgres during development.
- For testing using a cloud database as a service is not practical because, for each test, a new connection must be established over the internet, which makes tests very time-consuming. We build a Postgres docker container for our tests.

#### Backend
>Core Technologies:
- **Python 3.8**
- **PostgreSQL 12.1**

>Environment Management:
- **Pipenv** Automatically manages virtual environments and packages.
- **Postgres Server**
- - Installed locally, Built in a docker container, or Setup on a PaaS)
- **Docker**


>Packages:
- **Flask** Extensible and Lightweight WSGI web application framework
- **psycopg2-binary** Python PostgreSQL database adapter 
- **Flask-SQLAlchemy** Extension for Flask that adds support for SQLAlchemy
- **Flask-Cors** Flask extension for handling Cross Origin Resource Sharing
- **Flask-RESTful** Extension for Flask that adds support for quickly building REST APIs

>Code Quality 
- **flake8** Style guide enforcement
- **black** Code formatter
- **isort** Utility to sort imports

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 


#### Frontend
>Core Technologies:
- **React**


#### Authors
Yours truly, Babak Nikanjam

#### Acknowledgements 
- Jeff Shomali, React Support.
- The awesome team @ Udacity!
- Michael Herman @ testdriven.io

###### Changelog
