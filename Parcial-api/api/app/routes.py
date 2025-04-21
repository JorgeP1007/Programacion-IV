from flask import Blueprint, jsonify, request
from .data_loader import load_data

api_bp = Blueprint("api", __name__)
data = load_data()

@api_bp.route("/vaccination", methods=["GET"])
def get_all_data():
    return jsonify(data)

@api_bp.route("/vaccination/year/<int:year>", methods=["GET"])
def get_data_by_year(year):
    result = [entry for entry in data if entry["year"] == year]
    return jsonify(result)

@api_bp.route("/vaccination/region/<region>", methods=["GET"])
def get_data_by_region(region):
    result = [entry for entry in data if entry["region"].lower() == region.lower()]
    return jsonify(result)
