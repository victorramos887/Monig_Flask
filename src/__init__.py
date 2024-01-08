import os  # type: ignore
import json
from datetime import timedelta

# SWAGGER DOCUMENTATION
from flasgger import Swagger, swag_from, APISpec
from .config.swagger import swagger_config, swagger_config_cadastro, template

# MODELS
from .models import db, guard, Usuarios

from . import routes
from .routes.email import index

#Envio automático email
from apscheduler.schedulers.background import BackgroundScheduler
from flask_mail import Mail

from flask import Blueprint, Flask
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_cors import CORS
from flask_migrate import Migrate

from sqlalchemy import text
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import text

# from flask_continuum import Continuum


# Crie uma instância do objeto de cache
cache = Cache(config={'CACHE_TYPE': "SimpleCache"})
rotas = [getattr(routes, nome) for nome in dir(routes)
         if isinstance(getattr(routes, nome), Blueprint)]

mail = Mail()
scheduler = BackgroundScheduler()
scheduler.start()

def create_app(test_config=None):

    app = Flask(__name__,
                instance_relative_config=True)

    cache.init_app(app)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI='postgresql://{user}:{pw}@{url}/{db}'.format(user=os.getenv("POSTGRES_USER"),
                                                                                 pw=os.getenv(
                                                                                     "POSTGRES_PASSWORD"),
                                                                                 url=os.getenv(
                                                                                     "POSTGRES_ENDPOINT"),
                                                                                 db=os.getenv("POSTGRES_DATABASE")),
            SQLALCHEMY_TRACK_MODIFICATIONS=True,
            SQLALCHEMY_TIMEZONE='America/Sao_Paulo',
            JSON_AS_ASCII=False,  # permitir caracteres acentuados
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY'),
            JWT_EXPIRATION_DELTA=timedelta(seconds=10),
            DEBUG=False,
            SESSION_TYPE='redis',
            FLASK_DEBUG=os.environ.get('FLASK_DEBUG'),
            RBAC_USE_WHITE=False,
            JWT_ACCESS_LIFESPAN={'minutes': 10},
            SWAGGER={
                'titulo': 'API MONIG',
                'version': 1
            },
            MAIL_SERVER=os.getenv('MAIL_SERVER'),
            MAIL_PORT = os.getenv('MAIL_PORT'),
            MAIL_USERNAME = os.getenv('MAIL_USERNAME'),
            MAIL_PASSWORD = os.getenv('MAIL_PASSWORD'),
            MAIL_USE_TLS = True,
            MAIL_USE_SSL = False
            
        )
    
    else:
        app.config.from_mapping(
            test_config,
            SQLALCHEMY_DATABASE_URI=os.environ.get('DB_TEST'),
            DEBUG=False,
            SECRET_KEY='testabancodedados'
        )
    print("CONTEXT: ", app.config['SQLALCHEMY_DATABASE_URI'])
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    mail = Mail(app)
    
    with app.app_context():
        guard.init_app(app, Usuarios)
        migrate.init_app(app)
       
       
    JWTManager(app)
    mail.init_app(app)
    
    # Blue prints
    for rota in rotas:
        app.register_blueprint(rota)

    #Envio de email
    #scheduler.add_job(index(), 'cron', hour=11, minute=53)
    
    swagger_main = Swagger(app, config=swagger_config, template=template)

    @app.route('/')
    #@swag_from('./docs/apimonig.yaml')
    def index():
        return 'API MONIG'

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    context = ('local.crt', 'local.key')
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=context)

CORS(app, resources={r"/api/*": {"origins": "*"}})
 






