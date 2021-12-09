import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgres://postgres:Projecta2008@localhost:5432/trivia'
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_search = {
            'searchTerm': 'Soccer'
        }

        self.new_question = {
            'question': 'What colour is grass?',
            'answer': 'Green',
            'diffculty': '1',
            'category': '1'
        }    

        self.quizzes = {
            'previous_questions': [1, 2],
            'quiz_category': {
                'id': 2,
                'type': 'Art'
            }}
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions']) 
        self.assertTrue(len(data['questions'])) 

    def test_404_sent_requestion_beyond_valid_page(self):
        res = self.client().get('/question?page=1000', json={'rating': 1})
        data = json.loads(res.data) 

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories']) 
        self.assertTrue(len(data['categories'])) 

    def test_fail_get_categories(self):
        res = self.client().post('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False) 

    def test_create_new_question(self):
        res = self.client().post('/add', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['questions'])

    def test_fail_create_new_question(self):
        res = self.client().get('/add', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)  

    def test_get_category_questions(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))

    def test_fail_get_category_questions(self):
        res = self.client().post('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)  

    def test_search_question(self):
        res = self.client().get('/questions', json=self.new_search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_fail_search_question(self):
        res = self.client().post('/questions', json=self.new_search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)    

    def test_delete_question(self):
        res = self.client().delete('/questions/50')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 50).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 50)
        self.assertTrue(data['total_questions'])
        self.assertEqual(question, None)

    def test_fail_delete_question(self):
        res = self.client().post('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False) 

    def test_404_if_question_does_not_exist(self):
        res = self.client().delete('question/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_quiz_questions(self):
        res = self.client().post('/quizzes', json=self.quizzes)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_fail_get_quiz_questions(self):
        res = self.client().get('/quizzes', json=self.quizzes)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False) 
        


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()