from sqlalchemy import func, extract
from ..models import db, ConsumoAgua, EscolaNiveis, Escolas, AuxOpNiveis, Edificios, Populacao
from flask import Blueprint, json, jsonify
from datetime import datetime
from flasgger import swag_from 



dashboard = Blueprint('dashboard', __name__,
                          url_prefix='/api/v1/dashboard')


#Media de consumo das escolas - mes a mes
@swag_from('../docs/get/dashboard/media_consumo_escolas.yaml')
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
 
 
 
 #Media de consumo de uma escola mês a mês -- Verificar resultado
@swag_from('../docs/get/dashboard/media_consumo_escola.yaml')
@dashboard.get('/media-consumo-escola/<int:id>')
def consumo_media_escola(id):
    
    consumo_escola = ConsumoAgua.query.filter_by(fk_escola=id).first()
    
    if not consumo_escola:
        return jsonify({
            "status": False,
            "mensagem": "Não há registro de consumo para a escola indicada."
        }), 404
        
    consulta = db.session.query(
        func.avg(ConsumoAgua.consumo).label('media_ConsumoAgua'),
        extract('month', ConsumoAgua.data).label('mes'),
        extract('year', ConsumoAgua.data).label('ano')
    ).filter(ConsumoAgua.fk_escola==id)

    # Agrupar os resultados por ano e mês
    consulta = consulta.group_by('mes','ano')

    # Ordenar os resultados
    consulta = consulta.order_by('mes', 'ano')
    resultados = consulta.all()

    return jsonify({
        "data": [
            {
                "gastosEscola": round(l[0], 2),
                "mes_ano": (str(l[1]) + '-' + str(l[2]))
            } for l in resultados
        ],
        "status": True
    }), 200


 
 
#Media de consumo por pessoa de cada escola - mês a mês
@swag_from('../docs/get/dashboard/media_consumo_pessoas.yaml')
@dashboard.get('/media-consumo-pessoas')
def media_consumo_pessoas():

    populacao_escola = db.session.query(
        Edificios.fk_escola,
        func.sum(Populacao.alunos).label('total_alunos'),
        func.sum(Populacao.funcionarios).label('total_funcionarios'),
        func.sum(Populacao.alunos + Populacao.funcionarios).label('total_populacao')
    ).filter(Edificios.id == Populacao.fk_edificios).group_by(Edificios.fk_escola).subquery()

    consumo_escola = db.session.query(
        ConsumoAgua.fk_escola,
        func.sum(ConsumoAgua.consumo).label('consumo'),
        extract("year", ConsumoAgua.data).label('ano'),
        extract("month", ConsumoAgua.data).label('mes')
    ).group_by(ConsumoAgua.fk_escola, extract("year", ConsumoAgua.data), extract("month", ConsumoAgua.data)).subquery()

    juncao = db.session.query(
        populacao_escola.c.fk_escola,
        populacao_escola.c.total_alunos,
        populacao_escola.c.total_funcionarios,
        (populacao_escola.c.total_alunos + populacao_escola.c.total_funcionarios).label('total_pessoas'),
        consumo_escola.c.consumo,
        func.concat(consumo_escola.c.mes, "-" , consumo_escola.c.ano).label('mes_ano'),
        (consumo_escola.c.consumo / (populacao_escola.c.total_alunos + populacao_escola.c.total_funcionarios)).label('media_consumo')
    ).join(consumo_escola, populacao_escola.c.fk_escola == consumo_escola.c.fk_escola).subquery()

    resultados = db.session.query(
        juncao.c.fk_escola,
        juncao.c.total_alunos,
        juncao.c.total_funcionarios,
        juncao.c.total_pessoas,
        juncao.c.consumo,
        juncao.c.mes_ano,
        juncao.c.media_consumo
    ).order_by(juncao.c.fk_escola, juncao.c.mes_ano).all()
     
    resultados_json = [
        {
            "escola": l[0],
            "alunos": l[1],
            "funcionarios": l[2],
            "populacao_total": l[3],
            "consumo": l[4],
            "mes_ano": l[5],
            "media_consumo": round(l[6], 2)
        } for l in resultados
    ]

    return jsonify({
        "data": resultados_json,
        "status": True
}), 200
    



#Media de consumo por nivel das escolas -- problema ao dividir p nivel
@swag_from('../docs/get/dashboard/media_consumo_niveis.yaml')
@dashboard.get('/media-consumo-niveis')   
def consumo_media_niveis():
    consulta = (
        db.session.query(
            AuxOpNiveis.nivel,
            func.avg(ConsumoAgua.consumo).label('Media De Consumo')
         ) 
        .join(Escolas, Escolas.id == ConsumoAgua.fk_escola) 
        .join(EscolaNiveis, EscolaNiveis.escola_id == ConsumoAgua.fk_escola) 
        .join(AuxOpNiveis, AuxOpNiveis.id == EscolaNiveis.nivel_ensino_id) 
        .group_by(AuxOpNiveis.nivel)
        .all()
    )
    
    return jsonify({
        "data": [
            {
                "Nivel": l[0],
                "Media de Consumo": round(l[1], 2)
                
            } for l in consulta
        ],
    })

    
#Media de consumo das escola    
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





