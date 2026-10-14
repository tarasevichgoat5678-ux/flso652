from flask import Flask
from config import Config
from extensions import db
from routes import main_bp

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)


    db.init_app(app)


    app.register_blueprint(main_bp)


    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8080)
