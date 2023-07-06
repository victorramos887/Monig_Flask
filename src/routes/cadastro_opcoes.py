from flask import Blueprint, jsonify, request
from ..models import TiposEquipamentos, db


cadopcoes = Blueprint("cadopcoes", __name__,
                      url_prefix='/api/v1/cadastro_opcoes')


# @cadopcoes.post('/opcao')
# def opcaoCadastro():

#     # PEGAR INFORMACOES DO JSON
#     send = request.get_json()
#     opcoes = Opcoes(**send)
#     db.session.add(opcoes)
#     db.session.commit()
#     return jsonify({'mensagem': "enviado com sucesso!", "enviado": opcoes.to_json()})


# @cadopcoes.post('/opcoes')
# def opcoesCadastro():

#     # PEGAR INFORMACOES DO JSON
#     sends = request.get_json()
#     opcoes = [Opcoes(**send) for send in sends]
#     print(opcoes)
#     db.session.add_all(opcoes)
#     db.session.commit()
#     return jsonify({
#         'mensagem': "enviado com sucesso!", 
#         "enviado": [opcao.to_json() for opcao in opcoes]
#     })


@cadopcoes.post('/tipos-equipamentos')
def tiposCadastro():

    # PEGAR INFORMACOES DO JSON
    sends = request.get_json()
    tipos = [TiposEquipamentos(**send) for send in sends]
    print(tipos)
    db.session.add_all(tipos)
    db.session.commit()
    return jsonify({
        'mensagem': "enviado com sucesso!", 
        "enviado": [tipo.to_json() for tipo in tipos]
    })


