# Pizza Restaurant API
This project provides a simple API to manage restaurants, pizzas, and their many-to-many relationship using **Flask, **SQLAlchemy, and "Flask-Migrate". Users can perform various CRUD operations on restaurants, pizzas, and their associations. The API also allows adding new pizzas to restaurants, deleting restaurants, and retrieving data on both entities and their connections.

## Table of contents
1. Installation
2. Setup
3. Endpoints
* GET /restaurants
* GET /restaurants/<id>
* DELETE /restaurants/<id>
* GET /pizzas
* POST /restaurant_pizzas
4. Testing
5. Contributing
6. License
7. Author

## Installation

The instructions assume you changed into the `code-challenge` folder **prior**
to opening the code editor.

To get started with this project, you’ll need to install both backend and frontend dependencies. Ensure you have pipenv and npm installed.

```console
pipenv install
pipenv shell
npm install --prefix client
```

## Setup

1. You can run your Flask API on [`localhost:5555`](http://localhost:5555) by
running:

```console
python server/app.py
```

2. You can run your React app on [`localhost:4000`](http://localhost:4000) by
running:

```sh
npm start --prefix client
```

You are not being assessed on React, and you don't have to update any of the
React code; the frontend code is available just so that you can test out the
behavior of your API in a realistic setting.

Your job is to build out the Flask API to add the functionality described in the
deliverables below.

You will implement an API for the following data model:

![domain diagram](https://curriculum-content.s3.amazonaws.com/6130/code-challenge-1/domain.png)


3. Database setup
The file `server/models.py` defines the model classes **without relationships**.
Use the following commands to create the initial database `app.db`:

```console
export FLASK_APP=server/app.py
flask db init
flask db migrate
flask db upgrade head
```

4. Seed the Database

Run the migrations and seed the database:

```console
flask db revision --autogenerate -m 'message'
flask db upgrade head
python server/seed.py
```

> If you aren't able to get the provided seed file working, you are welcome to
> generate your own seed data to test the application.

### Validations

Add validations to the `RestaurantPizza` model:

- must have a `price` between 1 and 30

### Routes

Set up the following routes. Make sure to return JSON data in the format
specified along with the appropriate HTTP verb.

Recall you can specify fields to include or exclude when serializing a model
instance to a dictionary using to_dict() (don't forget the comma if specifying a
single field).

NOTE: If you choose to implement a Flask-RESTful app, you need to add code to
instantiate the `Api` class in server/app.py.

#### Endpoints
Here are the Available Api endpoints

#### GET /restaurants
fetch a list of all restaurants:

```json
[
  {
    "address": "address1",
    "id": 1,
    "name": "Karen's Pizza Shack"
  },
  {
    "address": "address2",
    "id": 2,
    "name": "Sanjay's Pizza"
  },
  {
    "address": "address3",
    "id": 3,
    "name": "Kiki's Pizza"
  }
]
```

Recall you can specify fields to include or exclude when serializing a model
instance to a dictionary using `to_dict()` (don't forget the comma if specifying
a single field).

#### GET /restaurants/<int:id>

Retrieve details of a specific `restaurant` by ID, including associated pizzas:

```json
{
  "address": "address1",
  "id": 1,
  "name": "Karen's Pizza Shack",
  "restaurant_pizzas": [
    {
      "id": 1,
      "pizza": {
        "id": 1,
        "ingredients": "Dough, Tomato Sauce, Cheese",
        "name": "Emma"
      },
      "pizza_id": 1,
      "price": 1,
      "restaurant_id": 1
    }
  ]
}
```

If the `Restaurant` does not exist, return the following JSON data, along with
the appropriate HTTP status code:

```json
{
  "error": "Restaurant not found"
}
```

#### DELETE /restaurants/<int:id>

If the `Restaurant` exists, it should be removed from the database, along with
any `RestaurantPizza`s that are associated with it (a `RestaurantPizza` belongs
to a `Restaurant`). If you did not set up your models to cascade deletes, you
need to delete associated `RestaurantPizza`s before the `Restaurant` can be
deleted.

After deleting the `Restaurant`, return an _empty_ response body, along with the
appropriate HTTP status code.

If the `Restaurant` does not exist, return the following JSON data, along with
the appropriate HTTP status code:

```json
{
  "error": "Restaurant not found"
}
```

#### GET /pizzas

Return JSON data in the format below:

```json
[
  {
    "id": 1,
    "ingredients": "Dough, Tomato Sauce, Cheese",
    "name": "Emma"
  },
  {
    "id": 2,
    "ingredients": "Dough, Tomato Sauce, Cheese, Pepperoni",
    "name": "Geri"
  },
  {
    "id": 3,
    "ingredients": "Dough, Sauce, Ricotta, Red peppers, Mustard",
    "name": "Melanie"
  }
]
```

#### POST /restaurant_pizzas

Create a new relationship between a Restaurant and a Pizza:

```json
{
  "price": 5,
  "pizza_id": 1,
  "restaurant_id": 3
}
```

If the `RestaurantPizza` is created successfully, send back a response with the
data related to the `RestaurantPizza`:

```json
{
  "id": 4,
  "pizza": {
    "id": 1,
    "ingredients": "Dough, Tomato Sauce, Cheese",
    "name": "Emma"
  },
  "pizza_id": 1,
  "price": 5,
  "restaurant": {
    "address": "address3",
    "id": 3,
    "name": "Kiki's Pizza"
  },
  "restaurant_id": 3
}
```

If the `RestaurantPizza` is **not** created successfully due to a validation
error, return the following JSON data, along with the appropriate HTTP status
code:

```json
{
  "errors": ["validation errors"]
}
```
### Testing 
run the tests using pytest:
```bash 
pytest -x
```
Alternatively, you can manually test the API via Postman by importing the provided collection ```challenge-1-pizzas.postman_collection.json.```

#### Contribution
If you would like to contribute to this project, feel free to fork the repository, make your changes, and submit a pull request. Contributions are welcome!

### Licence 
This project is licensed under the MIT License.

#### Author 
This project is developed by **Nyakundi Brian**.