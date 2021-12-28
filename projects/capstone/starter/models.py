import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy import Column, DateTime, Integer, String
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'castingagency')
DB_PATH = os.getenv('DATABASE_PATH_1','postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME))
db = SQLAlchemy()


def setup_db(app, database_path=DB_PATH):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def db_create_all():
    db.create_all()


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


def create_dummy_data():
    actor1 = Actors(name='1', age=20, gender='Male')
    actor1.insert()
    actor2 = Actors(name='2', age=30, gender='Female')
    actor2.insert()
    actor3 = Actors(name='3', age=40, gender='Female')
    actor3.insert()
    movie1 = Movies(title='Movie1', releaseDate='2021-12-01')
    movie1.insert()
    movie2 = Movies(title='Movie2', releaseDate='2021-12-021')
    movie2.insert()
    movie3 = Movies(title='Movie3', releaseDate='2021-12-03')
    movie3.insert()


class Actors(db.Model):
    __tablename__ = 'Actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(120))

    def __repr__(self):
        return f'<Actors id: {self.id}, name: {self.name}, age: {self.age}, gender: {self.gender}>'

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
    title = db.Column(db.String)
    releaseDate = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Movies id: {self.id}, title: {self.title}, releaseDate: {self.releaseDate}>'

    def __init__(self, title, releaseDate):
        self.title = title
        self.releaseDate = releaseDate

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
            'releaseDate': self.releaseDate
        }
