import os
from flask import Flask  # new
from flask_sqlalchemy import SQLAlchemy


# instantiate the db
db = SQLAlchemy()


# new
def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__)
    # set config
    app_settings = os.getenv("APP_SETTINGS")
    print(os.environ.get("APP_SETTINGS"))
    app.config.from_object(app_settings)
    # app.config[ "SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@api-db:5432/api_dev"
    # set up extensions
    db.init_app(app)
    # register blueprints
    from src.api.users import users_blueprint
    from src.api.ping import ping_blueprint
    app.register_blueprint(ping_blueprint)
    app.register_blueprint(users_blueprint)
    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}


    return app





