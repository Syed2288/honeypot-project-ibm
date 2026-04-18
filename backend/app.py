from flask import Flask, render_template, jsonify
import json
import os
import requests

app = Flask(__name__, template_folder="../templates", static_folder="../static")
LOG_FILE = "logs.json"


def load_logs():
    if not os.path.exists(LOG_FILE):
        return []
    try:
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def get_location(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}").json()
        if res["status"] == "success":
            return f"{res['city']}, {res['country']}"
        return "Unknown"
    except:
        return "Unknown"


@app.route("/")
def dashboard():
    logs = load_logs()

    for log in logs:
        log["location"] = get_location(log["ip"])

    total_attacks = len(logs)

    counts = {}
    for log in logs:
        counts[log["ip"]] = counts.get(log["ip"], 0) + 1

    top_attacker = max(counts, key=counts.get) if counts else "None"

    return render_template(
        "index.html",
        logs=logs[-10:],
        total_attacks=total_attacks,
        top_attacker=top_attacker
    )


@app.route("/logs")
def logs_page():
    logs = load_logs()
    for log in logs:
        log["location"] = get_location(log["ip"])
    return render_template("logs.html", logs=logs)


@app.route("/alerts")
def alerts():
    logs = load_logs()
    for log in logs:
        log["location"] = get_location(log["ip"])

    alerts = [log for log in logs if log["attempts"] >= 3]
    return render_template("alerts.html", alerts=alerts)


# ✅ LIVE GRAPH API
@app.route("/api/stats")
def stats():
    logs = load_logs()

    counts = {}
    for log in logs:
        ip = log["ip"]
        counts[ip] = counts.get(ip, 0) + 1

    return jsonify(counts)


# ✅ MUST BE AT END (OUTSIDE FUNCTIONS)
if __name__ == "__main__":
    print("🚀 Starting Flask Server...")
    app.run(debug=True, host="127.0.0.1", port=5000)