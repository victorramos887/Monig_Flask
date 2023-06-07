from flask import Blueprint, jsonify, request

from src.models.models import TiposEquipamentos
from ..models import db, Customizados, Escolas, Opcoes


options = Blueprint('options', __name__, url_prefix = '/api/v1/options')

#Escola
@options.get('/niveis')
def niveis():

    opcoes_pers = Opcoes.query.filter_by(funcao="Nivel").all()
    opcoes_pre_definidos = [op.opcao for op in opcoes_pers]
    opcoes_personalizadas = Customizados.query.all()
    opcoes_pers_str = [o.nivel_escola for o in opcoes_personalizadas if o.nivel_escola]
    options = opcoes_pre_definidos + opcoes_pers_str
    return jsonify(options)


#AreaUmida
@options.get('/tipo_area_umida')
def tipo_area_umida():
    opcoes_pers = Opcoes.query.filter_by(funcao="Area-Umida").all()
    opcoes_pre_definidos = [op.opcao for op in opcoes_pers]
    opcoes_personalizadas = Customizados.query.all()
    options = opcoes_pre_definidos + [o.tipo_area_umida for o in opcoes_personalizadas]
    return jsonify(options)


@options.get('/status_area_umida')
def status_area_umida():
    opcoes_pers = Opcoes.query.filter_by(funcao="Status-Area-Umida").all()
    opcoes_pre_definidos = [op.opcao for op in opcoes_pers] 
    opcoes_personalizadas = Customizados.query.all()
    options = opcoes_pre_definidos + [o.status_area_umida for o in opcoes_personalizadas]
    return jsonify(options)

#Equipamentos
@options.get('/tipo_equipamento')
def tipo_equipamento():
    opcoes_pers = Opcoes.query.filter_by(funcao="Equipamentos").all()
    opcoes_pre_definidos = [op.opcao for op in opcoes_pers]
    opcoes_personalizadas = Customizados.query.all()
    options = opcoes_pre_definidos + [o.tipo_equipamento for o in opcoes_personalizadas]
    return jsonify(options)

@options.get('/descricao_equipamento')
def descricao_equipamento():
    opcoes_pers = TiposEquipamentos.query.all()
    opcoes_pre_definidos = [{op.equipamento:op.tipos} for op in opcoes_pers]   

    return jsonify({"tipos":opcoes_pre_definidos})

#Populacao
@options.get('/periodo')
def periodo():

    opcoes_pers = Opcoes.query.filter_by(funcao="Periodo").all()
    opcoes_pre_definidos = [op.opcao for op in opcoes_pers]
    opcoes_personalizadas = Customizados.query.all() 
    options = opcoes_pre_definidos + [o.periodo_populacao for o in opcoes_personalizadas]
    return jsonify(options)

@options.get('/nivel_populacao/<int:id>')
def nivel_populacao(id):
    escola = Escolas.query.filter_by(id=id).first()
    
    if not escola:
        return jsonify({'mensagem': 'Escola não encontrado', "status": False}), 404
    
    opcoes_personalizadas = Customizados.query.all() 
    
    options = []
    if escola:
        options.extend(escola.nivel)
    options.extend(o.nivel_escola for o in opcoes_personalizadas if o.nivel_escola)
    
    return jsonify(options)

