import os  # type: ignore
import json
# SWAGGER DOCUMENTATION
from .config.swagger import swagger_config, template
from .models import db, add_opniveis
from . import routes
from datetime import timedelta
from flasgger import Swagger
from flask import Blueprint, Flask
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_cors import CORS
import tempfile
from .keycloak_flask import oidc

# Crie uma instância do objeto de cache
cache = Cache(config={'CACHE_TYPE': "SimpleCache"})
rotas = [getattr(routes, nome) for nome in dir(routes)
         if isinstance(getattr(routes, nome), Blueprint)]

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_arquivo = os.path.join(diretorio_atual, 'config', 'client_secrets.json')



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
            JWT_EXPIRATION_DELTA=timedelta(days=int(os.environ.get('JWT_EXPIRATION_DAYS', '30'))),
            DEBUG=False,
            OIDC_CLIENT_SECRETS=caminho_arquivo,
            OIDC_ID_TOKEN_COOKIE_SECURE=False,
            OIDC_REQUIRE_VERIFIED_EMAIL=False,
            OIDC_USER_INFOR_ENABLED=True,
            OIDC_OPENID_REALM='springBootkeycloak',
            OIDC_SCOPES=['openid', 'email', 'profile'],
            OIDC_INTROSPECTION_AUTH_METHOD='client_secret_post',
            OIDC_TOKEN_TYPE_HINT='access_token'
        )

        with open(caminho_arquivo, 'r') as f:
            client_secrets_content = f.read()
            client_secrets = json.loads(client_secrets_content)

        with tempfile.NamedTemporaryFile(mode='w', delete=False, dir=tempfile.gettempdir()) as temp_file:
            temp_file.write(json.dumps(client_secrets))
            temp_file.flush()
            temp_file_path = temp_file.name
            app.config['OIDC_CLIENT_SECRETS'] = temp_file.name

    else:
        app.config.from_mapping(
            test_config,
            SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI'),
            DEBUG=False
        )
    #os.path.join(config_dir, 'config', 'client_secrets.json')
    db.app = app  # type: ignore
    db.init_app(app)
    
    with app.app_context():
        oidc.init_app(app)
        db.create_all()
        add_opniveis()

    JWTManager(app)

    # Blue prints
    for rota in rotas:
        app.register_blueprint(rota)

    Swagger(app, config=swagger_config, template=template)

    @app.route('/')
    def index():
        return 'API MONIG'

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

CORS(app, resources={r"/api/*": {"origins": "*"}})