from flask import Blueprint, jsonify, request, render_template
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
from flasgger import swag_from

email = Blueprint("email", __name__, url_prefix = '/api/v1/email')
mail = Mail()

# Inicializando o scheduler
scheduler = BackgroundScheduler()
scheduler.start()

#Rota de test
@swag_from('../docs/email.yaml')
@email.post("/email")
def index():
        msg = Message('TESTE 2', sender = 'anaprferrari@gmail.com', recipients = ['paulocdferrari@gmail.com'])
        msg.body = "Olá Paulo, estamos enviado este email de teste"
        mail.send(msg)
        return "Message sent!"


#Rota enviar email para escola
@email.post("/escola_email")
def escola_email():
    return "None"


def minha_funcao():
    # with current_app.app_context():
    msg = Message("API TRIGGER", sender = "anaprferrari@gmail.com", recipients=['paulocdferrari@gmail.com'])
    msg.body = "Olá, este email foi enviado automaticamente todos os dias as 11:0"
    mail.send(msg)
    print("Evento acionado!")

# # Agendando a função para ser executada todos os dias às 12:00
# scheduler.add_job(minha_funcao, 'cron', hour=11, minute=53)