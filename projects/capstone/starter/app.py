from flask import Flask, request, abort, jsonify
from models import *
from flask_cors import CORS
from auth import AuthError, requires_auth


def paginate_actors(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ACTORS_PER_PAGE
    end = start + ACTORS_PER_PAGE

    actors = [actor.format() for actor in selection]
    current_actors = actors[start:end]

    return current_actors


ACTORS_PER_PAGE = 10


def paginate_movies(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * MOVIES_PER_PAGE
    end = start + MOVIES_PER_PAGE

    movies = [movie.format() for movie in selection]
    current_movies = movies[start:end]

    return current_movies


MOVIES_PER_PAGE = 10


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    '''
  @TODO: Set up CORS. Allow '*' for origins.
  '''

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        selection = Actors.query.order_by(Actors.id).all()
        current_actors = paginate_actors(request, selection)

        if len(current_actors) == 0:
            abort(404)

        return jsonify({
         'success': True,
         'actors': current_actors,
         'total_actors': len(Actors.query.all())
        })

    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth('get:actors')
    def get_actor(payload, actor_id):

        actor = Actors.query.filter(Actors.id == actor_id).one_or_none()

        if (actor is None):
            abort(404)

        try:

            return jsonify({
                "success": True,
                "actor": actor.format()
            })

        except:
            abort(422)

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        selection = Movies.query.order_by(Movies.id).all()
        current_movies = paginate_movies(request, selection)

        if len(current_movies) == 0:
            abort(404)

        return jsonify({
         'success': True,
         'movies': current_movies,
         'total_movies': len(Movies.query.all())

        })

    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth('get:movies')
    def get_movie(payload, movie_id):

        movie = Movies.query.filter(Movies.id == movie_id).one_or_none()

        if (movie is None):
            abort(404)

        try:

            return jsonify({
                "success": True,
                "movie": movie.format(),
            })

        except:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):

        selection = Actors.query.order_by(Actors.id).all()
        current_actors = paginate_actors(request, selection)

        try:
            actor = Actors.query.filter(
                Actors.id == actor_id).one_or_none()

            if actor is None:
                abort(404)

            actor.delete()

            return jsonify({
                'success': True,
                'deleted': actor_id,
                'actors': current_actors,
                'total_actors': len(Actors.query.all())
                })

        except:
                abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):

        selection = Movies.query.order_by(Movies.id).all()
        current_movies = paginate_movies(request, selection)

        try:
            movie = Movies.query.filter(
                Movies.id == movie_id).one_or_none()

            if movie is None:
                abort(404)

            movie.delete()

            return jsonify({
                'success': True,
                'deleted': movie_id,
                'movies': current_movies,
                'total_movies': len(Movies.query.all())
                })

        except:
                abort(422)

    @app.route('/add-actors', methods=['POST'])
    @requires_auth("post:actors")
    def create_actor(payload):
        body = request.get_json()

        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        try:
            actor = Actors(name=new_name, age=new_age,
                           gender=new_gender)
            actor.insert()

            selection = Actors.query.all()
            current_actors = paginate_actors(request, selection)

            return jsonify({
              'success': True,
              'created': actor.id,
              'actors': current_actors,
              'total_actors': len(Actors.query.all())
            })

        except:
            abort(422)

    @app.route('/add-movies', methods=['POST'])
    @requires_auth("post:movies")
    def create_movie(payload):
        body = request.get_json()

        new_title = body.get('title', None)
        new_releaseDate = body.get('releaseDate', None)

        try:
            movie = Movies(title=new_title,
                           releaseDate=new_releaseDate)

            movie.insert()
            selection = Movies.query.all()
            current_movies = paginate_movies(request, selection)

            return jsonify({
              'success': True,
              'created': movie.id,
              'movies': current_movies,
              'total_movies': len(Movies.query.all())
            })

        except:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def patch_actors(payload, actor_id):

        selection = Actors.query.order_by(Actors.id).all()
        current_actors = paginate_actors(request, selection)

        body = request.get_json()

        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        if new_name is None and new_age is None and new_gender is None:
            abort(422)

        try:
            actor = Actors.query.filter(
                Actors.id == actor_id).one_or_none()

            actor.name = new_name
            actor.age = new_age
            actor.gender = new_gender

            actor.update()

            return jsonify({
                'success': True,
                'actors': current_actors,
                'total_actors': len(Actors.query.all())
            })

        except:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def patch_movies(payload, movie_id):

        body = request.get_json()

        new_title = body.get('title', None)
        new_releaseDate = body.get('releaseDate', None)

        if new_title is None and new_releaseDate is None:
            abort(422)

        try:
            movie = Movies.query.filter(
                Movies.id == movie_id).one_or_none()

            movie.title = new_title
            movie.release_date = new_releaseDate

            movie.update()

            selection = Movies.query.order_by(Movies.id).all()
            current_movies = paginate_movies(request, selection)

            return jsonify({
                'success': True,
                'movies': current_movies,
                'total_movies': len(Movies.query.all())
            })

        except:
            abort(422)

    '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
    '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
          }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
          }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
          }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
          }), 405

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "error": 500,
            "message": "server error"
          }), 500

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        """
        Receive the raised authorization error and propagates it as response
        """
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response
    return app


app = create_app()
