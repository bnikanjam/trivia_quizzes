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
        """Create objects/rows in category and questions tables"""
        self.category_art = Category(type='Art').insert()
        self.category_science = Category(type='Science').insert()
        self.category_technology = Category(type='Technology').insert()

        # Create test questions
        Question(question='test question 1', answer='test answer 1', category=self.category_art, difficulty=3).insert()
        Question(question='test question 2', answer='test answer 2', category=self.category_science, difficulty=2).insert()
        Question(question='test question 3', answer='test answer 3', category=self.category_technology, difficulty=3).insert()
        Question(question='test question 4', answer='test answer 4', category=self.category_technology, difficulty=2).insert()
        Question(question='test question 5', answer='test answer 5', category=self.category_art, difficulty=3).insert()

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(test_config=True)
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        setup_db(self.app, os.getenv('TEST_DB_URI'))

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

            # create all tables
            self.db.create_all()
            self.create_data_in_database()

    def tearDown(self):
        """Executed after reach test"""
        # Delete all rows in both tables.
        Category.query.delete()
        Question.query.delete()

    def test_200_get_paginated_questions_list(self, page=1):
        self.create_data_in_database()
        resp = self.client().get('/questions?page=1')
        self.assertEqual(resp.json['status'], 'success')
        self.assertTrue(len(resp.json['categories']))
        self.assertTrue(len(resp.json['questions']))
        self.assertTrue(resp.json['total_questions'])
        self.assertEqual(resp.json['status'], 'success')
        self.assertEqual(resp.status_code, 200)

    def test_400_get_paginated_questions_list_with_no_questions_in_db(self, page=1):
        Question.query.delete()
        resp = self.client().get('/questions')

        self.assertEqual(resp.status_code, 400)

    def test_204_delete_a_question(self):
        """Create a test question in db and delete the same question"""
        Question(
            question='What color is the sky!?',
            answer='Blue',
            category=self.category_science,
            difficulty=1
        ).insert()
        test_question = Question.query.filter(Question.question == 'What color is the sky!?').one_or_none()
        resp = self.client().delete(f'/questions/{test_question.id}')
        retrieve_same_question = Question.query.filter(Question.id == test_question.id).one_or_none()
        self.assertIsNone(retrieve_same_question)
        self.assertEqual(resp.status_code, 204)

    def test_404_delete_a_question_doesnot_exist(self):
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
            "category": "2",
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
        self.assertEqual(read_from_db.category, '2')
        self.assertEqual(read_from_db.difficulty, 3)

        # response json payload
        self.assertEqual(resp.get_json()['status'], 'success')
        self.assertEqual(resp.get_json()['question'], 'Capital of CA?')
        self.assertEqual(resp.get_json()['answer'], 'Sacramento')
        self.assertEqual(resp.get_json()['category'], '2')
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
                                  data=json.dumps({'searchTerm': 'test q'}))
        self.assertEqual(resp.status_code, 200)

    # def test_200_questions_based_on_category(self):
    #     q = Question.query.all()

        # resp = self.client().get(f'/categories/{self.category_art.id}/questions')

    def test_200_get_questions_to_play_the_quiz(self):
        """  TEST: In the "Play" tab, after a user selects "All" or a category, one question
        at a time is displayed, the user is allowed to answer
        and shown whether they were correct or not."""

    def test_400_get_questions_to_play_the_quiz(self):
        pass


if __name__ == "__main__":
    unittest.main()
