from flask import Blueprint, jsonify, request, render_template
from flask_mail import Mail, Message
from flasgger import swag_from
from src.__init__ import scheduler, mail


email = Blueprint("email", __name__, url_prefix = '/api/v1/email')


#Rota de test
@scheduler.scheduled_job('cron', hour='18', minute='09')
@swag_from('../docs/email.yaml')
@email.post("/email")
def index():
    
        msg = Message('TESTE 2', sender = 'anaprferrari@gmail.com', recipients = ['paulocdferrari@gmail.com'])
        msg.body = "Olá, esse email será enviado automáticamente todos os dias"
        mail.send(msg)
        
        print('ok')
        
        return "Message sent!" 
   


#Rota enviar email para escola
@email.post("/escola_email")
def escola_email():
    return "None"




