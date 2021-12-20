
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import *

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "castingagency_test"
        self.database_path = 'postgresql://postgres:Projecta2008@localhost:5432/castingagency'
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        
        self.new_actor = {
            'name': 'Test',
            'age': '20',
            'gender': 'Male'
        }    

        self.new_movie = {
            'title': 'Test',
            'releaseDate': '2021-12-03'
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_paginated_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors']) 
        self.assertTrue(len(data['actors'])) 
        
    def test_get_paginated_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies']) 
        self.assertTrue(len(data['movies'])) 

    def test_404_sent_requestion_beyond_valid_page_actors(self):
        res = self.client().get('/actors?page=1000')
        data = json.loads(res.data) 

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_404_sent_requestion_beyond_valid_page_movies(self):
        res = self.client().get('/movies?page=1000')
        data = json.loads(res.data) 

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors']) 
        self.assertTrue(len(data['actors'])) 
    
    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies']) 
        self.assertTrue(len(data['movies'])) 

    def test_fail_get_actors(self):
        res = self.client().post('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False) 

    def test_fail_get_movies(self):
        res = self.client().post('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False) 

   # def test_create_new_actor(self):
       # res = self.client().post('/add-actors', json=self.new_actor)
       # data = json.loads(res.data)

       # self.assertEqual(res.status_code, 200)
       # self.assertEqual(data['success'], True)
        #self.assertTrue(data['created'])
       # self.assertTrue(data['actors'])

    #def test_create_new_movie(self):
       # res = self.client().post('/add-movies', json=self.new_movie)
       # data = json.loads(res.data)

        #self.assertEqual(res.status_code, 200)
        #self.assertEqual(data['success'], True)
        #self.assertTrue(data['created'])
        #self.assertTrue(data['movies'])

    def test_fail_create_new_actor(self):
        res = self.client().get('/add-actors', json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False) 

    def test_fail_create_new_movie(self):
        res = self.client().get('/add-movies', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False) 

    def test_delete_actor(self):
        res = self.client().delete('/actors/4')
        data = json.loads(res.data)

        actor = Actors.query.filter(Actors.id == 4).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 4)
        self.assertTrue(data['total_actors'])
        self.assertEqual(actor, None)

    def test_delete_movie(self):
        res = self.client().delete('/movies/32')
        data = json.loads(res.data)

        movie = Movies.query.filter(Movies.id == 32).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 32)
        self.assertTrue(data['total_movies'])
        self.assertEqual(movie, None)  

    def test_fail_delete_actor(self):
        res = self.client().post('/actors/1', json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False) 

    def test_fail_delete_movie(self):
        res = self.client().post('/movies/1', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False) 

    def test_patch_actors(self):
        res = self.client().patch('/actors/12', json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_patch_movies(self):
        res = self.client().patch('/movies/1', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_fail_patch_actors_(self):
        res = self.client().post('/actors/12', json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    def test_fail_patch_movies(self):
        res = self.client().post('/movies/1',json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()