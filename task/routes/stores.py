from flask import Blueprint, jsonify, render_template

stores_routes = Blueprint('stores_routes', __name__)

@stores_routes.route('/status')
def status():
    return jsonify({'status': 'OK'}), 200

@stores_routes.route('/')
def welcome():
    return render_template("welcome.html")

@stores_routes.route('/stores')
def stores():
    return render_template("stores.html")
