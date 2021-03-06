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


    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['categories']['1'], 'Science')
    
    # (to pass this) There should not be any categories in the database
    def test_failing_to_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        
    def test_get_paginated_questions(self):
        res = self.client().get('/questions/')
        data = json.loads(res.data)
        self.assertEqual(data['total_questions'], 10)

    # (to pass this) There should not be any questions
    def test_failing_to_get_questions(self):
        res = self.client().get('/questions/')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
            
    def test_post_new_question(self):
        res = self.client().post('/questions', json= {'question':'how do you do',
                                                      'answer': 'i am fine','difficulty': 4,'category': 1})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)

    def test_failing_to_post_question(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        
    def test_search_questions(self):
        res = self.client().post('/search', json={'searchTerm': 'soccer'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_questions'], 2)
        self.assertTrue(data['success'])
        
    def test_failing_search_questions(self):
        # As There is no json object contains searchTerm
        res = self.client().post('/search')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
                
    def test_delete_question(self):
        # the passed id should exist in the database
        res = self.client().delete('/questions/56')
        data = json.loads(res.data)
        self.assertTrue(data['success'])
    
    def test_failing_to_delete_question(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
    
    def test_get_specific_category_question(self):
        res = self.client().get('/categories/4/questions')
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_questions'], 3)
        
    def test_failing_to_get_specific_category_question(self):
        res = self.client().get('/categories/33/questions')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)
        
    #add section for testing
    def test_quiz_play(self):
        res = self.client().post('/quizzes', json={'previous_questions':[], 'quiz_category':{'id':2} })
        data = json.loads(res.data)
        self.assertTrue(data['success'])
    
    def test_failing_to_play_quiz(self):
        # since the specified method is not allowed
        res = self.client().get('/quizzes', json={'previous_questions':[], 'quiz_category':2})
        data = json.loads(res.data)
        self.assertEqual(data['error'], 405)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
