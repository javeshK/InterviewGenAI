from flask import Flask

from config import Config

from database import models

from database.db import db

from routes.main import main

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(main)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)