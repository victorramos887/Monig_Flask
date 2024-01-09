from flask import Blueprint, jsonify, request, render_template
from flask_mail import Message
from flasgger import swag_from
from apscheduler.schedulers.background import BackgroundScheduler
from src.__init__ import mail, app
from datetime import datetime

email = Blueprint("email", __name__, url_prefix = '/api/v1/email')



@email.post("/email")
def index():
        with app.app_context():
                msg = Message('TESTE DATA E HORA', sender = 'xxxx@gmail.com', recipients = ['xxxx@gmail.com'])
                msg.body = "Olá, esse email será enviado automáticamente todos os dias"
                mail.send(msg)
                
                print('EMAIL ENVIADO')
                
         
scheduler = BackgroundScheduler()

#Enviar emails 
def schedule_jobs(scheduler, *functions):
    for func in functions:
        scheduler.add_job(func, 'cron', hour=12, minute=24, day_of_week='mon-fri')
        
schedule_jobs(scheduler, index)
scheduler.start()
     






