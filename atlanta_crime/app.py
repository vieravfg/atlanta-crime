# import necessary libraries
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite"

# Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from .models import (
    Pet,
    Client)
# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

# create route that renders petsindex.html template
@app.route("/petsindex")
def petshome():
    return render_template("petsindex.html")


# Query the database and send the jsonified results
@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        name = request.form["petName"]
        lat = request.form["petLat"]
        lon = request.form["petLon"]

        pet = Pet(name=name, lat=lat, lon=lon)
        db.session.add(pet)
        db.session.commit()
        return redirect("/petsindex", code=302)

    return render_template("form.html")

# Query the database and send the jsonified results
@app.route("/sketch", methods=["GET", "POST"])
def clientsend():
    if request.method == "POST":
        clientname = request.form["clientname"]
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]


        client = Client(clientname=clientname, email = email, subject=subject, message=message)
        db.session.add(client)
        db.session.commit()
        return redirect("/", code=302)

    return render_template("sketch.html")


@app.route("/api/pals")
def pals():
    results = db.session.query(Pet.name, Pet.lat, Pet.lon).all()

    hover_text = [result[0] for result in results]
    lat = [result[1] for result in results]
    lon = [result[2] for result in results]

    pet_data = [{
        "type": "scattergeo",
        "locationmode": "USA-states",
        "lat": lat,
        "lon": lon,
        "text": hover_text,
        "hoverinfo": "text",
        "marker": {
            "size": 15,
            "line": {
                "color": "rgb(8,8,8)",
                "width": 1
            },
        }
    }]

    return jsonify(pet_data)

@app.route("/api/customers")
def customers():
    results = db.session.query(Client.clientname, Client.email, Client.subject, Client.message).all()

    name = [result[0] for result in results]
    email = [result[1] for result in results]
    subject = [result[2] for result in results]
    message = [result[3] for result in results]


    client_data = [{
        "name": name,
        "email": email,
        "subject": subject,
        "message": message,    
    }]

    return jsonify(client_data)


if __name__ == "__main__":
    app.run()
