from flask import Blueprint, jsonify, request
from ..models import db, Nivel, TipoArea, StatusArea, TipoEquipamento, DescricaoEquipamento, Periodo, Escolas



options = Blueprint('options', __name__, url_prefix = '/api/v1/options')

#Escola
@options.get('/niveis')
def niveis():
    opcoes_pre_definidos = ['Fundamental', 'Médio', 'Superior', 'Creche', 'Berçario', 'CEU']
    opcoes_personalizadas = Nivel.query.all()
    options = opcoes_pre_definidos + [o.nivel for o in opcoes_personalizadas]
    return jsonify(options)

#AreaUmida
@options.get('/tipo_area_umida')
def tipo_area_umida():
    opcoes_pre_definidos = ['Cozinha', 'Banheiro', 'Bebedouro'] 
    opcoes_personalizadas = TipoArea.query.all()
    options = opcoes_pre_definidos + [o.tipo_area_umida for o in opcoes_personalizadas]
    return jsonify(options)


@options.get('/status_area_umida')
def status_area_umida():
    opcoes_pre_definidos = ['Aberto', 'Fechado'] 
    opcoes_personalizadas = StatusArea.query.all()
    options = opcoes_pre_definidos + [o.status_area_umida for o in opcoes_personalizadas]
    return jsonify(options)

#Equipamentos
@options.get('/tipo_equipamento')
def tipo_equipamento():
    opcoes_pre_definidos = ['Chuveiro', 'Torneira', 'Sanitário'] 
    opcoes_personalizadas = TipoEquipamento.query.all()
    options = opcoes_pre_definidos + [o.tipo for o in opcoes_personalizadas]
    return jsonify(options)

@options.get('/descricao_equipamento')
def descricao_equipamento():
    opcoes_pre_definidos = ['Chuveiro a gás', 
                            'Chuveiro pressurizado', 
                            'Sanitário com caixa acoplada', 
                            'Sanitário com descarga embutida'] 
    opcoes_personalizadas = DescricaoEquipamento.query.all() 
    options = opcoes_pre_definidos + [o.tipo_equipamento for o in opcoes_personalizadas]
    return jsonify(options)

#Populacao
@options.get('/periodo')
def periodo():
    opcoes_pre_definidos = ['Manhã', 'Tarde', 'Noite', 'Integral'] 
    opcoes_personalizadas = Periodo.query.all() 
    options = opcoes_pre_definidos + [o.periodo for o in opcoes_personalizadas]
    return jsonify(options)

@options.get('/nivel_populacao/<int:id>')
def nivel_populacao(id):
    escola = Escolas.query.filter_by(id=id)
    opcoes_personalizadas = Nivel.query.all() 
    options = [o.nivel for o in escola]  + [o.nivel for o in opcoes_personalizadas] 
    return jsonify(options)
    