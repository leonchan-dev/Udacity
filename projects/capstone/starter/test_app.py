
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

        self.casting_assistant_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ill1M0dwWU1QMjlNSTFSd1FkUF8tTCJ9.eyJpc3MiOiJodHRwczovL2Rldi1md3dmbWUtai51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE5YTU0ZTFhZjA3YjMwMDcxODhiNTI3IiwiYXVkIjoiUm9sZXMiLCJpYXQiOjE2NDAyMjM3MTcsImV4cCI6MTY0MDMxMDExNywiYXpwIjoiZVZiTWlFaXdGQ21IOHdzYnN4YjQwM3hKWWJyaEpNd0ciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.eC6RHdZny2cPTDI3EUgYVpDeYTJTXPBzw1mvm7Kw1Ye7wtQNg-GiEa6_1foTQBgqA9LVNNB7u77q2qkq4-deozJ7Yn5dFfMmDMUukfmj4aqLFP0QkSQI-w4AIv0JS46lBExQTxRQqAOTPPQ_QKg9gXllI_VYp2RWfOJutwAO-fXmiPP5T5HrGDZeq9kBCbdGI3xd1GORN8ai9-SKj9mCuEmZtJe_O8IbMlJGCqjdg8YLfLEiSt3X6BRFKNgxCAjZGrtLUrMXfqcG6E6L8V-A4zYMixJFZbHF8c7SIueNBgBdMnjdIULAviqZ1HGRUOZ_2CnTpwB5uIpzhPn8Dw7_1w'
        self.casting_director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ill1M0dwWU1QMjlNSTFSd1FkUF8tTCJ9.eyJpc3MiOiJodHRwczovL2Rldi1md3dmbWUtai51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFjMGE3NjNmNjRkNGEwMDcyYjAwYjE4IiwiYXVkIjoiUm9sZXMiLCJpYXQiOjE2NDAyMjM4ODQsImV4cCI6MTY0MDMxMDI4NCwiYXpwIjoiZVZiTWlFaXdGQ21IOHdzYnN4YjQwM3hKWWJyaEpNd0ciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.f1qRG0frZn6jUAcAvsD-ys_LhDSO-Q-RHR5yBoaF583dsYBsEWrR9L1xM7W89RPHy6nKEJauf4-uqYM6dkI7KfOLzlndF-YGWUNd-X5mLGzfAasI40qj6ZQA2AyN17WAvSLe8JweAXTgt8k3VAFKt_ZfV8GXOaNTnPVB7v1QmNCYWJOgdoRXTG5LqLPJ4SDkiz97oTcztlLCENk_zZvK_QMK9ZPMk5WdDf_LPsed7xEe5Ym-NpaBLdVYXuGVSHKEmVfS5x1GQD7vp9BrLxDrHaRQt2k1QjQymzjAYAvIAS7hh-EJi2Z2LTaNxjn7YN3Z4fPTrn8FR_jXDNj7Fo85ww'
        self.executive_producer_token  = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ill1M0dwWU1QMjlNSTFSd1FkUF8tTCJ9.eyJpc3MiOiJodHRwczovL2Rldi1md3dmbWUtai51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE5YTRjNmFhYjc5YzkwMDcxM2M1YTY4IiwiYXVkIjoiUm9sZXMiLCJpYXQiOjE2NDAyMjM5OTAsImV4cCI6MTY0MDMxMDM5MCwiYXpwIjoiZVZiTWlFaXdGQ21IOHdzYnN4YjQwM3hKWWJyaEpNd0ciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.iM6t8Ih5SGSNi6oo6oobXB61INlXUOMr_pj-94YswWFqiHPzzdqIEVzm0OCpcVMzeb8o63a686sY6-IMVFLc8FMX3fvcd7eUWmvjKJFRE3XAdQPLmywT5Q5ihsu69HPG39htr2mbtfM2pQ4j_tpVd3sp50geJzZHab9pU0yqhIKTYU32W-owK8tShgtFiGeuBRJ47bl8kwsHKvfeTn_vilETRrmHsOFL-iLyWD1mT_H6PsuTTGdQmtiIlO8Tpi11PBZ2kp7vrBmLbN7xGedMLfOueIMIZCKohdeCE5r70b2Ca9QUCNYZv_i9V1fRFzFqgWMpAqEoRl_sORlNFYMomQ'

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
            'releaseDate': '2021-12-03'
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

    def test_404_sent_requestion_beyond_valid_page_actors_as_casting_assistant(self):
        res = self.client().get('/actors?page=1000', headers={
                "Authorization":
                    "Bearer {}".format(self.casting_assistant_token)
            })
        data = json.loads(res.data) 

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    

    def test_404_sent_requestion_beyond_valid_page_actors_as_casting_director(self):
        res = self.client().get('/actors?page=1000', headers={
                "Authorization":
                    "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data) 

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    def test_404_sent_requestion_beyond_valid_page_actors_as_executive_producer(self):
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

   # def test_delete_actor_correct_permission(self):
        #res = self.client().delete('/actors/6',json=self.new_actor, headers={
         #       "Authorization":
          #          "Bearer {}".format(self.casting_director_token)
           # })
        #data = json.loads(res.data)

      #  actor = Actors.query.filter(Actors.id == 6).one_or_none()

      #  self.assertEqual(res.status_code, 200)
      #  self.assertEqual(data['success'], True)
      #  self.assertEqual(data['deleted'], 6)
      #  self.assertTrue(data['total_actors'])
      #  self.assertEqual(actor, None)

    def test_delete_actor_incorrect_permission(self):
        res = self.client().delete('/actors/4',json=self.new_actor, headers={
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

 #   def test_patch_actors_correct_permission(self):
  #      res = self.client().patch('/actors/1', json=self.new_actor, headers={
  #              "Authorization":
  #                  "Bearer {}".format(self.casting_director_token)
  #          })
   #     data = json.loads(res.data)
#
    #    self.assertEqual(res.status_code, 200)
    #    self.assertEqual(data['success'], True)
    #    self.assertTrue(data['actors'])

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


  #  def test_delete_movie_correct_permission(self):
    #    res = self.client().delete('/movies/32', headers={
     #           "Authorization":
     #               "Bearer {}".format(self.executive_producer_token)
     #       })
     #   data = json.loads(res.data)

      #  movie = Movies.query.filter(Movies.id == 32).one_or_none()

       # self.assertEqual(res.status_code, 200)
       # self.assertEqual(data['success'], True)
       # self.assertEqual(data['deleted'], 32)
       # self.assertTrue(data['total_movies'])
       # self.assertEqual(movie, None)  

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

 #   def test_patch_movies_correct_permission(self):
  #      res = self.client().patch('/movies/1', json=self.new_movie, headers={
   #             "Authorization":
    #                "Bearer {}".format(self.casting_director_token)
     #       })
      #  data = json.loads(res.data)
#
 #       self.assertEqual(res.status_code, 200)
  #      self.assertEqual(data['success'], True)
   #     self.assertTrue(data['movies'])

    def test_patch_movies_incorrect_permission(self):
        res = self.client().patch('/movies/1', json=self.new_movie, headers={
                "Authorization":
                    "Bearer {}".format(self.casting_assistant_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')

    def test_fail_patch_movies(self):
        res = self.client().post('/movies/1',json=self.new_movie, headers={
                "Authorization":
                    "Bearer {}".format(self.executive_producer_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()