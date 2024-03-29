from flask import Blueprint, jsonify, request
from ..models import AuxTiposEquipamentos, db


cadopcoes = Blueprint("cadopcoes", __name__,
                      url_prefix='/api/v1/cadastro_opcoes')

@cadopcoes.post('/tipos-equipamentos')
def tiposCadastro():

    # PEGAR INFORMACOES DO JSON
    sends = request.get_json()
    tipos = [AuxTiposEquipamentos(**send) for send in sends]
    db.session.add_all(tipos)
    db.session.commit()
    return jsonify({
        'mensagem': "enviado com sucesso!", 
        "enviado": [tipo.to_json() for tipo in tipos]
    })


