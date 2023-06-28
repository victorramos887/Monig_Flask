from flask import Blueprint, jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token, get_jwt_identity, jwt_required)
from werkzeug.security import check_password_hash, generate_password_hash
from ..constants.http_status_codes import (HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT)
from ..models import Usuarios, db #session
from sqlalchemy import exc

auth = Blueprint("auth", __name__, url_prefix = '/api/v1/auth')



#login
@auth.post('/login')
def login():
    email = request.json.get('email', '')
    senha = request.json.get('senha', '')

    try:
        user = Usuarios.query.filter_by(email = email).first()

    except exc.DBAPIError as e:

        if e.orig.pgcode == '42703':
            return {'error':'Verifique os nomes das colunas no banco de dados', "status":False}
        else:
            return {'error':'ERRO NÃO TRATADO', "status":False}

    if user is None:
        return jsonify({'ERRO':'Usuário não cadastrado!'}), HTTP_400_BAD_REQUEST

    if user:
        if check := check_password_hash(user.senha, senha):
            reflesh = create_refresh_token(identity= user.id)
            access = create_access_token(identity= user.id)
            return jsonify({
                'user': {
                    'reflesh':reflesh,
                    'access':access,
                    'email':email
                }, 
                "status":True
            }), HTTP_200_OK
    else:
        return jsonify({'error':'senha incorreta'}), HTTP_409_CONFLICT
    return jsonify({
                'error':'Error',"status":False
            }), HTTP_400_BAD_REQUEST


#busca as informações do usuário identificado pelo token
@auth.get('/me')
@jwt_required()
def me():
    user_id = get_jwt_identity()

    user = Usuarios.query.filter_by(id=user_id).first()
    return jsonify({
        'email':user.email,
    }), HTTP_200_OK


#renovar o JWT de acesso do usuário
@auth.post('/token/refresh')
@jwt_required(refresh=True)
def refresh_user_token():
    identify = get_jwt_identity()
    access = create_access_token(identity=identify)

    return jsonify({'access':access}), HTTP_200_OK