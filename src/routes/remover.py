from flask import Blueprint, json, jsonify, request, render_template, flash, render_template_string
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_506_VARIANT_ALSO_NEGOTIATES, HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED
from ..models import Escolas, EscolaNiveis, TipoDeEventos, Eventos, Edificios, Reservatorios, db, AreaUmida, Equipamentos, Populacao, Hidrometros, Historico
from sqlalchemy import exc, text, select

remover = Blueprint('remover', __name__, url_prefix='/api/v1/remover')


#testar rota para reverter 
@remover.get('/restaurar-escola/<id>')
def reverter_escola(id):
    escola = db.session.query(Escolas).filter_by(id=id).all()
    if escola and escola.prev():
        escola.prev().revert()
        db.session.commit() # salva as mudanças no banco de dados
        return jsonify({"status": True, 'mensagem': 'Escola restaurada'}), HTTP_200_OK 
    

# @remover.get('/retornar-historico')
# def get_historico():

#     historicos = [historia.to_json() for historia in Historico.query.all()]

#     return jsonify(historicos)
    

#EDITAR ESCOLA
@remover.put('/escolas/<id>')
def escolas_remover(id):

    try: 

        escola = Escolas.query.filter_by(id=id).first()
        if not escola:
            return jsonify({'status':False,'mensagem': 'Escola não encontrado'}), 404
        
        niveis = EscolaNiveis.query.filter_by(escola_id=id).all()
        if niveis:
            for nivel in niveis:
                db.session.delete(nivel)

        edificios =  Edificios.query.filter_by(fk_escola=id).all()
        if edificios:
            for edificio in edificios:

                area_umidas =  AreaUmida.query.filter_by(fk_edificios=id).all()
                if area_umidas:
                    for area_umida in area_umidas:
                    
                        equipamentos = Equipamentos.query.filter_by(fk_area_umida=area_umida.id)
                        if equipamentos:
                            for equipamento in equipamentos:
                                equipamento.status_do_registro = False
                                #db.session.delete(equipamento)

                    area_umida.status_do_registro = False
                    #db.session.delete(area_umida)
            

                hidrometros = Hidrometros.query.filter_by(fk_edificios=edificio.id)
                if hidrometros:
                    for hidrometro in hidrometros:
                        hidrometro.status_do_registro = False
                        #db.session.delete(hidrometro)
                
                populacao  = Populacao.query.filter_by(fk_edificios=edificio.id)
                if populacao :
                    for populacao_ in populacao :
                        populacao_.status_do_registro = False
                        #db.session.delete(populacao)

        edificio.status_do_registro = False
        #db.session.delete(edificio)

        reservatorios = Reservatorios.query.filter_by(fk_escola=id).all()
        if reservatorios:
            for reservatorio in reservatorios:
                reservatorio.status_do_registro = False
                #db.session.delete(reservatorio)
                
           
        escola.status_do_registro = False
        db.session.delete(escola)
        db.session.commit()
        return jsonify({"status": True, 'mensagem': 'Escola removida'}), HTTP_200_OK 

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status":False, 'mensagem':"Erro não tratado", "codigo":str(e)
        }), 400


 
    
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
    area_umida =  AreaUmida.query.filter_by(id=id).first()

    if not area_umida:
        return jsonify({'status':False,'mensagem': 'Área Úmida não encontrado'}), 404
    
    if area_umida:
            equipamentos = Equipamentos.query.filter_by(fk_area_umida=area_umida.id)
            if equipamentos:
                for equipamento in equipamentos:
                    equipamento.status_do_registro = False

    area_umida.status_do_registro = False
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

#tipo-evento
@remover.put('/tipo-evento/<id>')
def tipo_evento_remover(id):
    tipo_evento = TipoDeEventos.query.filter_by(id=id).first()
  
    if not tipo_evento:
        return jsonify({'status':False,'mensagem': 'Tipo de Evento não encontrado'}), 404
    
    tipo_evento.status_do_registro = False
    db.session.commit()

    return jsonify({"status": True, 'mensagem': 'Tipo de Evento removido'}), HTTP_200_OK 


#eventos
@remover.put('/evento/<id>')
def evento_remover(id):
    evento = Eventos.query.filter_by(id=id).first()
  
    if not evento:
        return jsonify({'status':False,'mensagem': 'Evento não encontrado'}), 404
    
    evento.status_do_registro = False
    db.session.commit()

    return jsonify({"status": True, 'mensagem': 'Evento removido'}), HTTP_200_OK 

