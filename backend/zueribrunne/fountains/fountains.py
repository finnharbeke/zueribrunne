import csv
from flask import Blueprint, jsonify
from flask_login import current_user, login_required

from zueribrunne import db

fountains = Blueprint('fountains', __name__, url_prefix='/api/fountains')

@fountains.route("")
def all_fountains():
    fountain_list = []
    with open("data/wvz.wvz_brunnen23.csv") as csvfile:
        lines = csv.reader(csvfile)
        header = None
        for i, row in enumerate(lines):
            if i == 0:
                header = row
            else:
                fountain_list.append({
                    key: value for key, value in zip(header, row)
                })
    return jsonify(fountain_list)