import json

from task.app import create_app
from task.extencions import db
from task.models.stores import Stores


def load_stores(filepath):
    with open(filepath) as f:
        stores = json.load(f)
        for store in stores:
            new_store = Stores(name=store['name'], postcode=store['postcode'])
            db.session.add(new_store)
        db.session.commit()


def populate_db():
    app = create_app()
    with app.app_context():
        load_stores('data/stores.json')


if __name__ == "__main__":
    populate_db()
