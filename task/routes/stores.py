from flask import Blueprint, jsonify, render_template

from task.lib.stores import (clean_postcode_in_database,
                             update_lat_long_of_stores)
from task.models.stores import get_all_stores_in_alphabetical_order

stores_routes = Blueprint('stores_routes', __name__)

@stores_routes.route('/status')
def status():
    return jsonify({'status': 'OK'}), 200

@stores_routes.route('/')
def welcome():
    return render_template("welcome.html")

@stores_routes.route('/stores')
def stores():
    stores = get_all_stores_in_alphabetical_order()
    return render_template("stores.html", stores = stores)

@stores_routes.route('/stores/clean')
def store_clean_data():
    clean = clean_postcode_in_database()
    if clean:
        message = "Database postcodes cleaned"
    else:
        message = "Not able to clean database"
    stores = get_all_stores_in_alphabetical_order()
    return render_template('stores.html', stores = stores, message = message)

@stores_routes.route('/stores/calculate_lat_long')
def calculate_lat_long():
    try:
        updated = update_lat_long_of_stores()
        if updated:
            message = "Latitude and Longitude Updated"
        else:
            message = "Not able to update"
    except:
        message = "Fail to update, try cleaning the database"
    stores = get_all_stores_in_alphabetical_order()
    return render_template("stores.html", stores = stores, message = message)

