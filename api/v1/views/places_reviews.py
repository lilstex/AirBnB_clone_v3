#!/usr/bin/python3
"""
New view for Review object that handles default Restful API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.review import Review
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def getAllReviews(place_id):
    """retrieves the list of all Review objects of a Place"""
    reviews = []
    all_reviews = storage.all('Review')
    get_place = storage.get("Place", place_id)
    if get_place is None:
        abort(404)

    for review in all_reviews.values():
        if review.place_id == place_id:
            reviews.append(review.to_dict())

    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def getReview(review_id):
    """retrives a review object"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def DEL_review(review_id):
    """deletes a review"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()
    storage.close()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def POST_review(place_id):
    """creates a review object"""
    if not request.is_json():
        abort(400, "Not a JSON")
    if 'user_id' not in request.is_json():
        abort(400, "Missing user_id")
    if 'text' not in request.is_json():
        abort(400, "Missing text")

    user = storage.get("User", request.is_json().get('user_id'))
    if user is None:
        abort(404)

    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    new_review = Review(**request.is_json())
    new_review.place_id = place_id
    storage.new(new_review)
    new_review.save()
    storage.close()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def PUT_review(review_id):
    """updates a review object"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    if not request.is_json():
        abort(400, "Not a JSON")

    for key, val in request.is_json().items():
        if key not in ["id", "place_id", "user_id", "created_at", "updated_at"]:
            setattr(review, key, val)
    storage.save(review)
    storage.close()
    return jsonify(review.to_dict()), 200