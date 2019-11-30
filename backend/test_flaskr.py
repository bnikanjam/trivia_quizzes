import os
import unittest
import random
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

from utilities import *


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def create_data_in_database(self):
        # Create 10 test categories in db from 'Test Category 0' to 'Test Category 9'.
        self.categories = [Category(type=f'Test Category {x}').insert() for x in range(10)]

        # Create a test question in db
        self.test_question = str(os.urandom(32))
        self.test_answer = str(os.urandom(32))
        self.test_category = random.choice(self.categories)
        self.test_difficulty = random.randint(1, 5)
        Question(
            question=self.test_question,
            answer=self.test_answer,
            category=self.test_category,
            difficulty=3
        ).insert()
        self.a_question = Question.query.filter(
            Question.answer == self.test_answer and
            Question.question == self.test_question and
            Question.category == self.test_category and
            Question.difficulty == self.test_difficulty
        ).one_or_none()

        # Create 3 test questions
        Question('test question 1', 'test answer 1', 6, 3).insert()
        Question('test question 2', 'test answer 3', 5, 2).insert()
        Question('test question 3', 'test answer 3', 3, 4).insert()

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(test_config=True)
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        # self.database_path = "postgres://{}/{}".format('0.0.0.0:5432', self.database_name)
        setup_db(self.app, os.getenv('TEST_DB_URI'))

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # delete all rows in the tables
        Category.query.delete()
        Question.query.delete()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_paginated_questions_list(self, page=1):
        self.create_data_in_database()
        resp = self.client().get('/questions?page=1')
        self.assertEqual(resp.json['status'], 'success')
        self.assertTrue(len(resp.json['categories']))
        self.assertTrue(len(resp.json['questions']))
        self.assertTrue(resp.json['total_questions'])
        self.assertEqual(resp.json['status'], 'success')
        self.assertEqual(resp.status_code, 200)

    def test_400_get_paginated_questions_list_with_no_questions_read(self, page=1):
        resp = self.client().get('/questions')
        self.assertEqual(resp.status_code, 400)

    def test_delete_a_question(self):
        self.create_data_in_database()
        self.assertIsNotNone(self.a_question)
        resp = self.client().delete(f'/questions/{self.a_question.id}')
        retrieve_same_question = Question.query.filter(Question.question == self.test_question).one_or_none()
        self.assertIsNone(retrieve_same_question)
        self.assertEqual(resp.status_code, 204)

    def test_delete_a_question_doesnot_exist(self):
        retrieve_same_question = Question.query.filter(Question.id == 1000000).one_or_none()
        self.assertIsNone(retrieve_same_question)
        resp = self.client().delete(f'/questions/1000000')
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.json['status'], 'fail')

    def test_201_add_new_question(self):
        headers = {
            'Content-Type': 'application/json'
        }
        new_question = {
            "question": "Capital of CA?",
            "answer": "Sacramento",
            "category": "5",
            "difficulty": 3
        }
        resp = self.client().post('/questions',
                                  headers=headers,
                                  data=json.dumps(new_question))
        # response code
        self.assertEqual(resp.status_code, 201)

        # compare with database
        read_from_db = Question.query.filter(Question.question == 'Capital of CA?').one_or_none()
        self.assertIsNotNone(read_from_db)
        self.assertEqual(read_from_db.answer, 'Sacramento')
        self.assertEqual(read_from_db.category, '5')
        self.assertEqual(read_from_db.difficulty, 3)

        # response json payload
        self.assertEqual(resp.get_json()['status'], 'success')
        self.assertEqual(resp.get_json()['question'], 'Capital of CA?')
        self.assertEqual(resp.get_json()['answer'], 'Sacramento')
        self.assertEqual(resp.get_json()['category'], '5')
        self.assertEqual(resp.get_json()['difficulty'], 3)

    def test_400_add_new_question_no_json_in_request(self):
        headers = {
            'Content-Type': 'application/json'
        }
        resp = self.client().post('/questions',
                                  headers=headers,
                                  data='DSFGHF')
        # response code
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.get_json()['status'], 'fail')

    def test_444_add_new_question_with_missing_data_fields(self):
        headers = {
            'Content-Type': 'application/json'
        }
        new_question = {
            "question": "Capital of CA?",
            # "answer": "Sacramento",
            "category": "5",
            "difficulty": 3
        }
        resp = self.client().post('/questions',
                                  headers=headers,
                                  data=json.dumps(new_question))
        # response code
        self.assertEqual(resp.status_code, 400)

    def test_200_search_questions_returned_results(self):
        headers = {
            'Content-Type': 'application/json'
        }
        resp = self.client().post('/questions',
                                  headers=headers,
                                  data=json.dumps({'searchTerm': 'question 3'}))
        self.assertEqual(resp.status_code, 200)
        # self.assertEqual(resp.questions, ['test question 3'])
        self.assertEqual(resp.total_questions, 1)
        # self.assertEqual(resp.current_category, None)


if __name__ == "__main__":
    unittest.main()
