from sqlalchemy import func, extract
from ..models import ConsumoAgua, EscolaNiveis, db, AuxOpNiveis
from flask import Blueprint, json, jsonify
from datetime import datetime

dashboard = Blueprint('dashboard', __name__,
                          url_prefix='/api/v1/dashboard')


#Media de consumo das escolas independente de nivel -OK
@dashboard.get('/media-consumo')
def consumo_media():
    
    consulta = db.session.query(
        func.avg(ConsumoAgua.consumo).label('media_escola'),
        extract('month', ConsumoAgua.data).label('mes'),
        extract('year', ConsumoAgua.data).label('ano')
    )

    # Agrupar os resultados por ano e mês
    consulta = consulta.group_by('mes','ano')

    resultados = consulta.all()
    print(resultados)

    return jsonify({
        "data": [
            {"gastosEscola": round(l[0], 2), "mes_ano": (str(l[1]) + '-' + str(l[2]))} for l in resultados
        ],
        "status": True
    }), 200
        
        
        
#verificar saida --- retorno de 13.0 repetido pra cada ensino - não faz sentido - dividir pela população para o nivel?
@dashboard.get('/media-consumo-niveis')
def consumo_media_niveis():

  
    # Selecionar colunas
    consulta = db.session.query(
        AuxOpNiveis.nivel,
        func.avg(ConsumoAgua.consumo).label('media_escola'),
        extract('month', ConsumoAgua.data).label('mes'),
        extract('year', ConsumoAgua.data).label('ano')
    ).join(EscolaNiveis, EscolaNiveis.nivel_ensino_id == AuxOpNiveis.id).join(ConsumoAgua, ConsumoAgua.fk_escola == EscolaNiveis.escola_id)

    # Agrupar colunas
    consulta = consulta.group_by(AuxOpNiveis.nivel, 'mes', 'ano')
    
    # Executar a consulta e retornar os resultados em formato JSON
    resultado = consulta.all()
    print(resultado)

    return jsonify({
        "data": [
            {"gastosNivel": l[0], "gastosEscola": round(l[1], 2), "mes_ano": (str(l[2]) + '-' + str(l[3]))} for l in resultado
        ],
    })

    
    
    
@dashboard.get('/media_consumo')
def consumo_escolas():
    data = [
        {
           "mes": "Jan",
           " gastosEscola": 4000,
            "gastosNivel": 2400,
        },
        {
           "mes": "Fev",
           " gastosEscola": 3000,
            "gastosNivel": 1398,
        },
        {
           "mes": "Mar",
           " gastosEscola": 2000,
            "gastosNivel": 9800,
        },
        {
           "mes": "Abr",
           " gastosEscola": 2780,
            "gastosNivel": 3908,
        },
        {
           "mes": "Mai",
           " gastosEscola": 1890,
            "gastosNivel": 4800,
        },
        {
           "mes": "Jun",
           " gastosEscola": 2390,
            "gastosNivel": 3800,
        },
        {
           "mes": "Jul",
           " gastosEscola": 3490,
            "gastosNivel": 4300,
        },
        {
           "mes": "Ago",
           " gastosEscola": 4200,
            "gastosNivel": 2000,
        },
        {
           "mes": "Set",
           " gastosEscola": 3100,
            "gastosNivel": 3000,
        },
        {
           "mes": "Out",
           " gastosEscola": 2500,
            "gastosNivel": 4200,
        },
        {
           "mes": "Nov",
           " gastosEscola": 2870,
            "gastosNivel": 1500,
        },
        {
           "mes": "Dez",
           " gastosEscola": 1980,
            "gastosNivel": 6000,
        }]
    return jsonify(data)