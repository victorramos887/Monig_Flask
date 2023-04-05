from flask import Blueprint, jsonify, request, render_template, flash, render_template_string, current_app
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_506_VARIANT_ALSO_NEGOTIATES, HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED
from sqlalchemy import exc
from flasgger import swag_from
from ..models import Escolas, Edificios, db, AreaUmida, Equipamentos, Populacao
import string
import json
import re


cadastros = Blueprint('cadastros', __name__, url_prefix = '/api/v1/cadastros')


#Cadastros das escolas
@cadastros.post('/escolas')
@swag_from('../docs/cadastros/escolas.yaml')
def escolas():
    #Captura as informações que foram enviadas através do formulário HTML
    json_data = request.get_data()
    json_str = json_data.decode('utf-8', errors='ignore')
    clean_json_str = ''.join(filter(lambda x: x in string.printable, json_str))
    formulario = json.loads(clean_json_str)

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

    #Captura as informações que foram enviadas através do formulário HTML
    formulario = request.get_json()
    edificio = Edificios(**formulario)
    try:
        #inseri no banco de dados. Tabela escolas
        db.session.add(edificio)
        db.session.commit()
        return jsonify({'status':True, 'id': edificio.id, "data":edificio.to_json()}), HTTP_200_OK

    except exc.DBAPIError as e:
        if e.orig.pgcode == '23503':
            # FOREIGN KEY VIOLATION
            return jsonify({'status':False, 'erro': 'Erro Não tratado', 'codigo':f'{e}'}), HTTP_409_CONFLICT
        return jsonify({'status':False, 'erro': 'Erro Não tratado', 'codigo':f'{e}'}), HTTP_400_BAD_REQUEST

@cadastros.post('/populacao')
def populacao():

    #Captura as informações que foram enviadas através do formulário HTML
    # formulario = request.form.to_dict()
    formulario = request.get_json()
    populacao = Populacao(**formulario)
    try:
        #inseri no banco de dados. Tabela escolas
        db.session.add(populacao)
        db.session.commit()
        return  render_template('index.html')

    except exc.DBAPIError as e:
        if e.orig.pgcode == '23503':
            return jsonify({'Erro':'Escola já cadastrada!'})
        return jsonify({"Erro":f'Erro ao enviar! ({e})'})


#Cadastros das areas umidas
@cadastros.post('/area-umida')
@swag_from('../docs/cadastros/area-umidas.yaml')
def area_umida():

    #Captura as informações que foram enviadas através do formulário HTML
    # formulario = request.form.to_dict()
    formulario = request.form.to_dict()
    umida = AreaUmida(**formulario)
    try:
        #inseri no banco de dados. Tabela escolas
        db.session.add(umida)
        db.session.commit()
        return  render_template('index.html')

    except exc.DBAPIError as e:
        if e.orig.pgcode == '23503':
            return jsonify({'Erro':'Escola já cadastrada!'})
        return jsonify({"Erro":f'Erro ao enviar! ({e})'})

@cadastros.post('/equipamentos')
@swag_from('../docs/cadastros/equipamentos.yaml')
def equipamentos():

    #Captura as informações que foram enviadas através do formulário HTML
    formulario = request.form.to_dict()
    equipamento = Equipamentos(**formulario)
    try:
        #inseri no banco de dados. Tabela escolas
        db.session.add(equipamento)
        db.session.commit()
        return  render_template('index.html')

    except exc.DBAPIError as e:
        if e.orig.pgcode == '23503':
            return jsonify({'Erro':'Escola já cadastrada!'})
        return jsonify({"Erro":f'Erro ao enviar! ({e})'})
