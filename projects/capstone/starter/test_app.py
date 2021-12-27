
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import *


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case TESTING"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "castingagency_test"
        self.database_path = 'postgresql://postgres:Projecta2008@localhost:5432/castingagency'
        setup_db(self.app, self.database_path)

        self.casting_assistant_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ill1M0dwWU1QMjlNSTFSd1FkUF8tTCJ9.eyJpc3MiOiJodHRwczovL2Rldi1md3dmbWUtai51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE5YTU0ZTFhZjA3YjMwMDcxODhiNTI3IiwiYXVkIjoiUm9sZXMiLCJpYXQiOjE2NDA2MTI3NTgsImV4cCI6MTY0MDY5OTE1OCwiYXpwIjoiZVZiTWlFaXdGQ21IOHdzYnN4YjQwM3hKWWJyaEpNd0ciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.Vo3pSQ83aMyekpV3ANMBKvVsSOfiDBTePgKHt4SgxZg_olfTP-F8-YsznMqYu3-6Cw7oGOTn6seUkZrjAj6lbigKSWPlq9PT9LZZNEv_a5ahTqUZXGj0qJkMN4gOP8Torq9PWOxmUa8s0JyYsajNV9kAV47vhIuQOuYscCFjq6BOA9HPZpjO9rXtlIRig9hxeBla3YcMzkeqC3Z1mjF94nXXIJwjM5LjKYcHDfJfCJTRwMlnUFD9d2-YAGRxiEwQoxcNCdDzjKHq9X9CacdnI386I6edaNfGDDpOEBu1iLxn6AqDA3vBhlkoeAYczNmqGJJz18JvoSdLCmFhR4Iq4g'
        self.casting_director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ill1M0dwWU1QMjlNSTFSd1FkUF8tTCJ9.eyJpc3MiOiJodHRwczovL2Rldi1md3dmbWUtai51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFjMGE3NjNmNjRkNGEwMDcyYjAwYjE4IiwiYXVkIjoiUm9sZXMiLCJpYXQiOjE2NDA2MTI3MTEsImV4cCI6MTY0MDY5OTExMSwiYXpwIjoiZVZiTWlFaXdGQ21IOHdzYnN4YjQwM3hKWWJyaEpNd0ciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.awEJI2w3HnU7Kx5pbECPpY8f9pSIP76CWebZEoKYeaQZ1ivp9GNMr6nH5IyEVKHlMRHjnBlNuvfrvsU8uwg7qRdowCk4rAnv0zCCUBOv9fMlLbJOni09El-y-3imZDA4lLFPnRw7ZOmcGoKqGrXkHOfH2-ttCyaGX6-yjeO5dbHFpZXvCa7sygjsvkFIiHoRyfv8eHkZI7UQCY6LKyK9ycipPhNYbriW2hupEzSyjvJVSVXvm3TcoC58QKRkTsMGiczkk8Hd2LVa8rUyMONWXc1-RVx1lUfa9vRMqHdlD__-AR3v_7bRpw6sfbe3yYeXq_4PGkVnWIurebb1kGPc8g'
        self.executive_producer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ill1M0dwWU1QMjlNSTFSd1FkUF8tTCJ9.eyJpc3MiOiJodHRwczovL2Rldi1md3dmbWUtai51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE5YTRjNmFhYjc5YzkwMDcxM2M1YTY4IiwiYXVkIjoiUm9sZXMiLCJpYXQiOjE2NDA2MTI4MDMsImV4cCI6MTY0MDY5OTIwMywiYXpwIjoiZVZiTWlFaXdGQ21IOHdzYnN4YjQwM3hKWWJyaEpNd0ciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.NAhPzzfhdV9-ZP4aLhKgU42fkV8kBqBPgui0JSNqLBnVW-BVoJRw2JbCqoMrNWyKoFOfgUvl0zfYJIO4b7KaSEDlrrHMTch5u7FV25HipfWkeF2Fg0NaKq78oIZgWDwunx0JryaYYhjfcIWjdF4DUWUiwyt4RU8QaktaG-GMiFH3HePHA4Un3Nxb6K1xhTarssHFhmM2v9H22nIDJMUz0WHtOoRRhlBgU8t8sSJt0XcZ1l5m-JyQAHFj32-d_MLtpkQ1oaJarVmDVGudbi7DQapxIdFb54soN72v4GWR7uUE42kyN3l6bbYOKwF7CbAw0Iuc4WTy0uyafPfB9nZJrw'

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_actor = {
            'name': 'Test1',
            'age': '20',
            'gender': 'Male'
        }

        self.new_movie = {
            'title': 'Test',
            'releaseDate': '2021-12-03 00:00:00'
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_paginated_actors_as_casting_assistant(self):
        res = self.client().get('/actors', headers={
                "Authorization":
                "Bearer {}".format(self.casting_assistant_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    def test_get_paginated_actors_as_casting_director(self):
        res = self.client().get('/actors', headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    def test_get_paginated_actors_as_executive_producer(self):
        res = self.client().get('/actors', headers={
                "Authorization":
                "Bearer {}".format(self.executive_producer_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    def test_404_sent_requestion_beyond_valid_page_actors_as_CA(self):
        res = self.client().get('/actors?page=1000', headers={
                "Authorization":
                "Bearer {}".format(self.casting_assistant_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_404_sent_requestion_beyond_valid_page_actors_as_CD(self):
        res = self.client().get('/actors?page=1000', headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_404_sent_requestion_beyond_valid_page_actors_as_EP(self):
        res = self.client().get('/actors?page=1000', headers={
                "Authorization":
                "Bearer {}".format(self.executive_producer_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_actors_as_casting_assistant(self):
        res = self.client().get('/actors', headers={
                "Authorization":
                "Bearer {}".format(self.casting_assistant_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    def test_get_actors_as_casting_director(self):
        res = self.client().get('/actors', headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    def test_get_actors_as_executive_producer(self):
        res = self.client().get('/actors', headers={
                "Authorization":
                "Bearer {}".format(self.executive_producer_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    def test_fail_get_actors_as_casting_assistant(self):
        res = self.client().post('/actors', headers={
                "Authorization":
                "Bearer {}".format(self.casting_assistant_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    def test_fail_get_actors_as_casting_director(self):
        res = self.client().post('/actors', headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    def test_fail_get_actors_as_executive_producer(self):
        res = self.client().post('/actors', headers={
                "Authorization":
                "Bearer {}".format(self.executive_producer_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    def test_create_new_actor_correct_permission(self):
        res = self.client().post('/add-actors', json=self.new_actor, headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['actors'])

    def test_create_new_actor_incorrect_permission(self):
        res = self.client().post('/add-actors', json=self.new_actor, headers={
                "Authorization":
                "Bearer {}".format(self.casting_assistant_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')

    def test_fail_create_new_actor(self):
        res = self.client().get('/add-actors', json=self.new_actor, headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    def test_delete_actor_correct_permission(self):
        res = self.client().delete('/actors/28', headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)

        actor = Actors.query.filter(Actors.id == 28).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 28)
        self.assertTrue(data['total_actors'])
        self.assertEqual(actor, None)

    def test_delete_actor_incorrect_permission(self):
        res = self.client().delete('/actors/4', json=self.new_actor, headers={
                "Authorization":
                "Bearer {}".format(self.casting_assistant_token)
            })
        data = json.loads(res.data)

        actor = Actors.query.filter(Actors.id == 4).one_or_none()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')

    def test_fail_delete_actor(self):
        res = self.client().post('/actors/1', json=self.new_actor, headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    def test_patch_actors_correct_permission(self):
        res = self.client().patch('/actors/1', json=self.new_actor, headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_patch_actors_incorrect_permission(self):
        res = self.client().patch('/actors/1', json=self.new_actor, headers={
                "Authorization":
                "Bearer {}".format(self.casting_assistant_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')

    def test_fail_patch_actors_(self):
        res = self.client().post('/actors/12', json=self.new_actor, headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    def test_get_paginated_movies_as_casting_assistant(self):
        res = self.client().get('/movies', headers={
                "Authorization":
                "Bearer {}".format(self.casting_assistant_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    def test_get_paginated_movies_as_casting_director(self):
        res = self.client().get('/movies', headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    def test_get_paginated_movies_as_executive_producer(self):
        res = self.client().get('/movies', headers={
                "Authorization":
                "Bearer {}".format(self.executive_producer_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    def test_404_sent_requestion_beyond_valid_page_movies_as_casting_assistant(self):
        res = self.client().get('/movies?page=1000', headers={
                "Authorization":
                "Bearer {}".format(self.casting_assistant_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_404_sent_requestion_beyond_valid_page_movies_as_casting_director(self):
        res = self.client().get('/movies?page=1000', headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_404_sent_requestion_beyond_valid_page_movies_as_executive_producer(self):
        res = self.client().get('/movies?page=1000', headers={
                "Authorization":
                "Bearer {}".format(self.executive_producer_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_movies_as_casting_assistant(self):
        res = self.client().get('/movies', headers={
                "Authorization":
                "Bearer {}".format(self.casting_assistant_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    def test_get_movies_as_casting_director(self):
        res = self.client().get('/movies', headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    def test_get_movies_as_executive_producer(self):
        res = self.client().get('/movies', headers={
                "Authorization":
                "Bearer {}".format(self.executive_producer_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    def test_fail_get_movies_correct_permission(self):
        res = self.client().post('/movies', headers={
                "Authorization":
                "Bearer {}".format(self.executive_producer_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    def test_create_new_movie_correct_permission(self):
        res = self.client().post('/add-movies', json=self.new_movie, headers={
                "Authorization":
                "Bearer {}".format(self.executive_producer_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['movies'])

    def test_create_new_movie_incorrect_permission(self):
        res = self.client().post('/add-movies', json=self.new_movie, headers={
                "Authorization":
                "Bearer {}".format(self.casting_assistant_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')

    def test_fail_create_new_movie(self):
        res = self.client().get('/add-movies', json=self.new_movie, headers={
                "Authorization":
                "Bearer {}".format(self.executive_producer_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    def test_delete_movie_correct_permission(self):
        res = self.client().delete('/movies/45', headers={
                "Authorization":
                "Bearer {}".format(self.executive_producer_token)
            })
        data = json.loads(res.data)

        movie = Movies.query.filter(Movies.id == 45).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 45)
        self.assertTrue(data['total_movies'])
        self.assertEqual(movie, None)

    def test_delete_movie_incorrect_permission(self):
        res = self.client().delete('/movies/32', headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)

        movie = Movies.query.filter(Movies.id == 32).one_or_none()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')

    def test_fail_delete_movie(self):
        res = self.client().post('/movies/1', json=self.new_movie, headers={
                "Authorization":
                "Bearer {}".format(self.executive_producer_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    def test_patch_movies_correct_permission(self):
        res = self.client().patch('/movies/1', json=self.new_movie, headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_patch_movies_incorrect_permission(self):
        res = self.client().patch('/movies/1', json=self.new_movie, headers={
                "Authorization":
                "Bearer {}".format(self.casting_assistant_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')

    def test_fail_patch_movies(self):
        res = self.client().post('/movies/1', json=self.new_movie, headers={
                "Authorization":
                "Bearer {}".format(self.executive_producer_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
