import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restful import Api, Resource
import random

from sqlalchemy import exc, desc

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
        # response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    if not test_config:
        setup_db(app, os.getenv('DEV_DB_URI'))
    else:
        setup_db(app, os.getenv('TEST_DB_URI'))

    api = Api(app)

    class Categories(Resource):
        """"""
        payload_key = 'categories'

        def get(self):
            """HTTP GET """
            success_response = {
                'status': 'success',
                self.payload_key: list()
            }
            fail_response = {
                'status': 'fail',
                'message': 'The server can not find categories or no category exists yet.'
            }
            try:
                categories = Category.query.all()
                if categories is None:
                    return fail_response, 400
                else:
                    success_response[self.payload_key] = {category.id: category.type for category in categories}
                    return success_response, 200
            except ValueError:
                return fail_response, 404

    class Questions(Resource):
        """"""

        def get(self):
            """HTTP GET Request Method -> CRUD Read"""
            success_response = {
                'status': 'success',
                'questions': [],
                'total_questions': int(),
                'categories': {},
                'current_category': None
            }
            fail_response = {
                'status': 'fail',
                'message': 'The server can not find questions or no question exists yet.'
            }
            try:
                questions = Question.query.order_by(Question.id).all()
                categories = Category.query.all()

                if not questions or not categories:
                    fail_response['message'] = 'No questions/categories retrieved from database.'
                    return fail_response, 400
                else:
                    success_response['questions'] = paginate(request, questions)
                    success_response['total_questions'] = len(questions)
                    success_response['categories'] = {category.id: category.type for category in categories}
                    success_response['current_category'] = None
                    return success_response, 200
            except ValueError:
                return fail_response, 404

        def post(self):
            """HTTP POST Request Method"""
            success_response = {
                'status': 'success',
                'question': '',
                'answer': '',
                'category': {},
                'difficulty': int()
            }
            fail_response = {
                'status': 'fail',
                'message': 'Error adding new question to database.'
            }

            post_data = request.get_json(silent=True)
            if not post_data:
                fail_response['message'] = 'None or invalid question format sent to server.'
                return fail_response, 400

            if search_term := post_data.get('searchTerm', None):
                questions = Question.query.order_by(Question.id) \
                    .filter(Question.question.ilike(f'%{search_term}%')).all()

                categories_ids = {question.category for question in questions}
                categories = Category.query.filter(Category.id.in_(categories_ids)).all()
                current_category = random.choice(list(categories_ids)) if categories_ids else None

                success_response['questions'] = paginate(request, questions)
                success_response['total_questions'] = len(questions)
                success_response['categories'] = {category.id: category.type for category in categories}
                success_response['current_category'] = current_category
                return success_response, 200

            elif not all(
                    [post_data.get('question', None),
                     post_data.get('answer', None),
                     post_data.get('category', None),
                     post_data.get('difficulty', None)]
            ):
                fail_response['message'] = 'Required question data fields not sent to server.'
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
                    success_response['difficulty'] = difficulty
                    return success_response, 201
                except exc.IntegrityError:
                    new_question.rollback()
                    return fail_response, 433

        def delete(self, questions_id):
            """HTTP DELETE Request Method -> CRUD DELETE Action, to delete the specified question"""
            success_response = {
                'status': 'success',
                'message': 'Target question successfully deleted.'
            }
            fail_response = {
                'status': 'fail',
                'message': 'Error deleting target question.'
            }
            try:
                target_question = Question.query.filter(Question.id == questions_id).one_or_none()
                if target_question is None:
                    fail_response['message'] = 'Target question does not exist or already deleted.'
                    return fail_response, 404
                target_question.delete()
                return success_response, 204
            except exc.IntegrityError:
                target_question.rollback()
                return fail_response, 444

    class CategoryQuestions(Resource):

        def get(self, category_id):
            """Returns json response with list of questions base on a category.
            HTTP GET -> CRUD READ"""

            success_response = {
                'status': 'success',
                'questions': [],
                'total_questions': int(),
                'current_category': None
            }
            fail_response = {
                'status': 'fail',
                'message': 'Server can not find questions for requested category or the category does not exist.'
            }
            try:
                questions = Question.query.order_by(Question.id).filter(Question.category == category_id).all()

                if not questions:
                    return fail_response, 400
                else:
                    success_response['questions'] = paginate(request, questions)
                    success_response['total_questions'] = len(questions)
                    success_response['current_category'] = category_id
                    return success_response, 200
            except ValueError:
                return fail_response, 404

    class PlayQuiz(Resource):
        """"""

        def post(self):
            """Returns response object with questions to play the quiz.
            This endpoint takes category and previous question parameters and
            return a random questions within the given category, if provided,
            and that is not one of the previous questions. """
            success_response = {
                'status': 'success',
                # 'showAnswer': False,
                'previousQuestions': [],
                # 'guess': '',
                'forceEnd': False
            }
            fail_response = {
                'status': 'fail',
                'message': 'ERROR'
            }

            # # try:
            post_data = request.get_json(silent=True)
            print_blue(post_data)
            previous_questions = post_data.get('previous_questions')
            quiz_category = post_data.get('quiz_category')

            play_all_categories = True if not quiz_category['id'] else False
            if play_all_categories:
                questions_not_played_yet = Question.query.filter(~Question.id.in_(previous_questions)).all()
                new_question = random.choice(questions_not_played_yet)
                print_yellow(new_question)
                previous_questions.append(new_question.id)
            else:
                # TODO Category
                pass

            # success_response['showAnswer'] = False
            success_response['previousQuestions'] = previous_questions
            success_response['question'] = {
                'question': new_question.question,
                'answer': new_question.answer,
                # 'category': new_question.category,
                # 'difficulty': new_question.difficulty
                'forceEnd': False if questions_not_played_yet else True
            }
            # success_response['guess'] = ''
            success_response['forceEnd'] = False if questions_not_played_yet else True

            return success_response, 200

            # except:
            #     return fail_response, 400

    api.add_resource(Categories, '/categories')
    api.add_resource(CategoryQuestions, '/categories/<int:category_id>/questions')
    api.add_resource(Questions, '/', '/questions', '/questions/<int:questions_id>')
    api.add_resource(PlayQuiz, '/quizzes')

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    return app
