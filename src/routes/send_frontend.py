from flask import Blueprint, jsonify, request, render_template
from ..constants.http_status_codes import (HTTP_200_OK)
from sqlalchemy import exc
from ..models import Escolas, Edificios, AreaUmida, Equipamentos
from flasgger import swag_from

send_frontend = Blueprint('send_frontend', __name__, url_prefix = '/api/v1/send_frontend')


@send_frontend.get('/cadastro-escolas')
def cadastro_escolas():
    return render_template("cadastro.html")


@send_frontend.get('/escolas')
@swag_from('../docs/send_frontend/escolas.yaml')
def escolas():

    escolas = Escolas.query.all()
    return jsonify({'return':[escola.to_json() for escola in escolas]}), HTTP_200_OK

@send_frontend.get('/edificios')
@swag_from('../docs/send_frontend/edificios.yaml')
def edificios():
    fk_escola = request.args.get('')
    edificios = Edificios.query.filter_by(fk_escola=fk_escola).all()
    return jsonify({f'Edificios {fk_escola}': [edificio.to_json() for edificio in edificios]}), HTTP_200_OK

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