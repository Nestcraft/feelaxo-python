from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../instance/config.py')


    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:Nestcbd%4046@209.182.233.164/feelaxo'

    db.init_app(app)

    api = Api(app)

    from . import routes    
    routes.register_routes(api)
    routes.ai_routes(api)


    return app
