from flask import Blueprint, jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token, get_jwt_identity, jwt_required, decode_token, create_access_token)
from werkzeug.security import check_password_hash, generate_password_hash
from ..constants.http_status_codes import (HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT)
from ..models import Usuarios, Escolas, db
from sqlalchemy import exc
import time
import datetime

auth = Blueprint("auth", __name__, url_prefix = '/api/v1/auth')



#cadastro de usuário
@auth.post('/register')
def register():

    #PEGANDO VALORES POST JSON
    nome = request.json['nome']
    email = request.json['email']
    senha = request.json['senha']
    escola = request.json['escola']
    cod_cliente = request.json['cod_cliente']

    #COLOCANDO LIMITE NA SENHA
    if len(senha) < 6:
        return jsonify({'error':'Senha muito curta'}), HTTP_400_BAD_REQUEST

    #VERIFICANDO SE O USUÁRIO JÁ EXISTE
    if Usuarios.query.filter_by(email=email).first() is not None:
        return jsonify({'errors':'Usuario ja existe'}), HTTP_409_CONFLICT
    #GERANDO HASH DA SENHA
    
    
    
    if Escolas.query.filter_by(id=escola).first() is None and escola is not None:
        return jsonify({"errors":"Escola Não existe"})
        
    
    
    pws_hash = generate_password_hash(senha)

    #CRIANDO O USUÁRIO
    user = Usuarios(
        email=email,
        escola=escola,
        senha=generate_password_hash(senha),
        nome=nome,
        cod_cliente=cod_cliente
    )  

    db.session.add(user)
    db.session.commit()

    return jsonify({ 'mensagem':'Usuario criado com sucesso!', 'user':user.nome }), 200


#CRIAR UM NOVA ROLE
@auth.post('/roles')
def roles():
    
    try:
        name = request.json.get('name', '')
        role = Roles.query.filter_by(name=name).first()
        if role:
            return jsonify({'mensagem':"Role já existe!!!"}), 409
        
        role_add = Roles(
            name=name
        )
        
        db.session.add(role_add)
        db.session.commit()
        
        return jsonify({"mensagem":"Role criada!!!", "role":role_add.name})
    
    except Exception as e:
        return jsonify({"mensagem":"Erro não tratado", "Erro":str(e), "status":False}), 500


@auth.post('/roleuser')
def roleuser():
    
    try:
        user = request.json.get("usuario", "")
        role = request.json.get("role", "")
        
        usuario = Usuarios.query.filter_by(username = user).first()
        
        if not usuario:
            
            return jsonify({"mensagem":"usuário não encontrado", "status":False}), 400
        
        
        role_add = Roles.query.filter_by(name = role_add).first()
        
        if not role_add:
            return jsonify({"mensagem":"Role não encontrada", "status":False}), 400
        
        
        role_user_verifique = RolesUser.query.filter_by(usuarios_id=usuario.id,
            roles_id=role_add.id).first()
        
        if role_user_verifique:
            return jsonify({"mensagem":"Usuário já pertence a esta role", "status":False}), 400
        
        role_user = RolesUser(
            usuarios_id=usuario.id,
            roles_id=role_add.id
        )
        
        db.session.add(role_user)
        db.session.commit()
        
        return jsonify({
            "mensagem":"adicionado nova role"
        })

    except Exception as e:
        return jsonify({"mensagem":"Erro não tratado", "Erro":str(e), "status":False}), 500
        
@auth.post('/login')
def login():

    try:
        email = request.json.get('email', '')
        senha = request.json.get('senha', '')
        
        # print(senha, email)
        user = Usuarios.query.filter_by(email = email).first()
        print(user)

    except exc.DBAPIError as e:

        if e.orig.pgcode == '42703':
            return {'error':'Verifique os nomes das colunas no banco de dados', "status":False, "codigo":str(e)}
        else:
            return {'error':'ERRO NÃO TRATADO', "status":False, "codigo":str(e)}

    try:
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
                        'email':email,
                        'escola':user.escola
                    }, 
                    "status":True
                }), HTTP_200_OK
            else:
                return jsonify({'error':'senha incorreta'}), HTTP_409_CONFLICT
    except Exception as e:
        return jsonify({"error":str(e), "mensagem":"Erro não tratado", "status":False}), HTTP_400_BAD_REQUEST


#busca as informações do usuário identificado pelo token
@auth.get('/me')
@jwt_required()
def me():
    user_id = get_jwt_identity()
    print(user_id)

    user = Usuarios.query.filter_by(id=user_id).first()
    return jsonify({
        'email':user.email,
    }), HTTP_200_OK


# Rota para forçar a expiração de um token
@auth.route('/expire_token/', methods=['GET'])
@jwt_required()
def expire_token():
    try:
      
        # Forçar a expiração do token definindo 'exp' para um valor passado (por exemplo, 1 segundo atrás)
        current_user_id = get_jwt_identity()

        # Recriar o token com o payload modificado
        expires_timestamp = datetime.datetime.utcnow() - datetime.timedelta(seconds=1)
        payload = {'identity': current_user_id, 'exp': expires_timestamp}

        # Recriar o token com o payload modificado
        #expired_token = create_access_token(identity=current_user_id, expires_delta=False, expires=expires_timestamp)
        # expired_token = create_access_token(identity=current_user_id, expires_delta=False)
        expired_token = create_access_token(identity=current_user_id, payload=payload)

        return jsonify(expired_token=expired_token)
    except Exception as e:
        return jsonify(error=str(e))

#renovar o JWT de acesso do usuário
@auth.post('/token/refresh')
@jwt_required(refresh=True)
def refresh_user_token():
    identify = get_jwt_identity()
    access = create_access_token(identity=identify)
    reflesh = create_refresh_token(identity= identify)
    return jsonify({'access':access, 'reflesh':reflesh}), HTTP_200_OK