from flask import Blueprint, json, jsonify, request, render_template, flash, render_template_string
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_506_VARIANT_ALSO_NEGOTIATES, HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED
from ..models import Escolas, EscolaNiveis, Edificios, Reservatorios, db, AreaUmida, Equipamentos, Populacao, Hidrometros, Historico
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
    
    edificios =  Edificios.query.filter_by(fk_escola=id).all()
    if edificios:
        for edificio in edificios:
            edificio_json = edificio.to_json()
            edificio_json['data_criacao'] = edificio_json['data_criacao'].strftime('%m/%d/%Y %H:%M:%S')
            edificio_historico = Historico(tabela='Edificio', dados=edificio_json)
            db.session.add(edificio_historico)

            # area_umidas =  AreaUmida.query.filter_by(fk_edificios=id).all()
            # if area_umidas:
            #     for area_umida in area_umidas:
            #         area_umida_historico = Historico(tabela='Area_Umida', dados=json.dumps(area_umida.to_json()))
            #         equipamentos = Equipamentos.query.filter_by(fk_area_umida=area_umida.id).all()
            #         if equipamentos:
            #             for equipamento in equipamentos:
            #                 equipamento_historico = Historico(tabela='Equipamento', dados=json.dumps(equipamento.to_json()))
            #                 db.session.add(equipamento_historico)
            #                 db.session.delete(equipamento)
            # db.session.delete(area_umida)
            # db.session.add(area_umida_historico)

    # reservatorios = Reservatorios.query.filter_by(fk_escola=id).all()
    # if reservatorios:
    #     for reservatorio in reservatorios:
    #         reservatorio_historico = Historico(tabela='reservatorio', dados=json.dumps(reservatorio.to_json()))
    #         db.session.add(reservatorio_historico)
    #         db.session.delete(reservatorio)
    
    
    EscolaNiveis.query.filter_by(escola_id=id).delete()
     
    escola.status_do_registro = False
    escola_json = escola.to_json()
    escola_json['data_criacao'] = escola_json['data_criacao'].strftime('%m/%d/%Y %H:%M:%S')
    escola_historico = Historico(tabela='Escola', dados=escola_json)
    db.session.add(escola_historico)
    db.session.delete(escola)
    db.session.commit()

    return jsonify({"status": True, 'mensagem': 'Escola removida'}), HTTP_200_OK 

 
    
#edificios
@remover.put('/edificios/<id>')
def edificios_remover(id):
    edificio = Edificios.query.filter_by(id=id).first()
  
    if not edificio:
        return jsonify({'status':False,'mensagem': 'Edificio não encontrado'}), 404 

    edificio.status_do_registro = False

       # Insere os dados da linha excluída na tabela de histórico
    historico = Historico(tabela='Edificios', dados=json.dumps(edificio.to_json()))
    db.session.add(historico)

    
    db.session.commit()

    return jsonify({"status": True, 'mensagem': 'Edificio removido'}), HTTP_200_OK 


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
