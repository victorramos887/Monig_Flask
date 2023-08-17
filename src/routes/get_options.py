from flask import Blueprint, jsonify, request
from src.models.models import TiposEquipamentos
from ..models import ( db, Customizados, Escolas, EscolaNiveis, OpNiveis, TipoAreaUmida, 
TiposEquipamentos, PopulacaoPeriodo, AreaUmida, TipoDeAreaUmidaTipoDeEquipamento, OperacaoAreaUmida )
from sqlalchemy import select
from sqlalchemy.orm import joinedload

options = Blueprint('options', __name__, url_prefix='/api/v1/options')

# Escola
@options.get('/niveis')
def niveis():

    opcoes_pers = OpNiveis.query.all()
    opcoes_pre_definidos = [op.nivel for op in opcoes_pers]
    opcoes_personalizadas = Customizados.query.all()
    opcoes_pers_str = [
        o.nivel_escola for o in opcoes_personalizadas if o.nivel_escola]
    options = opcoes_pre_definidos + opcoes_pers_str
    return jsonify(options)

# AreaUmida
@options.get('/tipo_area_umida')
def tipo_area_umida():
    opcoes_pers = TipoAreaUmida.query.all()
    opcoes_pre_definidos = [op.tipo for op in opcoes_pers]
    opcoes_personalizadas = Customizados.query.all()
    options = opcoes_pre_definidos + \
        [o.tipo_area_umida for o in opcoes_personalizadas]
    return jsonify(options)



@options.get('operacao_area_umida')
def operacao_area_umida():

    opcoes_pers = OperacaoAreaUmida.query.all()
    opcoes_pre_definidos = [op.operacao for op in opcoes_pers]
    return jsonify(opcoes_pre_definidos)


# Equipamentos
@options.get('/tipo_equipamento/<int:area_umida>')
def tipo_equipamento(area_umida):
    tipoareaumida = AreaUmida.query.filter_by(id=area_umida).first()

    if tipoareaumida:
        tipoareaumida_id = tipoareaumida.tipo_area_umida
    else:
        return jsonify([])

    opcoes_pers = TipoDeAreaUmidaTipoDeEquipamento.query.filter_by(tipo_area_umida_id=tipoareaumida_id).all()
    opcoes_pre_definidos = [op.to_json()['tipo'] for op in opcoes_pers]
    print(opcoes_pre_definidos)
    return jsonify({
        "tipoequipamentos": opcoes_pre_definidos
    })

# Populacao
@options.get('/periodo')
def periodo():

    opcoes_pers = PopulacaoPeriodo.query.all()
    opcoes_pre_definidos = [op.opcao for op in opcoes_pers]
    opcoes_personalizadas = Customizados.query.all()
    options = opcoes_pre_definidos + \
        [o.periodo_populacao for o in opcoes_personalizadas]
    return jsonify(options)



@options.get('/nivel_populacao/<int:id>')
def nivel_populacao(id):
    escola = Escolas.query.filter_by(id=id).first()

    if not escola:
        return jsonify({'mensagem': 'Escola não encontrado', "status": False}), 404

    result = db.session.query(EscolaNiveis.escola_id, OpNiveis.nivel) \
        .join(OpNiveis, OpNiveis.id == EscolaNiveis.nivel_ensino_id) \
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


