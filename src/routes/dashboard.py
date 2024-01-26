from sqlalchemy import func, extract, select
from ..models import db, ConsumoAgua, EscolaNiveis, Escolas, AuxOpNiveis, Edificios, Populacao
from flask import Blueprint, json, jsonify, request
from datetime import datetime
from flasgger import swag_from


dashboard = Blueprint('dashboard', __name__,
                      url_prefix='/api/v1/dashboard')


# Media de consumo das escolas - mes a mes
@swag_from('../docs/get/dashboard/media_consumo_escolas.yaml')
@dashboard.get('/media-consumo')
def consumo_media():

    consulta = db.session.query(
        func.avg(ConsumoAgua.consumo).label('media_escola'),
        extract('month', ConsumoAgua.data).label('mes'),
        extract('year', ConsumoAgua.data).label('ano')
    )

    # Agrupar os resultados por ano e mês
    consulta = consulta.group_by('mes', 'ano')

    # Ordenar os resultados
    consulta = consulta.order_by('mes', 'ano')
    resultados = consulta.all()

    return jsonify({
        "data": [
            {"gastosEscola": round(l[0], 3), "mes_ano": (str(l[1]) + '-' + str(l[2]))} for l in resultados
        ],
        "status": True
    }), 200

 # Media de consumo de uma escola mês a mês


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
    ).filter(ConsumoAgua.fk_escola == id)

    # Agrupar os resultados por ano e mês
    consulta = consulta.group_by('mes', 'ano')

    # Ordenar os resultados
    consulta = consulta.order_by('mes', 'ano')
    resultados = consulta.all()

    return jsonify({
        "data": [
            {
                "gastosEscola": round(l[0], 3),
                "mes_ano": (str(l[1]) + '-' + str(l[2]))
            } for l in resultados
        ],
        "status": True
    }), 200


# Media de consumo por pessoa de cada escola - mês a mês
@swag_from('../docs/get/dashboard/media_consumo_pessoas.yaml')
@dashboard.get('/media-consumo-pessoas')
def media_consumo_pessoas():

    populacao_escola = db.session.query(
        Edificios.fk_escola,
        func.sum(Populacao.alunos).label('total_alunos'),
        func.sum(Populacao.funcionarios).label('total_funcionarios'),
        func.sum(Populacao.alunos +
                 Populacao.funcionarios).label('total_populacao')
    ).filter(Edificios.id == Populacao.fk_edificios).group_by(Edificios.fk_escola).subquery()

    consumo_escola = db.session.query(
        ConsumoAgua.fk_escola,
        func.sum(ConsumoAgua.consumo).label('consumo'),
        extract("year", ConsumoAgua.data).label('ano'),
        extract("month", ConsumoAgua.data).label('mes')
    ).group_by(ConsumoAgua.fk_escola, extract("year", ConsumoAgua.data), extract("month", ConsumoAgua.data)).subquery()

    # juncao = db.session.query(
    #     populacao_escola.c.fk_escola,
    #     populacao_escola.c.total_alunos,
    #     populacao_escola.c.total_funcionarios,
    #     (populacao_escola.c.total_alunos + populacao_escola.c.total_funcionarios).label('total_pessoas'),
    #     consumo_escola.c.consumo,
    #     func.concat(consumo_escola.c.mes, "-" , consumo_escola.c.ano).label('mes_ano'),
    #     (consumo_escola.c.consumo / (populacao_escola.c.total_alunos + populacao_escola.c.total_funcionarios)).label('media_consumo')
    # ).join(consumo_escola, populacao_escola.c.fk_escola == consumo_escola.c.fk_escola).subquery()

    juncao = db.session.query(
        populacao_escola.c.fk_escola,
        populacao_escola.c.total_alunos,
        populacao_escola.c.total_funcionarios,
        populacao_escola.c.total_alunos.label('total_pessoas'),
        consumo_escola.c.consumo,
        func.concat(consumo_escola.c.mes, "-",
                    consumo_escola.c.ano).label('mes_ano'),
        (consumo_escola.c.consumo /
         populacao_escola.c.total_alunos).label('media_consumo')
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
            "media_consumo": round(l[6], 3)
        } for l in resultados
    ]

    return jsonify({
        "data": resultados_json,
        "status": True
    }), 200


