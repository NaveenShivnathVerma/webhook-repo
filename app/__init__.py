from flask import Flask, render_template
from app.extensions import mongo
from app.webhook.routes import webhook

def create_app():
    app = Flask(__name__)

    # ✅ Step 1: MongoDB URI Set
    app.config["MONGO_URI"] = "mongodb://localhost:27017/webhookDB"

    # ✅ Step 2: Mongo Init
    mongo.init_app(app)

    # ✅ Step 3: Register Blueprint
    app.register_blueprint(webhook)

    # ✅ Step 4: Add Home Route (for index.html frontend)
    @app.route("/")
    def home():
        return render_template("index.html")

    return app
