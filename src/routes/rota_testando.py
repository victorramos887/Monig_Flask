from flask import Blueprint, jsonify, request
from ..constants.http_status_codes import (HTTP_200_OK, HTTP_400_BAD_REQUEST)
from sqlalchemy import exc, func
from ..models import testando, db


rota_testando = Blueprint('rota_testando', __name__, url_prefix = '/api/v1/rota_testando')


@rota_testando.post('/nome')
def rota_testando_function():
    dado = request.get_json()
    teste = testando(**dado)

    try:
        db.session.add(teste)
        db.session.commit()
        return jsonify({'status':True, 'nome':teste.nome}), HTTP_200_OK
    except exc.DBAPIError as e:
        return jsonify({'status':False}), HTTP_400_BAD_REQUEST