# Media de consumo por pessoa de uma escola - mês a mês
@swag_from('../docs/get/dashboard/media_consumo_pessoas_escola.yaml')
@dashboard.get('/media-consumo-pessoas-escola/<int:id>')
def media_consumo_pessoas_esc(id):

    consumo_escola = ConsumoAgua.query.filter_by(fk_escola=id).first()

    if not consumo_escola:
        return jsonify({
            "status": False,
            "mensagem": "Não há registro de consumo para a escola indicada."
        }), 404

    populacao_escola = db.session.query(
        Edificios.fk_escola,
        func.sum(Populacao.alunos).label('total_alunos'),
        func.sum(Populacao.funcionarios).label('total_funcionarios'),
        func.sum(Populacao.alunos +
                 Populacao.funcionarios).label('total_populacao')
    ).filter(Edificios.id == Populacao.fk_edificios).filter(Edificios.fk_escola == id).group_by(Edificios.fk_escola).subquery()

    consumo_escola = db.session.query(
        ConsumoAgua.fk_escola,
        func.sum(ConsumoAgua.consumo).label('consumo'),
        extract("year", ConsumoAgua.data).label('ano'),
        extract("month", ConsumoAgua.data).label('mes')
    ).filter(ConsumoAgua.fk_escola == id).group_by(ConsumoAgua.fk_escola, extract("year", ConsumoAgua.data), extract("month", ConsumoAgua.data)).subquery()

    juncao = db.session.query(
        populacao_escola.c.fk_escola,
        populacao_escola.c.total_alunos,
        populacao_escola.c.total_funcionarios,
        (populacao_escola.c.total_alunos +
         populacao_escola.c.total_funcionarios).label('total_pessoas'),
        consumo_escola.c.consumo,
        func.concat(consumo_escola.c.mes, "-",
                    consumo_escola.c.ano).label('mes_ano'),
        (consumo_escola.c.consumo / (populacao_escola.c.total_alunos +
         populacao_escola.c.total_funcionarios)).label('media_consumo')
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
            "media_consumo": round(l[6], 3)
        } for l in resultados
    ]

    return jsonify({
        "data": resultados_json,
        "status": True
    }), 200


# #Media de consumo por pessoa de todas as escola - mês a mês
# @swag_from('../docs/get/dashboard/consumo_pessoas_escolas.yaml')
# @dashboard.get('/consumo-pessoas-escolas/')
# def consumo_pessoas_esc():

#     consumo_escola = db.session.query(
#         ConsumoAgua.fk_escola,
#         func.sum(ConsumoAgua.consumo).label("consumo"),
#         extract("month", ConsumoAgua.data).label('mes'),
#         extract("year", ConsumoAgua.data).label('ano'),
#     ).group_by(ConsumoAgua.fk_escola,  extract("month", ConsumoAgua.data), extract("year", ConsumoAgua.data)).subquery()

#     populacao_escola = db.session.query(
#         Edificios.fk_escola,
#         func.sum(Populacao.alunos + Populacao.funcionarios).label("populacao")
#     ).filter(Edificios.id == Populacao.fk_edificios).group_by(Edificios.fk_escola).subquery()

#     juncao = db.session.query(
#         func.sum(consumo_escola.c.consumo).label('consumo_total'),
#         func.sum(populacao_escola.c.populacao).label('populacao_total'),
#         (func.sum(consumo_escola.c.consumo) / (func.sum(populacao_escola.c.populacao))).label("media_consumo"),
#         func.concat(consumo_escola.c.mes,"-", consumo_escola.c.ano).label('mes_ano')
#     ).join(consumo_escola, consumo_escola.c.fk_escola ==  populacao_escola.c.fk_escola).group_by('mes_ano').subquery()

#     print(juncao)

