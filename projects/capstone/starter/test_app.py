
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

        self.casting_assistant_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ill1M0dwWU1QMjlNSTFSd1FkUF8tTCJ9.eyJpc3MiOiJodHRwczovL2Rldi1md3dmbWUtai51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE5YTU0ZTFhZjA3YjMwMDcxODhiNTI3IiwiYXVkIjoiUm9sZXMiLCJpYXQiOjE2NDA3MDgzMTEsImV4cCI6MTY0MDc5NDcxMSwiYXpwIjoiZVZiTWlFaXdGQ21IOHdzYnN4YjQwM3hKWWJyaEpNd0ciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.FM0dt-fH44eA2ACMHu3ghq2RtBAGP9HjCYZOX-C_I51nlaNJ84srlh5H_61LjtYiRibO8hNhyL2F0JiidkxgeI5NO_yG-G0D1xWsg_gUlOKbnRRGWLfX7hMLuZ5nBhogcjQLkjJt6MMFlyeRmmApE4XpqFmjJQLciGJXX6R3i3uGpxgBWJoERQh54PLgkz4YEholl34AxiUTAnxcKmPFXMC_8fo6h4mRdPm2BWbkR1ZpReyoSJkOf_0rLovZYcSS9kQpTDwQmeoEuFMYxvEV5vqNRb6X1jLPmMI8vsQPgDtWCCA_KmypeC3G01ao9JX13_EJr2CxC9FXW7AikeVgwg'
        self.casting_director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ill1M0dwWU1QMjlNSTFSd1FkUF8tTCJ9.eyJpc3MiOiJodHRwczovL2Rldi1md3dmbWUtai51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFjMGE3NjNmNjRkNGEwMDcyYjAwYjE4IiwiYXVkIjoiUm9sZXMiLCJpYXQiOjE2NDA3MDgyNDgsImV4cCI6MTY0MDc5NDY0OCwiYXpwIjoiZVZiTWlFaXdGQ21IOHdzYnN4YjQwM3hKWWJyaEpNd0ciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.HU1_g9gWEQkMDo6piGvQZHWFpuQcnrR2wTa2u2X39dz4iPVrcvtw-XRla17czrw99yOLik-jRxWgcJ93fNYS5pxwO_fONWqvqdOl0zrd130z8fvF_Oui7zFZ3mmVmfMvxWSsa1_F1cTpgHAgXBy1Q_WajY5S_OUSouU1ZqMwtwBvcra2vmwXfT2ehyArz7GSKMzJT-NiCz4JTbbwi-Fw7QcuvVFyDh1aBlw3mkMGP6Yphhh5BiRMF9cgqfMVhlok3z4La4T-lKx05LcY_eXO-pvwo-1SOxZqCP3xOB3HqbJZwoBlBiz4pVV5lP4IMcCjanNA9aDknRQTNHgE83Ycyw'
        self.executive_producer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ill1M0dwWU1QMjlNSTFSd1FkUF8tTCJ9.eyJpc3MiOiJodHRwczovL2Rldi1md3dmbWUtai51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE5YTRjNmFhYjc5YzkwMDcxM2M1YTY4IiwiYXVkIjoiUm9sZXMiLCJpYXQiOjE2NDA3MDgzODcsImV4cCI6MTY0MDc5NDc4NywiYXpwIjoiZVZiTWlFaXdGQ21IOHdzYnN4YjQwM3hKWWJyaEpNd0ciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.qiMdZNMaStSFm-zAVJQyc2Hcq1grqSgfqTypjTsPr8oWbzVMF6EdWfd4orW5fnt0keJ8F5QqiC8wSL65MMkGd5-kOw9DIc5BWIYJUsPkV0R7bXV3rZit6xWeZrlyD9E1MuD3u437xD2AfGh-fuV0rJstPteMTRsvW8uCLbKZIxB_NcLEtNTMuR8NrLuohAwk-o257TvtHWHrV37WOMkxIrbIJQJeDkIVU4w9PXaY4T9wNGunBegc1sNaNd1vhDRUULMNO5UADSSlWcQfY_CddqNJ-3u00OyY2gNTR-yOQ3zFoOmdBjQD7ouuZFJS6do9kK1Aixxw_JdEKZG7fHpv5g'

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
        res = self.client().delete('/actors/34', headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)

        actor = Actors.query.filter(Actors.id == 34).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 34)
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
        res = self.client().delete('/movies/52', headers={
                "Authorization":
                "Bearer {}".format(self.executive_producer_token)
            })
        data = json.loads(res.data)

        movie = Movies.query.filter(Movies.id == 52).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 52)
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
