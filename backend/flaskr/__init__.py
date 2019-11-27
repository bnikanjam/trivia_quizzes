import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
import random

from sqlalchemy import exc

from models import setup_db, Question, Category

from utilities import print_blue, print_green, print_red, print_yellow

QUESTIONS_PER_PAGE = 10


def paginate(request, selection):
    page = request.args.get('page', 1, int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    # questions = [question.format() for question in selection]
    # return questions[start:end]
    return [question.format() for question in selection[start:end]]


# Application factory
def create_app(test_config=None):
    app = Flask(__name__)

    # Initializes Cross Origin Resource sharing for the app
    CORS(app)

    # Set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        #     # response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    if not test_config:
        setup_db(app, os.getenv('DEV_DB_URI'))
    else:
        setup_db(app, os.getenv('TEST_DB_URI'))

    api = Api(app)

    parser = reqparse.RequestParser()
    parser.add_argument('')

    class Categories(Resource):
        def get(self):

            success_response_object = {
                'status': 'success',
                'categories': list()
            }
            fail_response_object = {
                'status': 'fail',
                'message': 'The server can not find categories or no category exists yet.'
            }

            try:
                categories = Category.query.all()
                if categories is None:
                    return fail_response_object, 400
                else:
                    data = [category.format() for category in categories]
                    success_response_object['data'] = data
                    return success_response_object, 200
            except ValueError:
                return fail_response_object, 404

    class Questions(Resource):
        def get(self):
            success_response = {
                'status': 'success',
                'questions': list(),
                'total_questions': int(),
                'categories': list(),
                'current_category': str()
            }
            fail_response = {
                'status': 'fail',
                'message': 'The server can not find questions or no question exists yet.'
            }

            try:
                questions = Question.query.all()
                categories = Category.query.all()

                if not questions or not categories:
                    return fail_response, 400
                else:
                    success_response['questions'] = paginate(request, questions)
                    success_response['total_questions'] = len(questions)
                    success_response['categories'] = [category.format() for category in categories]
                    success_response['current_category'] = None
                    return success_response, 200
            except ValueError:
                return fail_response, 404

        def post(self):

            success_response = {
                'status': 'success',
                'question': str(),
                'answer': str(),
                'category': int(),
                'difficulty': int()
            }
            fail_response = {
                'status': 'fail',
                'message': 'Error adding new question to database.'
            }

            post_data = request.get_json()
            if post_data is None:
                fail_response['message'] = 'None or invalid question format sent to server.'
                return fail_response, 400
            else:
                try:
                    question = post_data.get('question'),
                    answer = post_data.get('answer'),
                    category = post_data.get('category'),
                    difficulty = post_data.get('difficulty')
                    new_question = Question(
                        question=question,
                        answer=answer,
                        category=category,
                        difficulty=difficulty
                    ).insert()
                    success_response['question'] = question[0]
                    success_response['answer'] = answer[0]
                    success_response['category'] = category[0]
                    success_response['difficulty'] = difficulty[0]
                    return success_response, 201
                except exc.IntegrityError:
                    new_question.rollback()
                    return fail_response, 400

    api.add_resource(Categories, '/categories')
    api.add_resource(Questions, '/', '/questions')


    # TEST: At this point, when you start the application
    # you should see questions and categories generated,
    # ten questions per page and pagination at the bottom of the screen for three pages.
    # Clicking on the page numbers should update the questions.

    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

    '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

    '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    return app