#     resultados = db.session.query(
#         juncao.c.consumo_total,
#         juncao.c.populacao_total,
#         juncao.c.media_consumo,
#         juncao.c.mes_ano
#     ).all()

#     resultados_json = [
#         {
#             "consumo_total": l[0],
#             "populacao_total": l[1],
#             "media_consumo": round(l[2], 3),
#             "mes_ano": l[3]
#         } for l in resultados
#     ]

#     return jsonify({
#         "data": resultados_json,
#         "status": True
#     }), 200


# Media de consumo por nivel das escolas -- problema ao dividir p nivel
# @swag_from('../docs/get/dashboard/media_consumo_niveis.yaml')
# @dashboard.get('/media-consumo-niveis')
# def consumo_media_niveis():
#     consulta = (
#         db.session.query(
#             AuxOpNiveis.nivel,
#             func.avg(ConsumoAgua.consumo).label('Media De Consumo')
#          )
#         .join(Escolas, Escolas.id == ConsumoAgua.fk_escola)
#         .join(EscolaNiveis, EscolaNiveis.escola_id == ConsumoAgua.fk_escola)
#         .join(AuxOpNiveis, AuxOpNiveis.id == EscolaNiveis.nivel_ensino_id)
#         .group_by(AuxOpNiveis.nivel)
#         .all()
#     )

#     return jsonify({
#         "data": [
#             {
#                 "Nivel": l[0],
#                 "Media de Consumo": round(l[1], 2)

#             } for l in consulta
#         ],
#     })

meses_em_portugues = {
    1: "Jan",
    2: "Fev",
    3: "Mar",
    4: "Abr",
    5: "Mai",
    6: "Jun",
    7: "Jul",
    8: "Ago",
    9: "Set",
    10: "Out",
    11: "Nov",
    12: "Dez"
}

def obter_nome_mes(numero_mes):
    return meses_em_portugues.get(numero_mes, str(numero_mes))


