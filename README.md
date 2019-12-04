# Trivia API

This project is a full-stack web app with API's first design. Users can add questions with categories and difficulty levels, Search questions, See a list of questions based on categories and play quiz games.

## Getting Started

### Pre-requisites and Local Development
You should already have Python 3.8, Docker, Pipenv, and node installed on your local machine. The project is using a PostgreSQL database, and you also need one or two PostgreSQL database servers. 
- For development, you can use Postgres server installed locally, built in a docker container, or setup and hosted on a PaaS cloud service such as Heroku. You need to have your PostgreSQL server up and running somewhere and its credentials to connect to it. In this project, we use Heroku Postgres during development.
- For testing using a cloud database as a service is not practical because, for each test, a new connection must be established over the internet, which makes tests very time-consuming. We build a Postgres docker container for our tests.

#### How to get a development env running
Clone the project repository and navigate to backend directory.
```
git clone https://github.com/bnikanjam/trivia_fullstack_api.git
cd trivia_fullstack_api/backend
```
Create a `.env` file to define environment variables we want to pass to our application and paste the following. You need to use your own Postgres database server URI.
```
# Flask
FLASK_APP=flaskr
FLASK_ENV=development

# Development PostgreSQL URI
DEV_DB_URI=<Place your own Postgres server URI>
TEST_DB_URI=postgresql://postgres:postgres@0.0.0.0:5432/trivia_test
```
Create the project virtual environment, install packages and spawn a shell with the virtualenv activated.
```
pipenv install
pipenv install --dev
pipenv shell
```
You should be able to see currently-installed dependency graph information.
```
pipenv graph
```
Verify that the project environment variables are properly loaded.
```
env | grep FLASK
env | grep DB_URI
```

##### Build a Postgres docker container for testing
We are pulling the Alpine version (minimal linux container)of Postgres 12.1. You can see docker the simple setup files in `Dockerfile` and `docker-compose.yml`. Start by ensuring that you have logged in `Docker Desktop` and you have Docker and Docker Compose:
```
docker -v
docker-compose -v
```
Build the image from docker file and fire up the container in detached mode:
```
docker build .
docker-compose up -d
```
To ensure our database now is ready to accept connections, view output from the container by:
```
docker-compose logs
```
If all successful with your current machine time stamp the last line should display:
```
test-db_1  | 2019-12-04 19:49:54.756 UTC [1] LOG:  database system is ready to accept connections
```
You can also populate the development database with some starting data from `trivia.psql` file. Here is how to do so with a Heroku Postgres database server:
```
 heroku pg:psql --app your-heroku-app-name-that-your-db-provisioned-with < trivia.psql
```




#### Backend
>Core Technologies:
- **Python 3.8**
- **PostgreSQL 12.1**

>Environment Management:
- **Pipenv**
Automatically manages virtual environments and packages
- **Postgres Server**
Installed locally, Built in a docker container, or Setup on a PaaS
- **Docker**

>Packages:
- **Flask** Extensible and Lightweight WSGI web application framework
- **psycopg2-binary** The Python PostgreSQL database adapter
- **SQLAlchemy** The Python SQL toolkit and Object Relational Mapper
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
- December 2019