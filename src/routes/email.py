from flask import Blueprint, jsonify, request, render_template
from flask_mail import Message
from flasgger import swag_from
from apscheduler.schedulers.background import BackgroundScheduler
from src.__init__ import mail, app
from datetime import datetime, date
from ..models import Escolas, Monitoramento, db


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
                scheduler.add_job(func, 'cron', hour=15, minute=46, day_of_week='mon-fri')
        
schedule_jobs(scheduler, monitoramento)
scheduler.start()



