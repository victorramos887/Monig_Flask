from sqlalchemy import func, extract
from ..models import ConsumoAgua, EscolaNiveis, db, AuxOpNiveis
from flask import Blueprint, json, jsonify
from datetime import datetime
from flasgger import swag_from

dashboard = Blueprint('dashboard', __name__,
                          url_prefix='/api/v1/dashboard')


#Media de consumo de todas as escolas 
@swag_from('../docs/get/media_consumo_escolas.yaml')
@dashboard.get('/media-consumo')
def consumo_media():
    
    consulta = db.session.query(
        func.avg(ConsumoAgua.consumo).label('media_escola'),
        extract('month', ConsumoAgua.data).label('mes'),
        extract('year', ConsumoAgua.data).label('ano')
    )

    # Agrupar os resultados por ano e mês
    consulta = consulta.group_by('mes','ano')
    
     # Ordenar os resultados
    consulta = consulta.order_by('mes', 'ano')
    resultados = consulta.all()
    print(resultados)

    return jsonify({
        "data": [
            {"gastosEscola": round(l[0], 2), "mes_ano": (str(l[1]) + '-' + str(l[2]))} for l in resultados
        ],
        "status": True
    }), 200
        
        
# select 
# 	avg(c.consumo) as media_consumo,
# 	o.nivel as nivel
# from main.consumo_agua c 
# 		inner join main.escolas e on(e.id=c.fk_escola)
# 		inner join main.escola_niveis n on (n.escola_id=c.fk_escola)
# 		inner join main.aux_opniveis o on (n.nivel_ensino_id=o.id)
# group by o.nivel; - ok

#media de consumo por niveis de todas as escolas			
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

    
#Media de consumo por pessoa das escolas 
    
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

# --- media de consumo por pessoa nas escolas -- problema -- calcula toda a populacao da escola - independente de ter ou não registro de consumo
# SELECT
# 	e.fk_escola,
# 	c.consumo_total,
# 	e.total_pessoas_escola,
# 	ROUND(c.consumo_total / CAST(e.total_pessoas_escola AS DECIMAL(18, 2)), 3) as media_consumo_por_pessoa
# FROM
# 	(
# 		SELECT
# 			e.fk_escola,
# 			sum(p.alunos) as total_de_alunos,
# 			sum(p.funcionarios) as total_de_funcionarios,
# 			sum(p.funcionarios + p.alunos) as total_pessoas_escola
# 		FROM main.edificios e
# 		INNER JOIN main.populacao p
# 		ON (e.id = p.fk_edificios)
# 		GROUP BY e.fk_escola
# 	) e
# INNER JOIN
# 	(
# 		SELECT
# 			fk_escola as escola,
# 			sum(consumo) as consumo_total
# 		FROM main.consumo_agua
# 		GROUP BY fk_escola
# 	) c
# ON (e.fk_escola = c.escola);