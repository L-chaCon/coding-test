import os

import pytest

from task.app import create_app


@pytest.fixture
def app():
    basedir = os.path.abspath(os.path.dirname(__file__))
    app = create_app(test_config={
        "DEBUG": True,
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{os.path.join(basedir, "test.sqlite")}"
    })
    return app
