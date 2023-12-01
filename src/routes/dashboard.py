from sqlalchemy import func
from ..models import ConsumoAgua,EscolaNiveis,db
from flask import Blueprint, json, jsonify


dashboard = Blueprint('dashboard', __name__,
                          url_prefix='/api/v1/dashboard')

@dashboard.get('/media-consumo')
def consumo_media():
    
    # Selecione as colunas desejadas
    consulta = db.session.query(ConsumoAgua.fk_escola, ConsumoAgua.consumo, ConsumoAgua.data)

    # Agrupe os resultados por mês e ano e calcule a média de consumo para cada grupo
    consulta = consulta.with_entities(func.to_char(ConsumoAgua.data, 'MM/YYYY').label('mes_ano'), func.avg(ConsumoAgua.consumo).label('media_escola')).group_by('mes_ano')

    # Execute a consulta e retorne os resultados em formato JSON
    resultados = consulta.all()
    return jsonify({
            "data": [
            {"mes_ano": l[0], "gastosEscola": round(l[1], 2)} for l in resultados
            ],
            "status": True
        }), 200
    
    
    
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