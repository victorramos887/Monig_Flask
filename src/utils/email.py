# from flask_mail import Message
# # from ..routes.email import mail
# # from flask import current_app
import sys
import os

# diretorio_atual = os.path.dirname(__file__)
# dois_niveis_acima = os.path.abspath(os.path.join(diretorio_atual, '..', '..'))


sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..')))


#from src import create_app
# from apscheduler.schedulers.background import BackgroundScheduler

# print("-- Path -- ", dois_niveis_acima)


import src
# # Inicializando o scheduler apenas no processo principal
# if __name__ == '__main__':
#     scheduler = BackgroundScheduler()
#     scheduler.start()

#     def minha_funcao():
#         with current_app.app_context():
#             msg = Message("API TRIGGER", sender="v.ramos587@gmail.com", recipients=['v.ramos58@hotmail.com'])
#             msg.body = "Olá, este email foi enviado automaticamente todos os dias às 11:29"
#             mail.send(msg)
#             print("Evento acionado!")

#     # Agendando a função para ser executada todos os dias às 11:29
#     scheduler.add_job(minha_funcao, 'cron', hour=11, minute=37)

#     current_app.run(debug=True)

# scheduler = BackgroundScheduler()
# scheduler.start()

def minha_funcao():

    return "Qualquer coisa"
    # with app.app_context():
    #     msg = Message("API TRIGGER", sender = "v.ramos587@gmail.com", recipients=['v.ramos58@hotmail.com'])
    #     msg.body = "Olá, este email foi enviado automaticamente todos os dias as 11:0"
    #     mail.send(msg)
    #     print("Evento acionado!")

minha_funcao()

# Agendando a função para ser executada todos os dias às 12:00


# def executa_rota():
#     with create_app.test_client() as client:
#         response = client.get('/api/v1/email/email')  # Substitua 'sua-rota' pela rota que você deseja executar
#         # Faça algo com a resposta, se necessário
#         return response.data

# executa_rota()


# scheduler.add_job(minha_funcao, 'cron', hour=11, minute=50)
