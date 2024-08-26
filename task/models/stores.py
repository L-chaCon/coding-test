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


def get_stores(stores: list[str] = []) -> list[Stores]:
    """
    By default gets all stores, a list of postcodes to only get the stores with that
    postcode
    """
    if not stores:
        try:
            store_list = Stores.query.all()
        except:
            raise Exception()
    else:
        try:
            store_list = Stores.query.filter(Stores.postcode.in_(stores)).all()
        except:
            raise Exception()
    return store_list 


def update_postcode_stores_in_bulk(update_data: list[dict]) -> None:
    try:
        for data in update_data:
            store = Stores.query.filter_by(id=data['id']).first()
            if store:
                store.postcode = data['postcode']
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Fail to update Stores: {e}")
    finally:
        db.session.close()


def update_lat_long_stores_in_bulk(update_data: list[dict]) -> None:
    try:
        for data in update_data:
            store = Stores.query.filter_by(id=data['id']).first()
            if store:
                store.latitude = data['latitude']
                store.longitude = data['longitude']
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Fail to update Stores: {e}")
    finally:
        db.session.close()


def sort_stores_north_to_south(stores: list[Stores]) -> list[Stores]:
    try:
        postcodes = [store.postcode for store in stores]
        store_list =  Stores.query.filter(Stores.postcode.in_(postcodes)).order_by(desc(Stores.latitude)).all()
    except:
        raise Exception()
    return store_list 
