from flask import Blueprint, jsonify, request, render_template, flash, render_template_string
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_506_VARIANT_ALSO_NEGOTIATES, HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED
from ..models import Escolas, Edificios, db, AreaUmida, Equipamentos, Populacao, Hidrometros
from sqlalchemy import exc

editar = Blueprint('editar', __name__, url_prefix='/api/v1/editar')

#EDITAR ESCOLA
@editar.put('/escolas/<id>')
def escolas_editar(id):
    escola = Escolas.query.filter_by(id=id).first()
    body = request.get_json()

    if not escola:
        return jsonify({'mensagem': 'Escola não encontrado'}), 404

    escola.update(**body)

    db.session.commit()

    return jsonify({"escola": escola.to_json()}), HTTP_200_OK

#EDITAR EDIFICIOS
@editar.put('/edificios/<id>')
def edificios_editar(id):
    edificio = Edificios.query.filter_by(id=id).first()
    body = request.get_json()

    if not edificio:
        return jsonify({'mensagem': 'Edificio não encontrado'}), 404

    edificio.update(**body)

    db.session.commit()

    return jsonify({"edificio":edificio.to_json()}), HTTP_200_OK


#EDITAR HIDROMETRO
@editar.put('/hidrometros/<id>')
def hidrometro_editar(id):
    hidrometro = Hidrometros.query.filter_by(id=id).first()
    body = request.get_json()

    if not hidrometro:
        return jsonify({'mensagem': 'Hidrometro não encontrado'}), 404

    hidrometro.update(**body)

    db.session.commit()

    return jsonify({"hidrometro":hidrometro.to_json()}), HTTP_200_OK


#EDITAR POPULACAO
@editar.put('/populacao/<id>')
def populacao_editar(id):
    populacao = Populacao.query.filter_by(id=id).first()
    body = request.get_json()

    if not populacao:
        return jsonify({'mensagem': 'Populacao não encontrado'}), 404

    populacao.update(**body)

    db.session.commit()

    return jsonify({"populacao":populacao.to_json()}), HTTP_200_OK


#EDITAR AREA UMIDA
@editar.put('/area-umida/<id>')
def area_umida_editar(id):
    umida = AreaUmida.query.filter_by(id=id).first()
    body = request.get_json()

    if not umida:
        return jsonify({'mensagem': 'Area Umida não encontrado'}), 404
    
    umida.update(**body)

    db.session.commit()

    return jsonify({"areaumida":umida.to_json}), HTTP_200_OK

#EDITAR EQUIPAMENTO
@editar.put('/equipamentos/<id>')
def equipamento_editar(id):
    equipamento = Equipamentos.query.filter_by(id=id).first()
    body = request.get_json()

    if not equipamento:
        return jsonify({'mensagem': 'Equipamento não encontrado'}), 404

    equipamento.update(**body)

    db.session.commit()

    return jsonify({"equipamento":equipamento.to_json}), HTTP_200_OK