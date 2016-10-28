from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Game(db.Model):
    """Board game."""

    __tablename__ = "games"
    game_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.String(100))


def connect_to_db(app, db_uri="postgresql:///games"):
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.app = app
    db.init_app(app)


def example_data():
    """Create example data for the test database."""
    
    lipsync = Game(name="Lip Sync Battle", description="sing and dance to whatever you want. whoever has the most fun wins!")
    trivia = Game(name="Trivia Night", description="test your knowledge to useless questions and drink")
    balloonicorn = Game(name="Worship balloonicorn", description="shower me with gifts and love!!!<3")

    db.session.add_all([lipsync, trivia, balloonicorn])
    db.session.commit()


if __name__ == '__main__':
    from server import app

    connect_to_db(app)
    print "Connected to DB."
 