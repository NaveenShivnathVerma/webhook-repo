from flask import Blueprint, request, jsonify
from app.extensions import mongo
from datetime import datetime

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    event_type = request.headers.get('X-GitHub-Event')
    payload = request.json

    author = payload.get("pusher", {}).get("name") or payload.get("sender", {}).get("login")
    timestamp = datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")

    data = {}

    if event_type == "push":
        to_branch = payload.get("ref", "").split("/")[-1]
        data = {
            "event": "push",
            "message": f"{author} pushed to {to_branch} on {timestamp}"
        }

    elif event_type == "pull_request":
        action = payload.get("action")
        if action == "opened":
            from_branch = payload.get("pull_request", {}).get("head", {}).get("ref")
            to_branch = payload.get("pull_request", {}).get("base", {}).get("ref")
            data = {
                "event": "pull_request",
                "message": f"{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}"
            }
        elif action == "closed" and payload.get("pull_request", {}).get("merged"):
            from_branch = payload["pull_request"]["head"]["ref"]
            to_branch = payload["pull_request"]["base"]["ref"]
            data = {
                "event": "merge",
                "message": f"{author} merged branch {from_branch} to {to_branch} on {timestamp}"
            }

    if data:
        mongo.db.github_events.insert_one(data)

    return jsonify({"status": "ok"}), 200


@webhook.route('/events', methods=["GET"])
def get_events():
    events = list(mongo.db.github_events.find().sort("_id", -1).limit(10))
    formatted = [{"message": e["message"]} for e in events]
    return jsonify(formatted), 200
