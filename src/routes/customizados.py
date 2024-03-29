
from flask import Blueprint, jsonify, request
from ..models import db, Customizados
from flasgger import swag_from


customizados= Blueprint('customizados', __name__, url_prefix = '/api/v1/cadastrar/option')

# @swag_from('../docs/cadastros/nivel_customizado.yaml')
@customizados.post('/nivel')
def nivel():
    # Obtém os dados enviados pelo usuário através do formulário
    item_personalizado = request.get_json()
    nivel = Customizados(**item_personalizado)
   # criado_por = current_user.username 
    db.session.add(nivel)
    db.session.commit()
    return jsonify({'status':True}), 200

#AREA UMIDA
# @swag_from('../docs/cadastros/tipo_area_umida_customizado.yaml')
@customizados.post('/tipo_area_umida')
def tipo_area_umida():
    # Obtém os dados enviados pelo usuário através do formulário
    item_personalizado = request.get_json()
    tipo = Customizados(**item_personalizado)
   # criado_por = current_user.username 
    db.session.add(tipo)
    db.session.commit()
    return jsonify({'status':True}), 200


# @swag_from('../docs/cadastros/status_area_umida_customizado.yaml')
@customizados.post('/status_area_umida')
def status_area_umida():
    # Obtém os dados enviados pelo usuário através do formulário
    item_personalizado = request.get_json()
    status = Customizados(**item_personalizado)
   # criado_por = current_user.username 
    db.session.add(status)
    db.session.commit()
    return jsonify({'status':True}), 200

#Equipamento    
# @swag_from('../docs/cadastros/tipo_equipamento_customizado.yaml')
@customizados.post('/tipo_equipamento')
def tipo_equipamento():
    # Obtém os dados enviados pelo usuário através do formulário
    item_personalizado = request.get_json()
    tipo = Customizados(**item_personalizado)
   # criado_por = current_user.username 
    db.session.add(tipo)
    db.session.commit()
    return jsonify({'status':True}), 200

#Populacao
# @swag_from('../docs/cadastros/periodo_customizado.yaml')
@customizados.post('/periodo')
def periodo():
    # Obtém os dados enviados pelo usuário através do formulário
    item_personalizado = request.get_json()
    periodo = Customizados(**item_personalizado)
   # criado_por = current_user.username 
    db.session.add(periodo)
    db.session.commit()
    return jsonify({'status':True}), 200