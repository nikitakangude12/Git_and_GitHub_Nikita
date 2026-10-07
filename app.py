import certifi
from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
import json

app = Flask(__name__)

# MongoDB Atlas connection
MONGO_URI = "mongodb+srv://nikitakangude12_db_user:Nikuu9756@cluster0.xg0ch5m.mongodb.net/?appName=Cluster0&compressors=zlib"

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=30000
)

db = client["flask_database"]
collection = db["users"]


# Task 1: JSON API Route
@app.route("/api")
def api():

    with open("data.json", "r") as file:
        data = json.load(file)

    return jsonify(data)


# Task 2: Frontend Form
@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        try:
            name = request.form["name"]
            email = request.form["email"]
            course = request.form["course"]

            data = {
                "name": name,
                "email": email,
                "course": course
            }

            collection.insert_one(data)

            return redirect(url_for("success"))

        except Exception as e:

            return render_template(
                "index.html",
                error=str(e)
            )

    return render_template("index.html")

# Task 3: To-Do Backend
@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():

    item_name = request.form["itemName"]
    item_description = request.form["itemDescription"]

    todo_item = {
        "itemName": item_name,
        "itemDescription": item_description
    }

    collection.insert_one(todo_item)

    return redirect(url_for("success"))


# Success page
@app.route("/success")
def success():

    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
    