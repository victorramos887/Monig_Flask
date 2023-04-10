from flask import Blueprint, jsonify, request, render_template, flash, render_template_string
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_506_VARIANT_ALSO_NEGOTIATES, HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED
from ..models import Escolas, Edificios, db, AreaUmida, Equipamentos, Populacao
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

    return 'ok'

#EDITAR EDIFICIOS
@editar.put('/edificios/<id>')
def edificios_editar(id):
    edificio = Edificios.query.filter_by(id=id).first()
    body = request.get_json()

    if not edificio:
        return jsonify({'mensagem': 'Edificio não encontrado'}), 404
    
    edificio.update(**body)

    db.session.commit()

    return 'ok'

#EDITAR POPULACAO
@editar.put('/populacao/<id>')
def populacao_editar(id):
    populacao = Populacao.query.filter_by(id=id).first()
    body = request.get_json()

    if not populacao:
        return jsonify({'mensagem': 'Populacao não encontrado'}), 404
    
    populacao.update(**body)

    db.session.commit()

    return 'ok'


#EDITAR AREA UMIDA
@editar.put('/area-umida/<id>')
def area_umida_editar(id):
    umida = AreaUmida.query.filter_by(id=id).first()
    body = request.get_json()

    if not umida:
        return jsonify({'mensagem': 'Area Umida não encontrado'}), 404
    
    umida.update(**body)

    db.session.commit()

    return 'ok'

#EDITAR EQUIPAMENTO
@editar.put('/equipamentos/<id>')
def equipamento_editar(id):
    equipamento = Equipamentos.query.filter_by(id=id).first()
    body = request.get_json()

    if not equipamento:
        return jsonify({'mensagem': 'Equipamento não encontrado'}), 404
    
    equipamento.update(**body)

    db.session.commit()

    return 'ok'

