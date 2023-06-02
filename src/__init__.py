import os  # type: ignore

# SWAGGER DOCUMENTATION
from .config.swagger import swagger_config, template
from .models import db
from . import routes
from datetime import timedelta
from flasgger import Swagger
from flask import Blueprint, Flask, render_template
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_cors import CORS

# Crie uma instância do objeto de cache
cache = Cache(config={'CACHE_TYPE': "SimpleCache"})
rotas = [getattr(routes, nome) for nome in dir(routes)
         if isinstance(getattr(routes, nome), Blueprint)]


def create_app(test_config=None):

    app = Flask(__name__,
                instance_relative_config=True)

    cache.init_app(app)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI'),
            SQLALCHEMY_TRACK_MODIFICATIONS=True,
            JSON_AS_ASCII=False,  # permitir caracteres acentuados
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY'),
            SWAGGER={
                'titulo': 'API MONIG',
                'version': 1
            },
            JWT_EXPIRATION_DELTA=timedelta(
                days=int(os.environ.get('JWT_EXPIRATION_DAYS', '30'))),
            DEBUG=False
        )

    else:
        app.config.from_mapping(
            test_config,
            SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI'),
            DEBUG=False
        )

    db.app = app  # type: ignore
    db.init_app(app)

    with app.app_context():
        db.create_all()

    JWTManager(app)

    # Blue prints
    for rota in rotas:
        app.register_blueprint(rota)

    Swagger(app, config=swagger_config, template=template)

    @app.route('/')
    def index():
        return render_template('homepage.html')

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

CORS(app, resources={r"/api/*": {"origins": "*"}})
