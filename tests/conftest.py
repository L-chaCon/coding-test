import os
import tempfile

import pytest

from populate_db import load_stores
from task.app import create_app


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app(test_config={
        "DEBUG": True,
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}"
    })
    # print(db_fd, db_path)
    with app.app_context():
        load_stores('data/stores.json')
    yield app
    os.close(db_fd)
    os.unlink(db_path)
