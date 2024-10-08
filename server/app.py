#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries_list = Bakery.query.all()
    response = make_response(jsonify([bakery.to_dict() for bakery in bakeries_list]), 200)
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery_one = Bakery.query.filter(Bakery.id == id).first()
    if bakery_one:
        response = make_response(jsonify(bakery_one.to_dict()), 200)
    else:
        response = make_response(jsonify({"error": "Bakery not found"}), 404)
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    response = make_response(jsonify([baked_good.to_dict() for baked_good in baked_by_price]), 200)
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if most_expensive:
        response = make_response(jsonify(most_expensive.to_dict()), 200)
    else:
        response = make_response(jsonify({"error": "No baked goods found"}), 404)
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
