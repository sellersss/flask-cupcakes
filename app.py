"""Flask app for Cupcakes"""
from flask import Flask, json, redirect, render_template, jsonify, request, abort, url_for
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'S3CR3T_K3Y'

connect_db(app)
db.create_all()


@app.route('/')
def index():
    """Returns homepage.

    Displays all cupcakes using ajax and jquery. Uses a form to submit a post
    request appending a new cupcake object to the list.
    """

    return render_template('index.html')


@app.route('/api/cupcakes', methods=['GET'])
def get_from_all():
    """Handler for returning all cupcakes in a json.

    Sends a query to cupcakes database and serializes all cupcakes. Returns
    cupcakes in a JSON format.
    """

    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]

    return jsonify(cupcakes=cupcakes)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['GET'])
def get_from_id(cupcake_id):
    """Handler for returning a specific cupcake.

    Sends a query for a specified cupcake by its ID. If no cupcake is found,
    return a 404 error.
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    if cupcake:
        json_format = cupcake.serialize()

        return jsonify(cupcake=json_format)
    else:
        abort(404)


@app.route('/api/cupcakes', methods=['POST'])
def post_to_all():
    """Handler for adding a cupcake.

    Sends a post request in order to append a cupcake to the database and
    returns a successful status response code.
    """

    json_cupcake = request.json

    cupcake = Cupcake(flavor=json_cupcake['flavor'],
                      rating=json_cupcake['rating'],
                      size=json_cupcake['size'],
                      image=json_cupcake['image'] or None)

    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake.serialize()), 201)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def patch_from_id(cupcake_id):
    """Handler for updating/patching a cupcake.

    Sends a patch request for a cupcake by its ID and adds it to the database.
    If no cupcake is found, return a 404 error.
    """

    json_cupcake = request.json

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    if cupcake:
        cupcake.flavor = json_cupcake['flavor']
        cupcake.rating = json_cupcake['rating']
        cupcake.size = json_cupcake['size']
        cupcake.image = json_cupcake['image']

        db.session.add(cupcake)
        db.session.commit()

        return jsonify(cupcake=cupcake.serialize())
    else:
        abort(404)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_from_id(cupcake_id):
    """Handler for deleting a cupcake.

    Sends a delete request per a specified cupcake ID. Returns succesful
    deletion response code and a 'deleted' message.
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    if cupcake:
        db.session.delete(cupcake)
        db.session.commit()

        return (jsonify(message='deleted'), 202)
    else:
        abort(404)


@app.errorhandler(404)
def page_not_found(e):
    """"""

    return render_template('404.html'), 404
