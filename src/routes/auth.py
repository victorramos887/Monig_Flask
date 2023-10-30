from flask import Blueprint, jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token, get_jwt_identity, jwt_required)
from werkzeug.security import check_password_hash, generate_password_hash
from ..constants.http_status_codes import (HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT)
from ..models import Usuarios, db
from sqlalchemy import exc

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
    
    
    
    if Escola.query.filter_by(id=escola).first() is None:
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


#login
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
        
        return jsonify({
                'error':'Error',"status":False, "erro":"Mensagem", "codigo":str(e)
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