# Trivia API

This project is a full-stack web app with API's first design. Users can add questions with categories and difficulty levels, Search questions, See a list of questions based on categories and play quiz games.

----

## Technologies Used:
####DevOps and Testing:
- **Docker** Container platform 
- **Heroku Postgres** Cloud Postgres database server as a service
- **Pipenv** Automatically manages virtual environments and packages
- **Unittest** Python builtin classbased test suit
- **Pytest** Python functional testing framework

#### Frontend:
- **React** JavaScript framework for interactive UIs.

#### Backend:
- **PostgreSQL 12.1**
- **Python 3.8**
- **Flask** Extensible and Lightweight WSGI web application framework
- **Flask-RESTful** Extension for Flask that adds support for quickly building REST APIs
- **Flask-SQLAlchemy** Extension for Flask that adds support for SQLAlchemy
- **Flask-Cors** Flask extension for handling Cross Origin Resource Sharing
- **SQLAlchemy** The Python SQL toolkit and Object Relational Mapper
- **psycopg2-binary** The Python PostgreSQL database adapter


#### Backend Code Quality:
- **flake8** Style guide enforcement
- **black** Code formatter
- **isort** Utility to sort imports

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 

---
## Getting Started

#### Pre-requisites
You should already have Python 3.8, Docker, Pipenv, and node installed on your local machine. The project is using a PostgreSQL database, and you also need one or two PostgreSQL database servers up and running ready to accept connections. 
- For development, you can use Postgres server installed locally, built in a docker container, or setup and hosted on a PaaS cloud service such as Heroku. You need to have your PostgreSQL server up and running somewhere and its credentials to connect to it. In this project, we use Heroku Postgres during development.
- For testing using a cloud database as a service is not practical because, for each test, a new connection must be established over the internet, which makes tests very time-consuming. We build a Postgres docker container for our tests.

#### Setup Local Development
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

##### Build Postgres Docker Container as Test Database
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
##### Run Tests
As explained above, in order to run the backend test suit you need to navigate to the backend directory and ensure:
- The project virtual environment is activated:
```
pipenv shell
```
- Our test database server, in our case, from within a docker container, is running and accepting connections:
```
docker-compose up -d
```
In this project we use Python builtin Unittest. That can be run:
```
python test_flaskr.py
```
The backend tests are not writen on pytest. Pytest is an entire functional testing framework of its own and it also runs classed based Unittests. Because pytest output uses color, is more informative,  and highlights errors and failed tests easier to see, we use it to run our unit tests.
```
pytest -s -p no:warnings
```
At the backend directory root there is you find a simple bash script file `cpytest.sh` that continuesly runs our tests. You can have this run in a seperate terminal while you write tests and codes to monitor your code effects as you are working on it. Other option could be IDEs like PyCharm can run your tests automatically everythime your codebase changes too. To fire up the isolated continues test run:
```
./cpytest.sh
```

##### Run Flask Development Web Server
To spin up flask built in development web server ensure virtual environment is activated and then run:
```
flask run
```
Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. The backend app is run on http://127.0.0.1:5000/ by default and is a proxy in the frontend configuration.

##### Run React Frontend Client 

Navigate to frontend directory, run the following commands to start the client:
```
npm install // only once to install dependencies
npm start
```
By default, the React app i.e. frontend runs on http://127.0.0.1:3000/.

---

## API Reference
#### Getting Started

Development Base URL: http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
Authentication: This version of the application does not require authentication or API keys.

#### Endpoints:

Success Response | Endpoints | HTTP Method | DB CRUD | Request URL Args | Request URL Vars | Request json body | Success Code | Error Codes | Frontend Views | Backend Resource |
:- | :- |:-:| :-:| :-: | :--: | :--: | :--: | :--: | :--: | :--: |
all categories | /categories | GET | READ | - | - | - | 200 | 400 404 | FormView QuizView | Categories
questions based on a category | /categories/category_id/questions | GET | READ | -| category_id | | 200 | 400 404 | QuestionView | CategoryQuestions
previous questions played. new question to play | /quizzes | POST | READ | - | - | YES | 200 | 400 | QuizView | PlayQuiz
all questions paginated | `/questions` or `/`| GET | READ | page| - | - | 200 | 400 404 | FormView QuestionView | Questions
Search all questions | `/questions` or `/`| POST | READ | - | - | Yes | 200 | 400  | FormView | Questions
Add a question | /questions| POST | CREATE | - | - | Yes | 201 | 400 404 | QuestionView
Delete a question | /questions/questions_id| DELETE | DELETE | - | questions_id| - | 204 | 404 | QuestionView


**GET /categories**
Sample Success Response
```
{
    "status": "success",
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    }
}
```

**GET /categories/category_id/questions**
Sample Success Response
```

{
    "status": "success",
    "questions": [
        {
            "id": 13,
            "question": "What is the largest lake in Africa?",
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2
        },
        {
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?",
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3
        },
        {
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?",
            "answer": "Agra",
            "category": 3,
            "difficulty": 2
        },
        {
            "id": 112,
            "question": "What is the highest and most extensive mountain range that lies entirely in Europe?",
            "answer": "Alps",
            "category": 3,
            "difficulty": 2
        },
        {
            "id": 113,
            "question": "What is the world's largest inland body of water, variously classed as the world's largest lake?",
            "answer": "Caspian Sea",
            "category": 3,
            "difficulty": 3
        }
    ],
    "total_questions": 5,
    "current_category": 3
}
```

**GET /quizzes**
Sample Request Body:
```
{
    "previous_questions": [
        12,
        4
    ],
    "quiz_category": {
        "type": "click",
        "id": 0
    }
}
```
Sample Success Response:
```
{
    "status": "success",
    "previousQuestions": [
        12,
        4,
        74
    ],
    "forceEnd": false,
    "question": {
        "question": "What percentage of women can orgasm through intercourse alone?",
        "answer": "25%"
    }
}
```


**GET /questions**
**GET /**
Sample Success Response:
```
{
    "status": "success",
    "questions": [
        {
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4
        },
        {
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4
        },
        {
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2
        },
        {
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?",
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3
        },
        {
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?",
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1
        },
        {
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?",
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3
        },
        {
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?",
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4
        },
        {
            "id": 12,
            "question": "Who invented Peanut Butter?",
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2
        },
        {
            "id": 13,
            "question": "What is the largest lake in Africa?",
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2
        },
        {
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?",
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3
        }
    ],
    "total_questions": 35,
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": null
}
```

**POST /questions** with `searchTerm` in request body
Sample Request Body with searchTerm:
```
{
    "searchTerm": "movie"
}
```
Sample Success Response:
```
{
    "status": "success",
    "question": "",
    "answer": "",
    "category": {},
    "difficulty": 0,
    "questions": [
        {
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4
        },
        {
            "id": 115,
            "question": "A 2015 artificial intelligence movie?",
            "answer": "Ex Machina",
            "category": 5,
            "difficulty": 5
        }
    ],
    "total_questions": 2,
    "categories": {
        "5": "Entertainment"
    },
    "current_category": 5
}
```



#### Authors
Yours truly, Babak Nikanjam

#### Acknowledgements 
- Jeff Shomali, React Support.
- The awesome team @ Udacity!
- Michael Herman @ testdriven.io
