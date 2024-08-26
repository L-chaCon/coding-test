import os

from flask import Flask

from task.extencions import db
from task.routes.stores import stores_routes


def create_app(test_config=None):
    app = Flask(__name__)
    # BASE CONFIG
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{}".format(os.path.join(basedir, "task.sqlite"))
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(stores_routes)

    return app

app = create_app()
