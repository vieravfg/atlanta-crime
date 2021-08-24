# import necessary libraries
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
from flask_cors import CORS
from pymongo import MongoClient
import  datetime

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
# Remove tracking modifications
app.config['MONGO_CONNECT'] = False
CORS(app)
client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
db = client.pytodo

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")


# create route that renders form.html template
@app.route("/send", methods=["GET"])
def send():
    return render_template("form.html")

##################### Machine Learning ############################
@app.route("/ml.html", methods=["GET"])
def ml():
    return render_template("ml.html")
@app.route("/arima.html", methods=["GET"])
def arima():
    return render_template("arima.html")
@app.route("/prophet.html", methods=["GET"])
def prophet():
    return render_template("prophet.html")
@app.route('/prediction')
def predication_ml():    
# Find one record of data from database
    if request.method == "GET":
        forecast_value = []
        for value in list(db.forecast_value.find()):
            forecast_value.append({
                "Date": value["DATE"],
                "arima_value": value["arima_value"],
                "prophet_value": value["prophet_value"] 
            })
# Return template and data
        return jsonify(forecast_value)
#############################################################################

# Query the database and send the jsonified results

@app.route("/api/customers", methods = ["GET","POST"])
def customers():
    if request.method == "GET":
        todos = []
        for todo in list(db.todos.find()):
            todos.append({
                "id": todo["id"],
                "name": todo["name"],
                "email": todo["email"],
                "subject": todo["subject"],
                "message": todo["message"],  
            })
        return jsonify(data={"status":200,"msg":"Found Subscribers", "Customers": todos})
    
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]
        
        #insert to dabase
        db.todos.insert_one({
            "id": str(datetime.datetime.now().timestamp()),
            "name": name,
            "email": email,
            "subject": subject,
            "message": message
        })
        return jsonify(data={"status":201,"msg":"You added a customer"})


if __name__ == "__main__":
    app.run(debug = True)


   