from flask import Flask, jsonify, render_template
import os
import requests

app = Flask(__name__)
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:5001")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/backend-status")
def backend_status():
    try:
        response = requests.get(f"{BACKEND_URL}/api/data", timeout=5)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as exc:
        return jsonify({"error": f"Backend unavailable: {exc}"}), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
