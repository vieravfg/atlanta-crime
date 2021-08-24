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
    Client)

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")


# Query the database and send the jsonified results
@app.route("/form", methods=["GET", "POST"])
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

    return render_template("form.html")



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
