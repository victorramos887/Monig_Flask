from flask import Blueprint, json, jsonify, request, render_template, flash, render_template_string
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_506_VARIANT_ALSO_NEGOTIATES, HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED
from ..models import Escolas, Edificios, Reservatorios, db, AreaUmida, Equipamentos, Populacao, Hidrometros, Historico, Eventos, TipoDeEventos
from sqlalchemy import exc, text

remover = Blueprint('remover', __name__, url_prefix='/api/v1/remover')



@remover.get('/retornar-historico')
def get_historico():

    historicos = [historia.to_json() for historia in Historico.query.all()]

    return jsonify(historicos)
    

#EDITAR ESCOLA
@remover.put('/escolas/<id>')
def escolas_remover(id):
    escola = Escolas.query.filter_by(id=id).first()

    if not escola:
        return jsonify({'status':False,'mensagem': 'Escola não encontrado'}), 404
    
    #alterar status da linha para False
    escola.status_do_registro = False

     # Insere os dados da linha excluída na tabela de histórico
    escola_json = escola.to_json()
    escola_json['data_criacao'] = escola_json['data_criacao'].strftime('%m/%d/%Y %H:%M:%S')
    
    historico = Historico(tabela='Escolas', dados=escola_json)
    db.session.add(historico)
    
    # Confirma as alterações no banco de dados
    db.session.commit()

    return jsonify({"status": True, 'mensagem': 'Escola removida'}), HTTP_200_OK 

 
    
#edificios
@remover.delete('/edificios/<id>')
def edificios_remover(id):
    edificio = Edificios.query.filter_by(id=id).first()


    try:
        if not edificio:
            return jsonify({'status':False,'mensagem': 'Edificio não encontrado'}), 404
    
        area_umidas =  AreaUmida.query.filter_by(fk_edificios=id).all()

        if area_umidas:
            for area_umida in area_umidas:
                equipamentos = Equipamentos.query.filter_by(fk_area_umida=area_umida.id).all()
                if equipamentos:
                    for equipamento in equipamentos:
                        equipamento.status_do_registro = False
                area_umida.status_do_registro = False

        populacoes = Populacao.query.filter_by(fk_edificios=id).all()

        if populacoes:
            for populacao in populacoes:
                populacao.status_do_registro = False

        hidrometros = Hidrometros.query.filter_by(fk_edificios=id).all()

        if hidrometros:
            for hidrometro in hidrometros:
                hidrometro.status_do_registro = False

        edificio.status_do_registro = False

        db.session.commit()
        return jsonify({"status": True, 'mensagem': 'Edificio removido'}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status":False, 'mensagem':"Erro não tratado", "codigo":str(e)
        }), 400


#hidrometro
@remover.put('/hidrometros/<id>')
def hidrometro_remover(id):
    hidrometro = Hidrometros.query.filter_by(id=id).first()
   
    if not hidrometro:
        return jsonify({'status':False,'mensagem': 'hidrometro não encontrado'}), 404
    
    hidrometro.status_do_registro = False
    db.session.commit()

    return jsonify({"status": True, 'mensagem': 'hidrometo removido'}), HTTP_200_OK 


#populacao
@remover.put('/populacao/<id>')
def populacao_remover(id):
    populacao = Populacao.query.filter_by(id=id).first()

    if not populacao:
        return jsonify({'status':False,'mensagem': 'População não encontrado'}), 404
    
    populacao.status_do_registro = False
    db.session.commit()

    return jsonify({"status": True, 'mensagem': 'População removida'}), HTTP_200_OK 


#area-umida
@remover.put('/area-umida/<id>')
def area_umida_remover(id):
    umida = AreaUmida.query.filter_by(id=id).first()
    

    if not umida:
        return jsonify({'status':False,'mensagem': 'Área Úmida não encontrado'}), 404
    
    umida.status_do_registro = False
    db.session.commit()

    return jsonify({"status": True, 'mensagem': 'Área Úmida removida'}), HTTP_200_OK 


#equipamentos
@remover.put('/equipamentos/<id>')
def equipamentos_remover(id):
    equipamento = Equipamentos.query.filter_by(id=id).first()
  

    if not equipamento:
        return jsonify({'status':False,'mensagem': 'Equipamento não encontrado'}), 404
    
    equipamento.status_do_registro = False
    db.session.commit()

    return jsonify({"status": True, 'mensagem': 'Equipamento removido'}), HTTP_200_OK 


#reservatorios
@remover.put('/reservatorios/<id>')
def reservatorio_remover(id):
    reservatorio = Reservatorios.query.filter_by(id=id).first()
  

    if not reservatorio:
        return jsonify({'status':False,'mensagem': 'Reservatório não encontrado'}), 404
    
    reservatorio.status_do_registro = False
    db.session.commit()

    return jsonify({"status": True, 'mensagem': 'Reservatório removido'}), HTTP_200_OK 


# EVENTOS
@remover.put('/tipo-evento/<id>')
def tipo_evento_remover(id):
    tipo_evento = TipoDeEventos.query.filter_by(id=id).first()

    if not tipo_evento:
        return jsonify({'status':False,'mensagem': 'Tipo de Evento não encontrado'}), 404
       
    tipo_evento.status_do_registro = False
    db.session.commit()

    return jsonify({"status": True, 'mensagem': 'Tipo de Evento removido'}), HTTP_200_OK 
    
    
    
@remover.put('/evento/<id>')
def evento_remover(id):
    evento = Eventos.query.filter_by(id=id).first()

    if not evento:
        return jsonify({'status':False,'mensagem': 'Evento não encontrado'}), 404
       
   
    evento.status_do_registro = False
    db.session.commit()

    return jsonify({"status": True, 'mensagem': 'Evento removido'}), HTTP_200_OK 
  