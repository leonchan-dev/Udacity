import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy import Column, DateTime, Integer, String
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')  
DB_USER = os.getenv('DB_USER', 'postgres')  
DB_PASSWORD = os.getenv('DB_PASSWORD', 'Projecta2008')  
DB_NAME = os.getenv('DB_NAME', 'castingagency')  
DB_PATH = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=DB_PATH):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

class Actors(db.Model):
    __tablename__ = 'Actors'

    id = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String)
    age = db.Column(db.String(120))
    gender = db.Column(db.String(120))
    
    def __repr__(self):
        return f'<actor id: {self.id}, name: {self.name}, age: {self.age}, gender: {self.gender}>'

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

class Movies(db.Model):
    __tablename__ = 'Movies'

    id = db.Column(db.Integer, primary_key=True)
    title  = db.Column(db.String)
    releaseDate = db.Column(db.String(120))

    def __repr__(self):
         return f'<movie id: {self.id}, title: {self.title}, releaseDate: {self.releaseDate}>'
    

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }
