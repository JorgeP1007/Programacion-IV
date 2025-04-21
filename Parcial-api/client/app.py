from flask import Flask, render_template, request
import requests

app = Flask(__name__)
API_URL = "http://api:5000/api/vaccination"

@app.route("/", methods=["GET"])
def index():
    region = request.args.get("region")
    year = request.args.get("year")
    try:
        if region:
            response = requests.get(f"{API_URL}/region/{region}")
        elif year:
            response = requests.get(f"{API_URL}/year/{year}")
        else:
            response = requests.get(API_URL)

        data = response.json()
    except Exception as e:
        data = []
        print("Error:", e)

    return render_template("index.html", data=data)
