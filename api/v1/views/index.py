from api.v1.views import app_views
from flask import jsonify
from models import storage

class_type = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}

@app_views.route('/status')
def status():
    """returns a JSON status Ok"""
    return jsonify({"status": "OK"})

@app_views.route('/stats')
def stat():
    """retrieves the number of each objects by type"""
    dict = {}
    for key, value in class_type.items():
        dict[key] = storage.count(value)
    return jsonify(dict)