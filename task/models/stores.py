from task.extencions import db


class Stores(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postcode = db.Column(db.String)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    def __init__(self, name, postcode):
        self.name = name
        self.postcode = postcode
        self.latitude = None
        self.longitude = None

    def __repr__(self):
        return f"<Store {self.postcode}>"

    def __str__(self):
        return f"{self.name}, {self.postcode}"


def get_all_stores_in_alphabetical_order() -> list[Stores]:
    try:
        all_stores_order_by_name = Stores.query.order_by(Stores.name).all()
    except:
        raise Exception()
    return all_stores_order_by_name
