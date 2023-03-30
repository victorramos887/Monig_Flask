import os  # type: ignore
from os import path
#VARIAVEIS DE AMBIENTE
from dotenv import load_dotenv
#SWAGGER DOCUMENTATION
from flasgger import Swagger
from .config.swagger import swagger_config, template
from flask import Flask, render_template
from .models import db
from .routes import *
from flask_caching import Cache
from flask_caching.backends import SimpleCache

# Crie uma instância do objeto de cache
cache = Cache(config={'CACHE_TYPE': "SimpleCache"})


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, "../.env"))


def create_app(test_config=None):

    app = Flask(__name__,
                instance_relative_config=True)

    cache.init_app(app)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI'),
            SQLALCHEMY_TRACK_MODIFICATIONS = True,
            JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY'),
            SWAGGER ={
                'titulo':'API MOIG',
                'version': 1
            }
        )

    else:
        app.config.from_mapping(
            test_config,
            SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI')
        )

    db.app = app  # type: ignore
    db.init_app(app)


    #Google Cloud
    with app.app_context():
        db.create_all()

    #Blue prints
    app.register_blueprint(cadastros)
    app.register_blueprint(send_frontend)
    app.register_blueprint(funcionalidades)

    Swagger(app, config=swagger_config, template=template)

    @app.route('/')
    def index():
        return render_template('homepage.html')

    @app.route('/testando')
    def index():
        return 'Olá GCP'

    return app


app = create_app()
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 8080))