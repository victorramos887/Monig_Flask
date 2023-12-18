from sqlalchemy import func, extract
from ..models import db, ConsumoAgua, EscolaNiveis, Escolas, AuxOpNiveis, Edificios, Populacao
from flask import Blueprint, json, jsonify
from datetime import datetime
from flasgger import swag_from 



dashboard = Blueprint('dashboard', __name__,
                          url_prefix='/api/v1/dashboard')


#Media de consumo das escolas 
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
 
 
        
#Media por pessoa das escolas -- checar a saida
@swag_from('../docs/get/media_consumo_pessoas.yaml')
@dashboard.get('/media_consumo_pessoas')
def media_consumo_pessoas():

        query = (
            db.session.query(
                Edificios.fk_escola.label('escola'),
                extract('month', ConsumoAgua.data).label('mes'),
                extract('year', ConsumoAgua.data).label('ano'),
                func.sum(ConsumoAgua.consumo).label('consumo_total'),
                func.sum(Populacao.alunos).label('total_alunos'),
                func.sum(Populacao.funcionarios).label('total_funcionarios')
            )
            .join(Populacao, Edificios.id == Populacao.fk_edificios)
            .join(ConsumoAgua, Edificios.fk_escola == ConsumoAgua.fk_escola)
            .group_by(Edificios.fk_escola, 'mes', 'ano' )
        )

        # Retornar JSON
        return jsonify({
            'data': [{
                'escola': escola,
                'mes_ano': str(mes) + '-' + str(ano),
                'consumo_total': consumo_total,
                'total_alunos': total_alunos,
                'total_funcionarios': total_funcionarios,
                'total_pessoas': total_alunos + total_funcionarios,
                'consumo_pessoa': round(consumo_total / (total_alunos + total_funcionarios), 2)
            } for escola, mes, ano, consumo_total, total_alunos, total_funcionarios, in query]
        })




#Media de consumo por nivel das escolas -- problema ao dividir p nivel
@swag_from('../docs/get/media_consumo_niveis.yaml')
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





