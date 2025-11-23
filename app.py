from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__, template_folder="templates")

db = mysql.connector.connect(
    host="shortline.proxy.rlwy.net",
    user="root",
    password="JHxYExZtJJlfLnSEjJCDdlWkJOkCuCYT",
    database="railway",
    port=27244
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register_serial():
    serial = request.form.get("serial")

    if not serial:
        return jsonify({"status": "error", "message": "serial required"})

    cur = db.cursor()
    cur.execute("SELECT id FROM serials WHERE serial=%s", (serial,))
    exists = cur.fetchone()

    if exists:
        return jsonify({"status": "exists", "message": "already exists"})

    cur.execute("INSERT INTO serials (serial) VALUES (%s)", (serial,))
    db.commit()

    return jsonify({"status": "success", "message": "registered"})
