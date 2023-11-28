from flask import Blueprint, jsonify, request
from flasgger import swag_from
from flask_jwt_extended import (create_access_token, create_refresh_token, get_jwt_identity,
                                jwt_required, decode_token, create_access_token, get_current_user)
from werkzeug.security import check_password_hash, generate_password_hash
from ..constants.http_status_codes import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT)
from ..models import Usuarios, Escolas, Roles, RolesUser, Usuarios, db, guard
from sqlalchemy import exc
import time
import datetime
import flask_praetorian
import time

auth = Blueprint("auth", __name__, url_prefix='/api/v1/auth')

@auth.post('/register')
@swag_from('../docs/auth/register.yaml')
def register():

    # PEGANDO VALORES POST JSON
    nome = request.json['nome']
    email = request.json['email']
    senha = request.json['senha']
    escola = request.json['escola']
    cod_cliente = request.json['cod_cliente']
    role = request.json['roles']

    if not Roles.query.filter_by(name=role).first():
        return jsonify({'error':f'Role {role} não encontrada'}), 409

    # COLOCANDO LIMITE NA SENHA
    if len(senha) < 6:
        return jsonify({'error': 'Senha muito curta'}), HTTP_400_BAD_REQUEST

    # VERIFICANDO SE O USUÁRIO JÁ EXISTE
    if Usuarios.query.filter_by(username=email).first() is not None:
        return jsonify({'errors': 'Usuario ja existe'}), HTTP_409_CONFLICT
    # GERANDO HASH DA SENHA

    if Escolas.query.filter_by(id=escola).first() is None and escola is not None:
        return jsonify({"errors": "Escola Não existe"})

    pws_hash = generate_password_hash(senha)

    # CRIANDO O USUÁRIO
    user = Usuarios(
        username=email,
        escola=escola,
        hashed_password=guard.hash_password(senha),
        nome=nome,
        cod_cliente=cod_cliente
    )

    # ADICIONANDO AS ROLES

    role_obj = Roles.query.filter_by(name=request.json['roles']).first()
    user.roles.append(role_obj)

    db.session.add(user)
    db.session.commit()

    return jsonify({'mensagem': 'Usuario criado com sucesso!', 'user': user.nome}), 200


#CRIAR UM NOVA ROLE
@auth.post('/roles')
def roles():
    
    try:
        name = request.json.get('name', '')
        role = Roles.query.filter_by(name=name).first()
        print(role)
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
@swag_from('../docs/auth/login.yaml')
def login():
    try:
        email = request.json.get('email', '')
        senha = request.json.get('senha', '')

        user = Usuarios.query.filter_by(username=email).first()
    except exc.DBAPIError as e:
        # Handle database errors
        return jsonify({'error': str(e), "mensagem":"Erro não tratado!"}), HTTP_400_BAD_REQUEST

    if user is None:
        return jsonify({'error': 'Usuário não cadastrado!'}), HTTP_400_BAD_REQUEST
    try:

        user = guard.authenticate(username=email, password=senha)
        
        access = guard.encode_jwt_token(user)
        return jsonify({
            'user': {
                'access': access,
                'email': user.username,
                'escola': user.escola
            },
            'status': True
        }), HTTP_200_OK
    except Exception as e:
        return str(e)


# busca as informações do usuário identificado pelo token
@auth.get("/me")
@flask_praetorian.auth_required
def protected():
    
    print(flask_praetorian.current_user().username)
    return jsonify(
        {"message":f"usuário {flask_praetorian.current_user().username}"}
    )


# Rota para forçar a expiração de um token
@auth.route('/expire_token/', methods=['GET'])
@jwt_required()
def expire_token():
    try:

        current_user_id = get_jwt_identity()

        expires_timestamp = datetime.datetime.utcnow() - datetime.timedelta(seconds=1)
        payload = {'identity': current_user_id, 'exp': expires_timestamp}

        
        expired_token = create_access_token(
            identity=current_user_id, payload=payload)

        return jsonify(expired_token=expired_token)
    except Exception as e:
        return jsonify(error=str(e))


@auth.route('/refresh', methods=['POST'])
def refresh_token():
    # Get the old token from the request body
    token = request.get_json()['token']
    print(token)
    # Verify the old token
    try:
        new_token = guard.refresh_jwt_token(token)
    except Exception as e:
        return jsonify({'error': str(e)}), 401

    # Issue a new token with the same claims as the old token

    return jsonify({'access_token': new_token}), 200