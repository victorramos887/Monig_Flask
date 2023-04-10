from flask import Blueprint, jsonify, request, render_template
from ..constants.http_status_codes import (HTTP_200_OK, HTTP_400_BAD_REQUEST)
from sqlalchemy import exc, func
from ..models import Escolas, Edificios, AreaUmida, Equipamentos, Populacao, db
from flasgger import swag_from

send_frontend = Blueprint('send_frontend', __name__, url_prefix = '/api/v1/send_frontend')

#RETORNA TODAS AS ESCOLAS
@send_frontend.get('/escolas')
@swag_from('../docs/send_frontend/escolas.yaml')
def escolas():

    escolas = Escolas.query.all()
    return jsonify({'return':[escola.to_json() for escola in escolas]}), HTTP_200_OK

#RETORNA APENAS UMA ESCOLA
@send_frontend.get('/escolas/<int:id>')
def get_escolas(id):
    escola = Escolas.query.filter_by(id=id).first()
    return jsonify({'escola':escola.to_json() if escola is not None else escola})

#RETORNA TODOS OS ESDIFICOS DA ESCOLA PARA MONTAR A TABELA
@send_frontend.get('/edificios-table/<int:id>')
@swag_from('../docs/send_frontend/edificios.yaml')
def edificios(id):
    edificios = Edificios.query.filter(Edificios.fk_escola == id).all()
    result = []

    for edificio in edificios:
        #População
        soma_colaboradores, soma_alunos = (
        db.session.query(
            func.sum(Populacao.quant_de_colaboradores).label('soma_colaboradores'),
            func.sum(Populacao.quant_de_colaboradores).label('soma_alunos')
            )
            .join(Edificios)
            .filter(Populacao.fk_edificios == edificio.id)
            .first()
        )
        #Area umida
        result.append({
            'id': edificio.id,
            'nome':edificio.nome_do_edificio,
            'soma_colaboradores': (soma_colaboradores or 0) + (soma_alunos or 0) or 0,
            'soma_alunos':soma_alunos or 0
        })

    return jsonify({'edificios':result}), HTTP_200_OK

#RETORNA APENAS O EDIFICIO QUE DESEJA ATUALIZAR
@send_frontend.get('/edificio/<id>')
def edificio(id):

    edificio = Edificios.query.filter(Edificios.id == id).first()
    if edificio is None or edificio == '':
        return jsonify({'erro':'Edificio não encontrado'}), HTTP_400_BAD_REQUEST

    return jsonify({'edificio':edificio.to_json()}), HTTP_200_OK


@send_frontend.get('/area_umidas')
@swag_from('../docs/send_frontend/area_umidas.yaml')
def area_umidas():
    fk_edificios = request.args.get('')
    areas_umidas = AreaUmida.query.filter_by(fk_edificios = fk_edificios).all()
    return jsonify({f'Areas Umidas {fk_edificios}':[area_umida.to_json() for area_umida in areas_umidas]}), HTTP_200_OK

@send_frontend.get('/equipamentos')
@swag_from('../docs/send_frontend/equipamentos.yaml')
def equipamentos():
    fk_area_umida = request.args.get('')
    equipamentos = Equipamentos.query.filter_by(fk_area_umida = fk_area_umida).all()

    return jsonify({
        f'Equipamentos {fk_area_umida}':[equipamento.to_json() for equipamento in equipamentos]
    }), HTTP_200_OK