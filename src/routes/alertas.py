from flask import Blueprint, jsonify
from ..constants.http_status_codes import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED)
from sqlalchemy import func, select, desc
from ..models import  AuxTipoDeEventos,Eventos
from datetime import timedelta, date
from dateutil.relativedelta import relativedelta


alertas = Blueprint('alertas', __name__,
                          url_prefix='/api/v1/alertas')

# RETORNO TOLERÂNCIA
@alertas.get('/evento-aberto')
def get_evento_sem_encerramento():
    # filtrando eventos ocasionais
    eventos_ocasional = Eventos.query.join(AuxTipoDeEventos).filter(
        AuxTipoDeEventos.recorrente == False).all()

    # eventos sem data de encerramento
    eventos_sem_encerramento = [
        evento for evento in eventos_ocasional if evento.data_encerramento is None]

    result = {
        "evento": []
    }

    for evento in eventos_sem_encerramento:

        # buscar o tipo do evento na tabela auxiliar e pegar tolerancia e unidade desse tipo
        tipo = AuxTipoDeEventos.query.filter_by(id=evento.fk_tipo).first()

        if tipo and tipo.tempo is not None:
            unidade = tipo.unidade
            tempo = tipo.tempo

            # comparar a unidade e realizar o calculo
            if unidade == "meses":
                tolerancia = evento.datainicio + relativedelta(months=tempo)

            elif unidade == "semanas":
                tolerancia = evento.datainicio + relativedelta(weeks=tempo)

            elif unidade == "dias":
                tolerancia = evento.datainicio + relativedelta(days=tempo)

            # igualar as datas
            tolerancia = tolerancia.date()
            data_atual = date.today()

            # comparar para retornar a mensagem
            if tolerancia > data_atual:
                mensagem = "Evento dentro do prazo"

            elif tolerancia == data_atual:
                mensagem = "Atenção"

            else:
                mensagem = "Evento fora do prazo de tolerância"

            # adicionar o evento ao resultado
            evento_json = {
                "id": evento.id,
                "title": evento.nome,
                "start": str(evento.datainicio).format("%d/%m/%Y"),
                "color": evento.tipodeevento.color,
                "recorrente": evento.tipodeevento.recorrente,
                "escola": evento.escola.nome,
                "requer ação": evento.tipodeevento.requer_acao,
                "tolerância": str(tolerancia).format("%d/%m/%Y"),
                "mensagem": mensagem
            }
            result["evento"].append(evento_json)

    return jsonify(result), 200