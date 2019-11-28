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

        # Create a test question
        self.test_question = str(os.urandom(32))
        self.test_answer = str(os.urandom(32))
        self.test_category = random.randint(1, 7)
        self.test_difficulty = random.randint(1, 5)
        Question(
            question=self.test_question,
            answer=self.test_answer,
            category=1,
            difficulty=3
        ).insert()
        self.a_question = Question.query.filter(Question.answer == self.test_answer and
                                                Question.question == self.test_question and
                                                Question.category == self.test_category and
                                                Question.difficulty == self.test_difficulty).one_or_none()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_delete_a_question(self):
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


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
