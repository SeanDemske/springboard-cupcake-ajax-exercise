"""Flask app for Cupcakes"""

from flask import Flask, request, redirect, render_template, jsonify
from models import db, connect_db, Cupcake, DEFAULT_IMG_URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:developer@localhost:5432/cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "SECRET!"

connect_db(app)
db.create_all()

# from flask_debugtoolbar import DebugToolbarExtension

# debug = DebugToolbarExtension(app)

##############################
# /////////////////#############
#   VIEW ROUTES         ########
# /////////////////#############
##############################

@app.route("/")
def home_page():
    """Display Homepage"""

    return render_template("index.html")

##############################
# /////////////////#############
#   API ROUTES          ########
# /////////////////#############
##############################

@app.route("/api/cupcakes")
def return_cupcakes_json():
    """Return json data with all the cupcakes"""

    cupcakes = Cupcake.query.all()
    cupcakes_dict = [cupcake.serialize() for cupcake in cupcakes]

    return jsonify(cupcakes=cupcakes_dict)

@app.route("/api/cupcakes/<int:cupcake_id>")
def return_cupcake_json(cupcake_id):
    """Return json data about the specified cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake_dict = cupcake.serialize()

    return jsonify(cupcake=cupcake_dict)

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Create a cupcake and add to database"""

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(cupcake)
    db.session.commit()
    cupcake_dict = cupcake.serialize()

    return (jsonify(cupcake=cupcake_dict), 201)

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update specified cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    cupcake.flavor = flavor
    cupcake.size = size
    cupcake.rating = rating
    cupcake.image = image

    db.session.add(cupcake)
    db.session.commit()
    cupcake_dict = cupcake.serialize()

    return jsonify(cupcake=cupcake_dict)

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Delete specified cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(msg="Delete successful")