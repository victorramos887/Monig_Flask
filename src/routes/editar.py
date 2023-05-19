from flask import Blueprint, jsonify, request, render_template, flash, render_template_string
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_506_VARIANT_ALSO_NEGOTIATES, HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED
from ..models import Escolas, Edificios, db, AreaUmida, Equipamentos, Populacao, Hidrometros, EscolasHistorico
from sqlalchemy import exc
from http import HTTPStatus

editar = Blueprint('editar', __name__, url_prefix='/api/v1/editar')

#EDITAR ESCOLA
@editar.put('/escolas/<id>')
def escolas_editar(id):
    escola = Escolas.query.filter_by(id=id).first()
    body = request.get_json()

    if not escola:
        return jsonify({'mensagem': 'Escola não encontrado', "status": False}), 404

    #comparar e incluir na tabela EscolasHistorico
    if escola != body:
        db.session.add(EscolasHistorico(fk_escola=escola.id, cnpj=escola.cnpj, cep=escola.cep, nivel=escola.nivel))

    #atualizar tabela Escola - novas informações
    escola.update(**body)

    db.session.commit()
  
    return jsonify({"escola": escola.to_json(),"mensagem":"Ediçao ok", "status": True}), HTTP_200_OK 
  

#EDITAR EDIFICIOS
@editar.put('/edificios/<id>')
def edificios_editar(id):
    edificio = Edificios.query.filter_by(id=id).first()
    body = request.get_json()

    if not edificio:
        return jsonify({'mensagem': 'Edificio não encontrado',"status": False}), 404

    edificio.update(**body)

    db.session.commit()

    return jsonify({"edificio":edificio.to_json(), "status": True}), HTTP_200_OK


#EDITAR HIDROMETRO
@editar.put('/hidrometros/<id>')
def hidrometro_editar(id):
    hidrometro = Hidrometros.query.filter_by(id=id).first()
    body = request.get_json()

    if not hidrometro:
        return jsonify({'mensagem': 'Hidrometro não encontrado', "status": False}), 404

    hidrometro.update(**body)

    db.session.commit()

    return jsonify({"hidrometro":hidrometro.to_json(), "status": True}), HTTP_200_OK


#EDITAR POPULACAO
@editar.put('/populacao/<id>')
def populacao_editar(id):
    populacao = Populacao.query.filter_by(id=id).first()
    body = request.get_json()

    if not populacao:
        return jsonify({'mensagem': 'Populacao não encontrado', "status": False}), 404

    populacao.update(**body)

    db.session.commit()

    return jsonify({"populacao":populacao.to_json(), "status": True}), HTTP_200_OK


#EDITAR AREA UMIDA
@editar.put('/area-umida/<id>')
def area_umida_editar(id):
    umida = AreaUmida.query.filter_by(id=id).first()
    body = request.get_json()

    if not umida:
        return jsonify({'mensagem': 'Area Umida não encontrado', "status": False}), 404
    
    umida.update(**body)

    db.session.commit()

    return jsonify({"areaumida":umida.to_json(), "status": True}), HTTP_200_OK

#EDITAR EQUIPAMENTO
@editar.put('/equipamentos/<id>')
def equipamento_editar(id):
    equipamento = Equipamentos.query.filter_by(id=id).first()
    body = request.get_json()

    if not equipamento:
        return jsonify({'mensagem': 'Equipamento não encontrado', "status": False}), 404

    equipamento.update(**body)

    db.session.commit()

    return jsonify({"equipamento":equipamento.to_json(), "status": True}), HTTP_200_OK