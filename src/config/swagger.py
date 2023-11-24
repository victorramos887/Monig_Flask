template = {
    "swagger": "2.0",
    "info": {
        "title": "MOIG",
        "description": "API MOIG",
        "contact": {
            "responsibleOrganization": "monitora tecnologia e informação",
            "responsibleDeveloper": "Equipe Monitora",
            "email": "vsoares@monitora.info",
            "url": "http://www.monitora.info",
        },
        "termsOfService": "",
        "version": "1.0"
    },
    "basePath": "/api/v1",  # base bash for blueprint registration
    "schemes": [
        "http",
    ],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Autenticação",
            "in": "header",
            "description": "Cabeçalho de autorização JWT usando o esquema Bearer. Exemplo: \"Autenticação: Bearer {token}\""
        }
    },
}

swagger_config = {

    "headers": [
    ],

    "specs": [
        {
            "title": "Monig",
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],

    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/"
}

swagger_config_cadastro = {

    "headers": [],
    "specs": [
        {
            "title": "Cadastro",
            "endpoint": 'apispec_cadastro',
            "route": '/apispec_cadastro.json',
            "rule_filter": lambda rule: 'cadastro' in rule.endpoint,
            "model_filter": lambda tag: 'cadastro' in tag,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/cadastro_docs"
}
