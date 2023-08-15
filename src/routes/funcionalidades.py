from flask import Blueprint, jsonify, request
from ..constants.http_status_codes import HTTP_200_OK
from ..models import AreaUmida, TipoAreaUmida

funcionalidades = Blueprint('funcionalidades', __name__, url_prefix = '/api/v1/funcionalidades')



@funcionalidades.get('/quantidades_au_edificio')
def quantidades_au_edificio():

    fk_edificios = request.args.get('')
    quantidade_area_umidas = AreaUmida.query.filter_by(fk_edificios=fk_edificios).count()
    return jsonify({
        'Quantidade Areas umidas':quantidade_area_umidas
    })


@funcionalidades.get("/testando")
def area_umida():

    tipoareaumidaequipamento = {
        "Banheiro": [
            "Bacia sanitária Caixa de descarga", 
            "Bacia sanitária Válvula de descarga",
            "Chuveiro ou ducha",
            "Chuveiro elétrico"
        ]
    }

    for key, values in tipoareaumidaequipamento.items():
        return jsonify({
            'tipo':values
        })
        # for key in areaequipamento:
        #     tipoarea = TipoAreaUmida.query.filter_by(tipo=key).first()
        #     return jsonify({
        #         "tipo": key
        #     })
            