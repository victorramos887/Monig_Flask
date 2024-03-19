from flask import Blueprint, jsonify, request, render_template
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler

email = Blueprint("email", __name__, url_prefix = '/api/v1/email')
mail = Mail()

# Inicializando o scheduler
scheduler = BackgroundScheduler()
scheduler.start()

#Rota de test
@email.post("/email")
def value_email():
    msg = Message('API VICTOR', sender = 'v.ramos587@gmail.com', recipients = ['j.carolinosantos@gmail.com'])
    msg.body = "Olá Jaqueline Soares, estamos enviado este email de teste"
    mail.send(msg)
    return "Message sent!"


#Rota enviar email para escola
@email.post("/escola_email")
def escola_email():
    return "None"


def minha_funcao():
    # with current_app.app_context():
    msg = Message("API TRIGGER", sender = "v.ramos587@gmail.com", recipients=['v.ramos58@hotmail.com'])
    msg.body = "Olá, este email foi enviado automaticamente todos os dias as 11:0"
    mail.send(msg)

# # Agendando a função para ser executada todos os dias às 12:00
# scheduler.add_job(minha_funcao, 'cron', hour=11, minute=53)