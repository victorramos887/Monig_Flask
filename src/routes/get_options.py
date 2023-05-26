from flask import Blueprint, jsonify, request
from ..models import db, Customizados, Escolas


options = Blueprint('options', __name__, url_prefix = '/api/v1/options')

#Escola
@options.get('/niveis')
def niveis():
    opcoes_pre_definidos = ['Fundamental', 'Médio', 'Superior', 'Creche', 'Berçario', 'CEU']
    opcoes_personalizadas = Customizados.query.all()
    opcoes_pers_str = [o.nivel_escola for o in opcoes_personalizadas if o.nivel_escola]
    options = opcoes_pre_definidos + opcoes_pers_str
    return jsonify(options)
    

#AreaUmida
@options.get('/tipo_area_umida')
def tipo_area_umida():
    opcoes_pre_definidos = ['Cozinha', 'Banheiro', 'Bebedouro'] 
    opcoes_personalizadas = Customizados.query.all()
    options = opcoes_pre_definidos + [o.tipo_area_umida for o in opcoes_personalizadas]
    return jsonify(options)


@options.get('/status_area_umida')
def status_area_umida():
    opcoes_pre_definidos = ['Aberto', 'Fechado'] 
    opcoes_personalizadas = Customizados.query.all()
    options = opcoes_pre_definidos + [o.status_area_umida for o in opcoes_personalizadas]
    return jsonify(options)

#Equipamentos
@options.get('/tipo_equipamento')
def tipo_equipamento():
    opcoes_pre_definidos = ['Chuveiro', 'Torneira', 'Sanitário'] 
    opcoes_personalizadas = Customizados.query.all()
    options = opcoes_pre_definidos + [o.tipo_equipamento for o in opcoes_personalizadas]
    return jsonify(options)

@options.get('/descricao_equipamento')
def descricao_equipamento():
    opcoes_pre_definidos = ['Chuveiro a gás', 
                            'Chuveiro pressurizado', 
                            'Sanitário com caixa acoplada', 
                            'Sanitário com descarga embutida'] 
    opcoes_personalizadas = Customizados.query.all() 
    options = opcoes_pre_definidos + [o.descricao_equipamento for o in opcoes_personalizadas]
    return jsonify(options)

#Populacao
@options.get('/periodo')
def periodo():
    opcoes_pre_definidos = ['Manhã', 'Tarde', 'Noite', 'Integral'] 
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

    #ESTÁ RETORNANDO APENAS OS ITENS CUSTOMIZADOS
''' escola = Escolas.query.filter_by(id=id).all()
    opcoes_personalizadas = Customizados.query.all() 
    options = [o.nivel for o in escola]  + [o.nivel_escola for o in opcoes_personalizadas] 
    return jsonify(options)'''
    