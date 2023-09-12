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
            SQLALCHEMY_DATABASE_URI='postgresql://{user}:{pw}@{url}/{db}'.format(user=get_env_variable("POSTGRES_USER"),
                                                                                    pw=os.getenv("POSTGRES_PASSWORD"),
                                                                                    url=os.getenv("POSTGRES_ENDPOINT")), #os.environ.get('SQLALCHEMY_DATABASE_URI'),
            SQLALCHEMY_TRACK_MODIFICATIONS=True,
            JSON_AS_ASCII=False,  # permitir caracteres acentuados
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY'),
            JWT_EXPIRATION_DELTA=timedelta(days=int(os.environ.get('JWT_EXPIRATION_DAYS', '30'))),
            DEBUG=False,
            SESSION_TYPE='redis'
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
    
    
    #REEINICIANDO O BANCO
    @app.cli.command('resetdb')
    def resetdb_command():
        """Destroys and creates the database + tables."""

        SQLALCHEMY_DATABASE_URI = app.config["SQLALCHEMY_DATABASE_URI"]
        print("DB_URL : " + str(SQLALCHEMY_DATABASE_URI))

        from sqlalchemy_utils import database_exists, create_database, drop_database
        if database_exists(SQLALCHEMY_DATABASE_URI):
            print('Deleting database.')
            create_schema_sql = text('CREATE SCHEMA IF NOT EXISTS meu_esquema;')
            db.session.execute(create_schema_sql)
            db.session.commit()
            # drop_database(SQLALCHEMY_DATABASE_URI)
        if not database_exists(SQLALCHEMY_DATABASE_URI):
            print('Creating database.')
            create_database(SQLALCHEMY_DATABASE_URI)

            
        db.drop_all()
        print('Creating tables.')
        db.create_all()
        print('Shiny!!!')
    

    with app.app_context():
        db.create_all()
        add_opniveis()
        continuum.init_app(app)


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
    app.run(host='0.0.0.0', port=5000, debug=True)

CORS(app, resources={r"/api/*": {"origins": "*"}})