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
        self.database_name = "trivia"
        self.database_path = "postgres://postgres:1234@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['categories']['1'], 'Science')
        
    def test_failing_to_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['categories']['1'], 'math')
        
    def test_get_paginated_questions(self):
        res = self.client().get('/questions/')
        data = json.loads(res.data)
        self.assertEqual(data['total_questions'], 10)

    def test_failing_to_get_questions(self):
        res = self.client().get('/questions/')
        data = json.loads(res.data)
        self.assertEqual(data['total_questions'], 11)
            
    def test_post_new_question(self):
        res = self.client().post('/questions', json= {
            'question':'how do you do', 'answer': 'i am fine','difficulty': 4,'category': 'Science'})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)

    def test_failing_to_post_question(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
                
    def test_delete_question(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['question_id'], 5)
    
    def test_failing_to_delete_question(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['question_id'], 5)

       #add section for testing
    def test_quiz_play(self):
        res = self.client().post('/quizzes', json={'previous_questions':[], 'quiz_category':{'id':2} })
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['question']['id'], 21)
        # this most likely to fail since the returned question is random
    
    def test_failing_to_play_quiz(self):
        # since the specified method is not allowed
        res = self.client().get('/quizzes', json={'previous_questions':[], 'quiz_category':2})
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
