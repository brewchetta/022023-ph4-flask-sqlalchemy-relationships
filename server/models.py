from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class VideoGame(db.Model):
    __tablename__ = 'video_games'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    genre = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f'<VideoGame id={self.id} title={self.title} genre={self.genre}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'genre': self.genre,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @validates('title', 'genre')
    def validate_title(self, key, value):
        if len(value) == 0:
            raise KeyError(f'{key} cannot be empty')
        return value


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('score')
    def validate_score(self, key, score):
        if score > 10 or score < 0:
             raise ValueError('Score must be between 0 and 10')
        return score

    def __repr__(self):
        return f'<Review id={self.id} score={self.score}>'

    def to_dict(self):
        return {
            'id': self.id,
            'score': self.score
        }
