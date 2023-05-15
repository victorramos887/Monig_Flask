from flask import Blueprint, jsonify, request, render_template, flash, render_template_string, current_app
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_506_VARIANT_ALSO_NEGOTIATES, HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED
from sqlalchemy import exc
from flasgger import swag_from
from ..models import Escolas, Edificios, db, AreaUmida, Equipamentos, Populacao, Hidrometros
import string
import json
import re


cadastros = Blueprint('cadastros', __name__, url_prefix = '/api/v1/cadastros')

@cadastros.post('/testando')
def testando():
    formulario = request.get_json()
    return formulario


#Cadastros das escolas
@cadastros.post('/escolas')
@swag_from('../docs/cadastros/escolas.yaml')
def escolas():
    #Captura as informações que foram enviadas através do formulário HTML
    formulario = request.get_json()
    escola = Escolas(**formulario) #Atribui ao objeto escola

    try:
        #inseri no banco de dados. Tabela escolas
        db.session.add(escola)
        db.session.commit()

        return jsonify({'status':True, 'id': escola.id, "data":escola.to_json()}), HTTP_200_OK

    except exc.DBAPIError as e:
        formulario_cadastro = render_template('cadastro.html')
        if e.orig.pgcode == '23503':
            # FOREIGN KEY VIOLATION
            return jsonify({'status':False, 'erro': "Chave estrangeira", 'codigo':f'{e}'}), HTTP_409_CONFLICT

        if e.orig.pgcode == '23505':
            # UNIQUE VIOLATION
            return jsonify({'status':False, 'erro': False, 'codigo':f'{e}'}), HTTP_401_UNAUTHORIZED

        if e.orig.pgcode == '01004':
            #STRING DATA RIGHT TRUNCATION
            return jsonify({'status':False, 'erro': False, 'codigo':f'{e}'}), HTTP_506_VARIANT_ALSO_NEGOTIATES

        #flash("Erro, 4 não salva")
        return jsonify({'status':False, 'erro': 'Não foi tratado', 'codigo':f'{e}'}), HTTP_400_BAD_REQUEST


#Cadastros dos edifícios.
@cadastros.post('/edificios')
@swag_from('../docs/cadastros/edificios.yaml')
def edificios():

    formulario = request.get_json()
    edificio = Edificios(**formulario)
    try:
        #inseri no banco de dados. Tabela edificios
        db.session.add(edificio)
        db.session.commit()

        return jsonify({'status':True, 'id': edificio.id, "data":edificio.to_json()}), HTTP_200_OK

    except exc.DBAPIError as e:
        formulario_cadastro = render_template('cadastro.html')
        if e.orig.pgcode == '23503':
            # FOREIGN KEY VIOLATION
            return jsonify({'status':False, 'erro': "Chave estrangeira", 'codigo':f'{e}'}), HTTP_409_CONFLICT

        if e.orig.pgcode == '23505':
            # UNIQUE VIOLATION
            return jsonify({'status':False, 'erro': False, 'codigo':f'{e}'}), HTTP_401_UNAUTHORIZED

        if e.orig.pgcode == '01004':
            #STRING DATA RIGHT TRUNCATION
            return jsonify({'status':False, 'erro': False, 'codigo':f'{e}'}), HTTP_506_VARIANT_ALSO_NEGOTIATES

        #flash("Erro, 4 não salva")
        return jsonify({'status':False, 'erro': 'Não foi tratado', 'codigo':f'{e}'}), HTTP_400_BAD_REQUEST


@cadastros.post('/hidrometros')
@swag_from('../docs/cadastros/hidrometros.yaml')
def hidrometros():

    formulario = request.get_json()
    hidrometros = Hidrometros(**formulario)

    try:
        #inseri no banco de dados. Tabela hidrometros
        db.session.add(hidrometros)
        db.session.commit()

        return jsonify({'status':True, 'id': hidrometros.id, "data":hidrometros.to_json()}), HTTP_200_OK

    except exc.DBAPIError as e:
        formulario_cadastro = render_template('cadastro.html')
        if e.orig.pgcode == '23503':
            # FOREIGN KEY VIOLATION
            return jsonify({'status':False, 'erro': "Chave estrangeira", 'codigo':f'{e}'}), HTTP_409_CONFLICT

        if e.orig.pgcode == '23505':
            # UNIQUE VIOLATION
            return jsonify({'status':False, 'erro': False, 'codigo':f'{e}'}), HTTP_401_UNAUTHORIZED

        if e.orig.pgcode == '01004':
            #STRING DATA RIGHT TRUNCATION
            return jsonify({'status':False, 'erro': False, 'codigo':f'{e}'}), HTTP_506_VARIANT_ALSO_NEGOTIATES

        #flash("Erro, 4 não salva")
        return jsonify({'status':False, 'erro': 'Não foi tratado', 'codigo':f'{e}'}), HTTP_400_BAD_REQUEST  



