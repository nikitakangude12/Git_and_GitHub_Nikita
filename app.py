
import os
import json
import certifi

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# MongoDB Atlas connection
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError(
        "MONGO_URI is missing. Please add it to your .env file."
    )

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
    with open("data.json", "r", encoding="utf-8") as file:
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
            app.logger.exception("Error submitting frontend form")
            return render_template(
                "index.html",
                error="Unable to save your details. Please try again."
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
