from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    year = db.Column(db.Integer)
    country = db.Column(db.String(120))
    director = db.Column(db.String(120))
    genre = db.Column(db.String(120))
    actors = db.relationship('Actors', secondary='movies_actors', backref="movie", lazy=True)

    def __repr__(self):
        return f'{self.title}'


class Actors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    movies = db.relationship('Movies', secondary='movies_actors', backref="actor", lazy=True)

    def __repr__(self):
        return f'{self.name}'


class MoviesActors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'))

    def __repr__(self):
        return f'{self.name}'
