from flask import Flask, request, abort, jsonify
from models import *

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

    questions = [question.format() for question in selection]
    current_movies = questions[start:end]

    return current_movies

MOVIES_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

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
                             'GET, PUT, POST, PATCH, DELETE, OPTIONS')
        return response
    '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
    @app.route('/actors')
    def get_actors():
        selection = Actors.query.order_by(Actors.id).all()
        current_actors = paginate_actors(request, selection)

        if len(current_actors) == 0:
            abort(404)

        return jsonify({
         'success': True,
         'actors': current_actors,
         'total_actors': len(Actors.query.all())
        })


    @app.route('/movies')
    def get_movies():
        selection = Movies.query.order_by(Movies.id).all()
        current_movies = paginate_movies(request, selection)

        if len(current_movies) == 0:
            abort(404)

        return jsonify({
         'success': True,
         'movies': current_movies,
         'total_movies': len(Movies.query.all())

        })

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    def delete_actor(actor_id):

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
    def delete_movie(movie_id):

        selection = Movies.query.order_by(Movies.id).all()
        current_movies = paginate_movies(request, selection)

        try:
            actor = Movies.query.filter(
                Movies.id == movie_id).one_or_none()

            if actor is None:
                abort(404)

            actor.delete()

            return jsonify({
                'success': True,
                'deleted': movie_id,
                'actors': current_movies,
                'total_actors': len(Movies.query.all())
                })

        except:
                abort(422)

    @app.route('/add-actor', methods=['POST'])
    def create_actor():
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

    @app.route('/add-movie', methods=['POST'])
    def create_movie():
        body = request.get_json()

        new_title = body.get('title', None)
        new_releaseDate = body.get('releaseDate', None)

        try:
          movie = Movies(title=new_title, release_date=new_releaseDate)
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
    def patch_actors(payload, actor_id):

        body = request.get_json()

        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        if new_name is None and new_age is None and new_gender is None:
            abort(422)

        try:
            actor = Actors.query.filter(
                Actors.id == actor_id).one_or_none()

            if actor is None:
                abort(404)    

            actor.update()

            selection = Actors.query.order_by(Actors.id).all()
            current_actors = paginate_actors(request, selection)

            return jsonify({
                'success': True,
                'actors': current_actors,
                'total_actors': len(Actors.query.all())
            })

        except:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    def patch_movies(payload, movie_id):

        body = request.get_json()

        new_title = body.get('title', None)
        new_releaseDate = body.get('releaseDate', None)

        if new_title is None and new_releaseDate is None:
            abort(422)

        try:
            movie = Movies.query.filter(
                Movies.id == movie_id).one_or_none()

            if movie is None:
                abort(404)  

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
    return app


app = create_app()