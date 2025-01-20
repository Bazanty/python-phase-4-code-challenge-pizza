#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_restful import Api
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Restaurant, RestaurantPizza, Pizza
import os

# Configure the application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False

# Enable CORS and initialize extensions
CORS(app)
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# Routes
@app.route("/")
def index():
    return "<h1>Code challenge</h1>"


@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    restaurants = Restaurant.query.all()
    restaurant_data = [
        {
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address
        } for restaurant in restaurants
    ]
    return jsonify(restaurant_data)


@app.route("/restaurants/<int:id>", methods=["GET"])
def get_restaurant(id):
    restaurant = Restaurant.query.filter_by(id=id).first()

    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404

    restaurant_data = {
        "id": restaurant.id,
        "name": restaurant.name,
        "address": restaurant.address,
        "restaurant_pizzas": []
    }

    for pizza in restaurant.restaurant_pizzas:
        pizza_data = {
            "id": pizza.id,
            "pizza": {
                "id": pizza.pizza.id,
                "name": pizza.pizza.name,
                "ingredients": pizza.pizza.ingredients
            },
            "pizza_id": pizza.pizza.id,
            "price": pizza.price,
            "restaurant_id": pizza.restaurant.id
        }
        restaurant_data["restaurant_pizzas"].append(pizza_data)

    return jsonify(restaurant_data)


@app.route("/restaurants/<int:id>", methods=["DELETE"])
def delete_restaurant(id):
    restaurant = Restaurant.query.filter_by(id=id).first()

    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404

    RestaurantPizza.query.filter_by(restaurant_id=id).delete()
    db.session.delete(restaurant)
    db.session.commit()

    return '', 204


@app.route("/pizzas", methods=["GET"])
def get_pizzas():
    pizzas = Pizza.query.all()
    pizza_data = [
        {
            "id": pizza.id,
            "ingredients": pizza.ingredients,
            "name": pizza.name
        } for pizza in pizzas
    ]
    return jsonify(pizza_data)


@app.route("/restaurant_pizzas", methods=["POST"])
def create_restaurant_pizza():
    data = request.get_json()

    price = data.get("price")
    pizza_id = data.get("pizza_id")
    restaurant_id = data.get("restaurant_id")

    errors = []

    # Validate required fields
    if price is None:
        errors.append("Pizza price is required.")
    elif not (0 <= price <= 100):
        errors.append("Price must be between 0 and 100.")

    if pizza_id is None:
        errors.append("Pizza ID is required.")
    if restaurant_id is None:
        errors.append("Restaurant ID is required.")

    # Validate the existence of pizza and restaurant
    pizza = db.session.get(Pizza, pizza_id) if pizza_id else None
    restaurant = db.session.get(Restaurant, restaurant_id) if restaurant_id else None

    if not pizza:
        errors.append(f"Pizza with ID {pizza_id} does not exist.")
    if not restaurant:
        errors.append(f"Restaurant with ID {restaurant_id} does not exist.")

    if errors:
        return jsonify({"errors": errors}), 400

    try:
        restaurant_pizza = RestaurantPizza(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)
        db.session.add(restaurant_pizza)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400

    response_data = {
        "id": restaurant_pizza.id,
        "pizza": {
            "id": pizza.id,
            "ingredients": pizza.ingredients,
            "name": pizza.name
        },
        "pizza_id": restaurant_pizza.pizza_id,
        "price": restaurant_pizza.price,
        "restaurant": {
            "address": restaurant.address,
            "id": restaurant.id,
            "name": restaurant.name
        },
        "restaurant_id": restaurant_pizza.restaurant_id
    }

    return jsonify(response_data), 201


if __name__ == "__main__":
    app.run(port=5555, debug=True)
