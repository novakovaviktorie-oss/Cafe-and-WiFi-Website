# makes src a package
from flask import Flask
from flask_bootstrap import Bootstrap5

bootstrap = Bootstrap5()

def create_app():
    app = Flask(__name__)
    # Load config from src/config.py or .env
    app.config['SECRET_KEY'] = "your-default-secret-key"

    bootstrap.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    return app