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
        self.database_path = "postgres://{}/{}".format('localhost:5432',
                                                        self.database_name
                                                        )

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
    Write at least one test for each test for
    successful operation and for expected errors.
    """
    # Question Test
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Category Test
    def test_retrieve_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data["categories"]))

    def test_retrieve_categories_id(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/categories/200/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Delete Question
    def test_delete_question(self):
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)
        #question = Question.query.filter(Question.id == 2).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        #self.assertEqual(data['deleted'], 2)
        #self.assertEqual(question, None)

    def test_422_if_question_does_not_exist(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # Search Question
    def test_search_question(self):
        post_data = {'searchTerm': 'name'}
        res = self.client().post('/questions/search', json=post_data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data['questions']))

    # Add New Question
    def test_correct_add_new_question(self):
        n_data = {
            "question": "What .... ?",
            "answer": "answer",
            "category": 4,
            "difficulty": 3}
        res = self.client().post('/questions', json=n_data)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)

    def test_bad_request_add_new_question(self):
        n_data = {
            "question": "What .... ?",
            "answer": "answer",
            "category": 4,
            "difficulty": 3}
        res = self.client().post('/questions/100', json=n_data)
        data = res.get_json()
        self.assertEqual(res.status_code, 405)
        self.assertFalse(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # Play quiz
    def test_play_quiz(self):
        post_data = {
            'previous_questions': [],
            'quiz_category': {
                'type': 'History',
                'id': 4}}
        res = self.client().post('/quizzes', json=post_data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_422_play_quiz(self):
        post_data = {
            'quiz_category': {
                'type': 'History',
                'id': 4}}
        res = self.client().post('/quizzes', json=post_data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'unprocessable')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
