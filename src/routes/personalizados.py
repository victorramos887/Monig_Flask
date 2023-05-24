
from flask import Blueprint, jsonify, request
from ..models import db, Nivel, TipoArea, StatusArea, TipoEquipamento, DescricaoEquipamento, Periodo


personalizados= Blueprint('personalizados', __name__, url_prefix = '/api/v1/cadastrar/option')

@personalizados.post('/nivel')
def nivel():
    # Obtém os dados enviados pelo usuário através do formulário
    item_personalizado = request.get_json()
    nivel = Nivel(**item_personalizado)
   # criado_por = current_user.username 
    db.session.add(nivel)
    db.session.commit()
    return jsonify({'status':True}), 200

#AREA UMIDA
@personalizados.post('/tipo_area_umida')
def tipo_area_umida():
    # Obtém os dados enviados pelo usuário através do formulário
    item_personalizado = request.get_json()
    tipo = TipoArea(**item_personalizado)
   # criado_por = current_user.username 
    db.session.add(tipo)
    db.session.commit()
    return jsonify({'status':True}), 200

@personalizados.post('/status_area_umida')
def status_area_umida():
    # Obtém os dados enviados pelo usuário através do formulário
    item_personalizado = request.get_json()
    status = StatusArea(**item_personalizado)
   # criado_por = current_user.username 
    db.session.add(status)
    db.session.commit()
    return jsonify({'status':True}), 200

#Equipamento
@personalizados.post('/tipo_equipamento')
def tipo_equipamento():
    # Obtém os dados enviados pelo usuário através do formulário
    item_personalizado = request.get_json()
    tipo = TipoEquipamento(**item_personalizado)
   # criado_por = current_user.username 
    db.session.add(tipo)
    db.session.commit()
    return jsonify({'status':True}), 200

@personalizados.post('/descricao_equipamento')
def descricao_equipamento():
    # Obtém os dados enviados pelo usuário através do formulário
    item_personalizado = request.get_json()
    tipo_equipamento = DescricaoEquipamento(**item_personalizado)
   # criado_por = current_user.username 
    db.session.add(tipo_equipamento)
    db.session.commit()
    return jsonify({'status':True}), 200


#Populacao
@personalizados.post('/periodo')
def periodo():
    # Obtém os dados enviados pelo usuário através do formulário
    item_personalizado = request.get_json()
    periodo = Periodo(**item_personalizado)
   # criado_por = current_user.username 
    db.session.add(periodo)
    db.session.commit()
    return jsonify({'status':True}), 200