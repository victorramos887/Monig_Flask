from flask import Blueprint, json, jsonify, request, render_template, flash, render_template_string
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_506_VARIANT_ALSO_NEGOTIATES, HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED
from ..models import Escolas, Edificios, Reservatorios, db, AreaUmida, Equipamentos, Populacao, Hidrometros, Historico
from sqlalchemy import exc, text

remover = Blueprint('remover', __name__, url_prefix='/api/v1/remover')

#EDITAR ESCOLA
@remover.put('/escolas/<id>')
def escolas_remover(id):
    escola = Escolas.query.filter_by(id=id).first()

    if not escola:
        return jsonify({'status':False,'mensagem': 'Escola não encontrado'}), 404
    
    #alterar status da linha para False
    escola.status_do_registro = False

     # Insere os dados da linha excluída na tabela de histórico
    historico = Historico(tabela='Escolas', dados=json.dumps(escola.to_json()))
    db.session.add(historico)


    # Confirma as alterações no banco de dados
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
