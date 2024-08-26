from flask import Blueprint, jsonify, render_template

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
