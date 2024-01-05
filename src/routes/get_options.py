from flask import Blueprint, jsonify, request
from ..models import ( db, Customizados, Escolas, EscolaNiveis, AuxOpNiveis, AuxTipoAreaUmida, 
AuxTiposEquipamentos, AuxPopulacaoPeriodo, AreaUmida, AuxTipoDeAreaUmidaTipoDeEquipamento, AuxOperacaoAreaUmida )
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from flasgger import swag_from

options = Blueprint('options', __name__, url_prefix='/api/v1/options')

# Escola
@swag_from('../docs/get/niveis.yaml')
@options.get('/niveis')
def niveis():

    opcoes_pers = AuxOpNiveis.query.all()
    opcoes_pre_definidos = [op.nivel for op in opcoes_pers]
    opcoes_personalizadas = Customizados.query.filter(Customizados.nivel_escola != None).all()
    # opcoes_personalizadas = Customizados.query.all()
    # opcoes_pers_str = [
    #     o.nivel_escola for o in opcoes_personalizadas if o.nivel_escola]
    opcoes_pers_str = [
        o.nivel_escola for o in opcoes_personalizadas]
    options = opcoes_pre_definidos + opcoes_pers_str
    return jsonify(options)


   
# AreaUmida
@swag_from('../docs/get/tipo_area_umida.yaml')
@options.get('/tipo_area_umida')
def tipo_area_umida():
    opcoes_pers = AuxTipoAreaUmida.query.all()
    opcoes_pre_definidos = [op.tipo for op in opcoes_pers]
    opcoes_personalizadas = Customizados.query.filter(Customizados.tipo_area_umida != None).all()
    options = opcoes_pre_definidos + \
        [o.tipo_area_umida for o in opcoes_personalizadas]
    return jsonify(options)



@swag_from('../docs/get/operacao_area_umida.yaml')
@options.get('operacao_area_umida')
def operacao_area_umida():

    opcoes_pers = AuxOperacaoAreaUmida.query.all()
    opcoes_pre_definidos = [op.operacao for op in opcoes_pers]
    return jsonify(opcoes_pre_definidos)



# Equipamentos
@swag_from('../docs/get/tipo_equipamento.yaml')
@options.get('/tipo_equipamento/<int:area_umida>')
def tipo_equipamento(area_umida):
    tipoareaumida = AreaUmida.query.filter_by(id=area_umida).first()

    if tipoareaumida:
        tipoareaumida_id = tipoareaumida.tipo_area_umida
    else:
        return jsonify([])

    opcoes_pers = AuxTipoDeAreaUmidaTipoDeEquipamento.query.filter_by(tipo_area_umida_id=tipoareaumida_id).all()
    opcoes_pre_definidos = [op.to_json()['tipo'] for op in opcoes_pers]
    print(opcoes_pre_definidos)
    return jsonify({
        "tipoequipamentos": opcoes_pre_definidos
    })


# Populacao
@swag_from('../docs/get/periodo.yaml')
@options.get('/periodo')
def periodo():

    opcoes_pers = AuxPopulacaoPeriodo.query.all()
    opcoes_pre_definidos = [op.periodo for op in opcoes_pers]
    # opcoes_personalizadas = Customizados.query.all()
    opcoes_personalizadas = Customizados.query.filter(Customizados.periodo_populacao != None).all()
    opcoes_pers_str = [o.periodo_populacao for o in opcoes_personalizadas]
    options = opcoes_pre_definidos + opcoes_pers_str
    return jsonify(options)

 
@swag_from('../docs/get/nivel_populacao.yaml')
@options.get('/nivel_populacao/<int:id>')
def nivel_populacao(id):
    escola = Escolas.query.filter_by(id=id).first()

    if not escola:
        return jsonify({'mensagem': 'Escola não encontrado', "status": False}), 404

    result = db.session.query(EscolaNiveis.escola_id, AuxOpNiveis.nivel) \
        .join(AuxOpNiveis, AuxOpNiveis.id == EscolaNiveis.nivel_ensino_id) \
        .filter(EscolaNiveis.escola_id == escola.id) \
        .all()

    serialized_result = [nivel for escola_id, nivel in result]
    # return serialized_result

    opcoes_personalizadas = Customizados.query.all()
    options = []

    if escola:
        options.extend(serialized_result)
    options.extend(
        o.nivel_escola for o in opcoes_personalizadas if o.nivel_escola)

    return jsonify(options)


