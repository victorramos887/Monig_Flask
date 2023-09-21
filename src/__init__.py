import os  # type: ignore
import json

# SWAGGER DOCUMENTATION
from .config.swagger import swagger_config, template
from .models import db, add_opniveis, continuum
from . import routes
from datetime import timedelta
from flask import Blueprint, Flask
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_cors import CORS
from sqlalchemy import text
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import text

#from flask_migrate import Migrate


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
            SQLALCHEMY_DATABASE_URI='postgresql://{user}:{pw}@{url}/{db}'.format(user=os.getenv("POSTGRES_USER"),
                                                                                    pw=os.getenv("POSTGRES_PASSWORD"),
                                                                                    url=os.getenv("POSTGRES_ENDPOINT"),
                                                                                    db=os.getenv("POSTGRES_DATABASE")),
            SQLALCHEMY_TRACK_MODIFICATIONS=True,
            JSON_AS_ASCII=False,  # permitir caracteres acentuados
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY'),
            JWT_EXPIRATION_DELTA=timedelta(days=int(os.environ.get('JWT_EXPIRATION_DAYS', '30'))),
            DEBUG=False,
            SESSION_TYPE='redis',
            FLASK_DEBUG=os.environ.get('FLASK_DEBUG')
        )

    else:
        app.config.from_mapping(
            test_config,
            SQLALCHEMY_DATABASE_URI=os.environ.get('DB_TEST'),
            DEBUG=False
        )

    #os.path.join(config_dir, 'config', 'client_secrets.json')
    db.app = app  # type: ignore
    db.init_app(app)

    # def create_database_init():
    with app.app_context():
        SQLALCHEMY_DATABASE_URI = app.config["SQLALCHEMY_DATABASE_URI"]
        if not database_exists(SQLALCHEMY_DATABASE_URI):
            create_database(SQLALCHEMY_DATABASE_URI)            
            print('Criando banco de dados!!!')
            
        continuum.init_app(app)
        if test_config is None:
            create_schema_sql = text('CREATE SCHEMA IF NOT EXISTS main;')
            db.session.execute(create_schema_sql)
            db.session.commit()
        db.create_all()
        add_opniveis()

    # create_database_init()
       
    # Continuum(app, db)
    JWTManager(app)
    
    # Blue prints
    for rota in rotas:
        app.register_blueprint(rota)

    # Swagger(app, config=swagger_config, template=template)
    @app.route('/')
    def index():
        return 'API MONIG'

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('cert.pem', 'key.pem'))

CORS(app, resources={r"/api/*": {"origins": "*"}})