@dashboard.get('/grafico-media-consumo-mensal-todas-escolas')
def grafico_media_consumo_mensal_todas_escolas():

    try:
        niveis = request.args['niveis']
    except:
        niveis = None

    if niveis is not None:
        print("Verificando o recebimento: ", niveis)
        lista = niveis.split(',')
        # Crie uma condição usando SQLAlchemy
        query = AuxOpNiveis.query.filter(AuxOpNiveis.nivel.in_(lista)).all()
        # Use a condição em uma consulta SQL

        listaid = [q.id for q in query]

        #escolas_all = EscolaNiveis.query.all()
        #print("Todas as Escolas: ", [escola_.escola_id for escola_ in escolas_all])

        # Filtrar por nível
        query = Escolas.query.join(
            EscolaNiveis, Escolas.id == EscolaNiveis.escola_id)
        query = query.filter(EscolaNiveis.nivel_ensino_id.in_(listaid))
        escolas_id = [q.id for q in query]


        consulta = db.session.query(
            func.avg(ConsumoAgua.consumo).label('media_escola'),
            extract('month', ConsumoAgua.data).label('mes'),
            extract('year', ConsumoAgua.data).label('ano')
        )

        # Agrupar os resultados por ano e mês
        consulta = consulta.group_by('mes', 'ano')
        # Ordenar os resultados 
        consulta = consulta.order_by('mes', 'ano')
        resultados = consulta.all()

        resultados_nivel = db.session.query(
            func.sum(ConsumoAgua.consumo).label('media_escola'),
            extract('month', ConsumoAgua.data).label('mes'),
            extract('year', ConsumoAgua.data).label('ano')
        ).where(ConsumoAgua.fk_escola.in_(escolas_id))

        resultados_nivel = resultados_nivel.group_by('mes', 'ano').all()     

        # consumoaguaniveis = ConsumoAgua.query.filter(ConsumoAgua.fk_escola.in_(escolas_id)).all()
        # print([l.consumo for l in consumoaguaniveis])
        # consulta_nivel = db.session.query(
        #     func.avg(consumoaguaniveis.consumo).label('media_escola'),
        #     extract('month', ConsumoAgua.data).label('mes'),
        #     extract('year', ConsumoAgua.data).label('ano')
        # ).filter(ConsumoAgua.fk_escola.in_(escolas_id))

        # # Agrupar os resultados por ano e mês
        # resultados_nivel = consulta_nivel.group_by('mes', 'ano')
        # # # Ordenar os resultados
        # resultados_nivel = consulta_nivel.order_by('mes', 'ano')
        # resultados_nivel = consulta_nivel.all()
        lista_resultado = []

        index_nivel = 0

        for resultado in resultados:
            if index_nivel < len(resultados_nivel):
                resultado_nivel = resultados_nivel[index_nivel]
                # Adiciona o resultado atual de 'resultados' ao resultado final
                mes_ano = f"{obter_nome_mes(resultado[1])}-{resultado[2]}"
                lista_resultado.append({
                    "mes": mes_ano,
                    "gastosEscola": round(resultado[0], 3),
                    "gastosNivel": round(resultado_nivel[0], 3)
                })

                # Avança para o próximo resultado_nivel se estivermos na mesma mes/ano
                while (
                    index_nivel < len(resultados_nivel) and
                    resultado.mes == resultado_nivel.mes and
                    resultado.ano == resultado_nivel.ano
                ):
                    index_nivel += 1
                    if index_nivel < len(resultados_nivel):
                        resultado_nivel = resultados_nivel[index_nivel]

            else:
                # Adiciona o resultado atual de 'resultados' ao resultado final sem correspondência
                mes_ano = f"{obter_nome_mes(resultado[1])}-{resultado[2]}"
                lista_resultado.append({
                    "mes": mes_ano,
                    "gastosEscola": round(resultado[0], 3),
                    "gastosNivel": None,
                })

        if len(lista_resultado) > 0:

            return jsonify({
                "data": lista_resultado,
                "status": True
            }), 200
        
        else:
            consulta = db.session.query(
                func.avg(ConsumoAgua.consumo).label('media_escola'),
                extract('month', ConsumoAgua.data).label('mes'),
                extract('year', ConsumoAgua.data).label('ano')
            )

            # Agrupar os resultados por ano e mês
            consulta = consulta.group_by('mes', 'ano')

            # # Ordenar os resultados
            resultados = consulta.all()       

            lista_ordenada = sorted(resultados, key=lambda x: (int(x[2]), int(x[1])))

            return jsonify({
                "data": [
                    {"gastosEscola": round(l[0], 3), "mes": f"{obter_nome_mes(l[1])}-{l[2]}", "gastosNivel":""} for l in resultados
                ],
                "status": True
            }), 200
        
    else:
            consulta = db.session.query(
                func.avg(ConsumoAgua.consumo).label('media_escola'),
                extract('month', ConsumoAgua.data).label('mes'),
                extract('year', ConsumoAgua.data).label('ano')
            )

            # Agrupar os resultados por ano e mês
            consulta = consulta.group_by('mes', 'ano')

            # # Ordenar os resultados
            resultados = consulta.all()       

            lista_ordenada = sorted(resultados, key=lambda x: (int(x[2]), int(x[1])))
            print("Lista ordenada: ", lista_ordenada)

            return jsonify({
                "data": [
                    {"gastosEscola": round(l[0], 3), "mes": f"{obter_nome_mes(l[1])}-{l[2]}", "gastosNivel":""} for l in resultados
                ],
                "status": True
            }), 200

@dashboard.get('/cad-principal')
def cad_principal():

    # Total de Alunos
    # Total de População
    populacao = db.session.query(
                func.sum(Populacao.alunos).label('alunos'),
                func.sum(Populacao.funcionarios).label('funcionarios')
            ).all()

    # Consumo total

    consumo = db.session.query(
        func.sum(ConsumoAgua.consumo).label('soma_consumo')
    ).all()

    populacao = {"Alunos":populacao[0][0], "Funcionarios":populacao[0][1]}
    consumo = {"Consumo":consumo[0][0]}


    return jsonify({
        "data": [populacao, consumo]
    })




# Media de consumo das escola
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