@cadastros.post('/populacao')
@swag_from('../docs/cadastros/populacao.yaml')
def populacao():

    formulario = request.get_json()
    populacao = Populacao(**formulario)

    try:
        #inseri no banco de dados. Tabela populacao
        db.session.add(populacao)
        db.session.commit()

        return jsonify({'status':True, 'id': populacao.id, "data":populacao.to_json()}), HTTP_200_OK

    except exc.DBAPIError as e:
        formulario_cadastro = render_template('cadastro.html')
        if e.orig.pgcode == '23503':
            # FOREIGN KEY VIOLATION
            return jsonify({'status':False, 'erro': "Chave estrangeira", 'codigo':f'{e}'}), HTTP_409_CONFLICT

        if e.orig.pgcode == '23505':
            # UNIQUE VIOLATION
            return jsonify({'status':False, 'erro': False, 'codigo':f'{e}'}), HTTP_401_UNAUTHORIZED

        if e.orig.pgcode == '01004':
            #STRING DATA RIGHT TRUNCATION
            return jsonify({'status':False, 'erro': False, 'codigo':f'{e}'}), HTTP_506_VARIANT_ALSO_NEGOTIATES

        #flash("Erro, 4 não salva")
        return jsonify({'status':False, 'erro': 'Não foi tratado', 'codigo':f'{e}'}), HTTP_400_BAD_REQUEST


#Cadastros das areas umidas
@cadastros.post('/area-umida')
@swag_from('../docs/cadastros/area-umida.yaml')
def area_umida():

    formulario = request.get_json()
    umida = AreaUmida(**formulario)

    try:
        #inseri no banco de dados. Tabela AreaUmida
        db.session.add(umida)
        db.session.commit()

        return jsonify({'status':True, 'id': umida.id, "data":umida.to_json()}), HTTP_200_OK

    except exc.DBAPIError as e:
        formulario_cadastro = render_template('cadastro.html')
        if e.orig.pgcode == '23503':
            # FOREIGN KEY VIOLATION
            return jsonify({'status':False, 'erro': "Chave estrangeira", 'codigo':f'{e}'}), HTTP_409_CONFLICT

        if e.orig.pgcode == '23505':
            # UNIQUE VIOLATION
            return jsonify({'status':False, 'erro': False, 'codigo':f'{e}'}), HTTP_401_UNAUTHORIZED

        if e.orig.pgcode == '01004':
            #STRING DATA RIGHT TRUNCATION
            return jsonify({'status':False, 'erro': False, 'codigo':f'{e}'}), HTTP_506_VARIANT_ALSO_NEGOTIATES

        #flash("Erro, 4 não salva")
        return jsonify({'status':False, 'erro': 'Não foi tratado', 'codigo':f'{e}'}), HTTP_400_BAD_REQUEST


@cadastros.post('/equipamentos')
@swag_from('../docs/cadastros/equipamentos.yaml')
def equipamentos():

    formulario = request.get_json()
    equipamento = Equipamentos(**formulario)

    try:
        #inseri no banco de dados. Tabela Equipamentos
        db.session.add(equipamento)
        db.session.commit()

        return jsonify({'status':True, 'id': equipamento.id, "data":equipamento.to_json()}), HTTP_200_OK

    except exc.DBAPIError as e:
        formulario_cadastro = render_template('cadastro.html')
        if e.orig.pgcode == '23503':
            # FOREIGN KEY VIOLATION
            return jsonify({'status':False, 'erro': "Chave estrangeira", 'codigo':f'{e}'}), HTTP_409_CONFLICT

        if e.orig.pgcode == '23505':
            # UNIQUE VIOLATION
            return jsonify({'status':False, 'erro': False, 'codigo':f'{e}'}), HTTP_401_UNAUTHORIZED

        if e.orig.pgcode == '01004':
            #STRING DATA RIGHT TRUNCATION
            return jsonify({'status':False, 'erro': False, 'codigo':f'{e}'}), HTTP_506_VARIANT_ALSO_NEGOTIATES

        #flash("Erro, 4 não salva")
        return jsonify({'status':False, 'erro': 'Não foi tratado', 'codigo':f'{e}'}), HTTP_400_BAD_REQUEST