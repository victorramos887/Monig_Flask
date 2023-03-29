from flask import Blueprint, jsonify, request, render_template, flash, render_template_string, current_app
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_506_VARIANT_ALSO_NEGOTIATES, HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED
from sqlalchemy import exc
from flasgger import swag_from
from ..models import Escolas, Edificios, db, AreaUmida, Equipamentos
import string
import json
import re


cadastros = Blueprint('cadastros', __name__, url_prefix = '/api/v1/cadastros')


@cadastros.route('/testes', methods=['POST', 'GET'])
def teste_de_rota():
    if request.method == 'POST':
        valor_retorno = request.get_data()
        return valor_retorno
    else:
        return 'Valor, do resultado!!!'


#Cadastros das escolas
@cadastros.post('/escolas')
@swag_from('../docs/cadastros/escolas.yaml')
def escolas():
    #Captura as informações que foram enviadas através do formulário HTML
    json_data = request.get_data()
    json_str = json_data.decode('utf-8', errors='ignore')
    clean_json_str = ''.join(filter(lambda x: x in string.printable, json_str))
    formulario = json.loads(clean_json_str)
    cache = list(current_app.extensions['cache'].values())[0]
    escola = Escolas(**formulario) #Atribui ao objeto escola

    try:
        #inseri no banco de dados. Tabela escolas
        db.session.add(escola)
        db.session.commit()
        cache.set('id_escola', 1)
        novo_formulario = render_template('form_edificacoes.html')
        return jsonify({'success':True, 'edificios':novo_formulario, 'id_escola': cache.get('id_escola')}), HTTP_200_OK

    except exc.DBAPIError as e:
        formulario_cadastro = render_template('cadastro.html')
        if e.orig.pgcode == '23503':
            # FOREIGN KEY VIOLATION
            return jsonify({'erro': False, 'form':formulario_cadastro, 'codigo':e}), HTTP_409_CONFLICT

        if e.orig.pgcode == '23505':
            # UNIQUE VIOLATION
            return jsonify({'erro': False, 'form':formulario_cadastro, 'codigo':e}), HTTP_401_UNAUTHORIZED

        if e.orig.pgcode == '01004':
            #STRING DATA RIGHT TRUNCATION
            return jsonify({'erro': False, 'form':formulario_cadastro, 'codigo':e}), HTTP_506_VARIANT_ALSO_NEGOTIATES

        #flash("Erro, 4 não salva")
        return jsonify({'erro': False, 'form':formulario_cadastro, 'codigo':e}), HTTP_400_BAD_REQUEST


#Cadastros dos edifícios.
@cadastros.post('/edificios')
@swag_from('../docs/cadastros/edificios.yaml')
def edificios():

    #Captura as informações que foram enviadas através do formulário HTML
    formulario = request.form.to_dict()
    edificio = Edificios(**formulario)
    try:
        #inseri no banco de dados. Tabela escolas
        db.session.add(edificio)
        db.session.commit()
        novo_formulario = '<div>Formulário de áreas humidas</div>'
        return  jsonify({'success':True}), HTTP_200_OK

    except exc.DBAPIError as e:
        if e.orig.pgcode == '23503':
            # FOREIGN KEY VIOLATION
            return jsonify({'erro': False, 'codigo':e}), HTTP_409_CONFLICT
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
