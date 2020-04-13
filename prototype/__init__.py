from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from os import environ
from sqlalchemy import event

db = SQLAlchemy()



def create_app():
    """Construct the core application."""

    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    db.init_app(app)

    engine = create_engine(environ.get('SQLALCHEMY_DATABASE_URI'))

    def _fk_pragma_on_connect(dbapi_con, con_record):
        dbapi_con.execute('pragma foreign_keys=ON')

    event.listen(engine, 'connect', _fk_pragma_on_connect)

    with app.app_context():
        from . import routes

        # Create tables for our models
        db.create_all()

        return app