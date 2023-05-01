#!/usr/bin/env python3

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import exc

from models import db, Review, VideoGame

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.get('/')
def index():
    return "Index for VideoGame/Review API"

# GAMES #

@app.get('/videogames')
def all_games():
    games = VideoGame.query.all()
    games_to_dict = [game.to_dict() for game in games]
    return games_to_dict, 200


@app.get('/reviews')
def all_reviews():
    revs = Review.query.all()
    return [rev.to_dict() for rev in revs], 200


@app.post('/videogames')
def create_game():
    try:
        data = request.json
        new_vg = VideoGame(title=data['title'], genre=data['genre'])
        db.session.add(new_vg)
        db.session.commit()
        return new_vg.to_dict(), 201
    except KeyError as e:
        return { 'error': str(e) }
    except exc.IntegrityError as e:
        return {'error': str(e)}


@app.post('/reviews')
def create_review():
    data = request.json
    new_review = Review(
        score=data["score"],
        game_id=data["game_id"]
    )

    db.session.add(new_review)
    db.session.commit()

    return new_review.to_dict(), 201


@app.get('/videogames/<int:id>')
def game_by_id(id):
    try:
        game = VideoGame.query.where(VideoGame.id == id).first()
        return game.to_dict(), 200
    except AttributeError:
        return {'message': 'No game found'}, 404


@app.patch('/videogames/<int:id>')
def patch_game(id):
    data = request.json
    game = VideoGame.query.where(VideoGame.id == id).update(data)
    db.session.commit()

    updated_game = VideoGame.query.where(VideoGame.id == id).first()

    return updated_game.to_dict(), 202


@app.delete('/videogames/<int:id>')
def delete_game(id):
    game = VideoGame.query.where(VideoGame.id == id).first()
    if game:
        db.session.delete(game)
        db.session.commit()
        return {}, 204
    else:
        return {'message': 'No game found'}, 404


if __name__ == '__main__':
    app.run(port=5555, debug=True)
