from flask import Blueprint, jsonify, request, render_template
from flask_mail import Message
from flasgger import swag_from
from apscheduler.schedulers.background import BackgroundScheduler
from src.__init__ import mail, app
from datetime import datetime, date
from ..models import Escolas, Monitoramento, db, Eventos, AuxTipoDeEventos
from dateutil.relativedelta import relativedelta
from sqlalchemy import or_
from sqlalchemy.orm import aliased


email = Blueprint("email", __name__, url_prefix = '/api/v1/email')


#Enviar email Monitoramento -OK
# @swag_from('../docs/email.yaml')
@email.post("/monitoramento")
def monitoramento():
        with app.app_context():
        
                #percorre apenas escolas com registro - id das escolas
                escolas = Monitoramento.query.with_entities(Monitoramento.fk_escola).distinct().all() 
                
                for i in escolas:
                        fk_escola = i.fk_escola
                        print(fk_escola)
                
                        #pegar todos os registros desse fk
                        registros = Monitoramento.query.filter_by(fk_escola=fk_escola).all() 
                        
                        # Pegar a última data registrada
                        registro_recente = max(r.datahora for r in registros).date()
                        print(registro_recente)
                        
                        # Pegar a data atual
                        hoje = datetime.now().date()

                        # diferença de dias
                        intervalo = (hoje - registro_recente).days
                        
                        if intervalo > 10:
                                info_escola = Escolas.query.filter_by(id=fk_escola).first()
                                
                                #email para escola
                                msg = Message('Teste email monitoramento', sender = 'monitoramento_escola@gmail.com', recipients = [info_escola.email])
                                msg.body = "Alerta de monitoramento para a escola {}.\n Não registramos nenhum monitoramento nos últimos {} dias.".format(info_escola.nome, intervalo)
                                mail.send(msg)

                                print('EMAIL ENVIADO')  




# RETORNO TOLERÂNCIA
@email.post('/evento-aberto')
def evento_sem_encerramento():
        with app.app_context():
                
                # eventos_ocasional = Eventos.query.join(AuxTipoDeEventos).filter(
                #     AuxTipoDeEventos.recorrente.in_([False, None])).all()

                tipo_alias = aliased(AuxTipoDeEventos)
                
                # filtrando eventos ocasionais
                # Alterando junção
                eventos_ocasional = (
                        db.session.query(Eventos)
                        .join(tipo_alias, Eventos.fk_tipo == tipo_alias.id)
                        .filter(
                        or_(tipo_alias.recorrente == False, tipo_alias.recorrente == None)
                        )
                        .all()
                )

                # eventos sem data de encerramento
                eventos_sem_encerramento = [
                        evento for evento in eventos_ocasional if evento.data_encerramento is None]

                for evento in eventos_sem_encerramento:

                        # buscar o tipo do evento na tabela auxiliar e pegar tolerancia e unidade desse tipo
                        tipo = AuxTipoDeEventos.query.filter_by(id=evento.fk_tipo).first()

                        if tipo and tipo.tempo is not None:
                                unidade = tipo.unidade.lower() #Reduzindo a unidade para minúsculo
                                tempo = tipo.tempo
                                # comparar a unidade e realizar o calculo
                                if unidade == "meses":
                                        tolerancia = evento.datainicio + relativedelta(months=tempo)

                                elif unidade == "semanas":
                                        tolerancia = evento.datainicio + relativedelta(weeks=tempo)

                                elif unidade =="dias": 
                                        tolerancia = evento.datainicio + relativedelta(days=tempo)
                                else:
                                        tolerancia = None

                                # igualar as datas
                                tolerancia = tolerancia.date() if tolerancia is not None else None
                                data_atual = date.today()

                                if tolerancia < data_atual:
                                       
                                        #email para escola
                                        tolerancia = str(tolerancia).format("%d/%m/%Y") 
                                        inicio_evento = str().format("%d/%m/%Y") 
                                        print(evento.escola.nome)
                                        
                                        msg = Message('Teste evento fora de prazo', sender = 'monitoramento_escola@gmail.com', recipients = [evento.escola.email])
                                        corpo_msg = 'Você possui um ou mais evento fora do prazo de tolerância'
                                        msg.body = "Evento em aberto\n titulo do evento:{}.\n inicio do evento:{}. \n tolerância: {}. \n alerta: {}".format(evento.nome, evento.datainicio, tolerancia, corpo_msg )
                                        mail.send(msg)

                                        print('EMAIL ENVIADO') 
                                        
                                     

#Enviar email Monitoramento -OK
# @email.post("/monitoramento")
# def monitoramento():
#         with app.app_context():
#                 #percorrer escolas
#                 escolas = Escolas.query.all()
                
#                 for escola in escolas:
                
#                         #verificar se escola tem registro na tabela Monitoramento
#                         registros = Monitoramento.query.filter_by(fk_escola=escola.id).all()
                        
#                         if registros:
#                                 # Pegar a última data registrada
#                                 ultima_data_registrada = max(r.datahora for r in registros).date()
                                
#                                 # Pegar a data atual
#                                 hoje = datetime.now().date()

#                                 # diferença de dias
#                                 intervalo = (hoje - ultima_data_registrada).days
                                
#                                 if intervalo > 10:
                                        
#                                         #email para escola
#                                         msg = Message('Teste email monitoramento', sender = 'monitoramento_escola@gmail.com', recipients = [escola.email])
#                                         msg.body = "Alerta de monitoramento para a escola {}.\n Não registramos nenhum monitoramento nos últimos {} dias.".format(escola.nome, intervalo)
#                                         mail.send(msg)

#                                         print('EMAIL ENVIADO', escola.id)  
                        
#ativar só se necessário

scheduler = BackgroundScheduler()
#Enviar emails 
def schedule_jobs(scheduler, *functions):
             
        for func in functions:
                scheduler.add_job(func, 'cron', hour=17, minute=59, day_of_week='mon-fri')
        
schedule_jobs(scheduler, evento_sem_encerramento)
scheduler.start()

