from flask import Blueprint, jsonify, request, render_template, flash, render_template_string
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_506_VARIANT_ALSO_NEGOTIATES, HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED
from ..models import Escolas, Edificios, db, AreaUmida, Equipamentos, Populacao, Hidrometros
from sqlalchemy import exc

remover = Blueprint('remover', __name__, url_prefix='/api/v1/remover')

#EDITAR ESCOLA
@remover.put('/escolas/<id>')
def escolas_remover(id):
    escola = Escolas.query.filter_by(id=id).first()
    escola.status = False

    if not escola:
        return jsonify({'mensagem': 'Escola não encontrado'}), 404
    
   
    db.session.commit()

    return jsonify(), HTTP_200_OK


#edificios
@remover.put('/edificios/<id>')
def edificios_remover(id):
    edificio = Edificios.query.filter_by(id=id).first()
    edificio.status = False

    if not edificio:
        return jsonify({'mensagem': 'Edificio não encontrado'}), 404
    
   
    db.session.commit()

    return jsonify(), HTTP_200_OK


#hidrometro
@remover.put('/hidrometros/<id>')
def hidrometro_remover(id):
    hidrometro = Hidrometros.query.filter_by(id=id).first()
    hidrometro.status = False

    if not hidrometro:
        return jsonify({'mensagem': 'hidrometro não encontrado'}), 404
    
    db.session.commit()

    return jsonify(), HTTP_200_OK


#populacao
@remover.put('/populacao/<id>')
def populacao_remover(id):
    populacao = Populacao.query.filter_by(id=id).first()
    populacao.status = False

    if not populacao:
        return jsonify({'mensagem': 'População não encontrado'}), 404
    
   
    db.session.commit()

    return jsonify(), HTTP_200_OK


#area-umida
@remover.put('/area-umida/<id>')
def area_umida_remover(id):
    umida = AreaUmida.query.filter_by(id=id).first()
    umida.status = False

    if not umida:
        return jsonify({'mensagem': 'Area Umida não encontrado'}), 404
    
   
    db.session.commit()

    return jsonify(), HTTP_200_OK


#equipamentos
@remover.put('/equipamentos/<id>')
def equipamentos_remover(id):
    equipamento = Equipamentos.query.filter_by(id=id).first()
    equipamento.status = False

    if not equipamento:
        return jsonify({'mensagem': 'Equipamento não encontrado'}), 404
    
   
    db.session.commit()

    return jsonify(), HTTP_200_OK
