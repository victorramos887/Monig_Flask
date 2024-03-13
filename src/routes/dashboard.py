from sqlalchemy import func, extract, text, and_, desc
from sqlalchemy.sql.functions import concat
from ..models import db, ConsumoAgua, EscolaNiveis, Escolas, AuxOpNiveis, Edificios, Populacao
from flask import Blueprint, json, jsonify, request
from datetime import datetime, timedelta
from sqlalchemy.dialects.postgresql import INTERVAL
from dateutil import relativedelta
from flasgger import swag_from
import dateutil
from sqlalchemy.orm import aliased
from geoalchemy2.shape import to_shape

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
                "mes": (str(l[1]) + '-' + str(l[2]))
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

def converter_mes_ano(data_str):
    meses_abreviados = {
        "01": "Jan",
        "02": "Fev",
        "03": "Mar",
        "04": "Abr",
        "05": "Mai",
        "06": "Jun",
        "07": "Jul",
        "08": "Ago",
        "09": "Set",
        "10": "Out",
        "11": "Nov",
        "12": "Dez",
    }

    ano, mes = data_str.split("-")
    mes_abreviado = meses_abreviados[mes]
    return f"{mes_abreviado}-{ano}"


@dashboard.get('/grafico-media-consumo-mensal-todas-escolas')
def grafico_media_consumo_mensal_todas_escolas():
    try:
        niveis = request.args['niveis']
    except:
        niveis = None
    #LISTA COM INTERVALO DE DATAS
    #maior data e menor - intervalo
    data = db.session.query(
                    func.max(ConsumoAgua.data).label('maior_data'),
                    func.min(ConsumoAgua.data).label('menor_data')
                ).all()
    #pegar resultado da consulta
    data_maior = data[0][0]
    data_menor = data[0][1]
    lista_com_intervalo = []
    #alimentar a lista com intervalo de datas
    while data_menor <= data_maior:
        lista_com_intervalo.append(data_menor.strftime("%Y-%m"))
        prox_mes = (data_menor.month % 12) + 1
        if prox_mes == 1:
            data_menor = data_menor.replace(year=data_menor.year + 1, month=1)
        else:
            data_menor = data_menor.replace(month=prox_mes)
    # Adicione a maior data à lista
    lista_com_intervalo.append(data_maior.strftime("%Y-%m"))
    ###
    if niveis is not None:
        print("Verificando o recebimento: ", niveis)
        lista = niveis.capitalize().split(',')
        print("lista: ", lista)
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

        # consulta = db.session.query(
        #             func.avg(ConsumoAgua.consumo).label('media_escola'),
        #             func.concat(extract('year', ConsumoAgua.data),'-',  func.to_char(ConsumoAgua.data, 'MM')).label('ano_mes')
        #         ).group_by(extract('year', ConsumoAgua.data), func.to_char(ConsumoAgua.data, 'MM'))\
        #          .order_by(extract('year', ConsumoAgua.data), func.to_char(ConsumoAgua.data, 'MM'))\
        #          .all()
                 
        resultados_nivel = db.session.query(
            func.avg(ConsumoAgua.consumo).label('media_escola'),
            func.concat(extract('year', ConsumoAgua.data),'-',  func.to_char(ConsumoAgua.data, 'MM')).label('ano_mes')
            ).group_by(extract('year', ConsumoAgua.data), func.to_char(ConsumoAgua.data, 'MM'))\
            .order_by(extract('year', ConsumoAgua.data), func.to_char(ConsumoAgua.data, 'MM'))\
            .where(ConsumoAgua.fk_escola.in_(escolas_id))\
            .all()
        lista_resultado = []
        index_nivel = 0

        for resultado in resultados_nivel:

            # print("Consulta atual: ", consulta)
            if index_nivel < len(resultados_nivel):
                resultado_nivel = resultados_nivel[index_nivel]
                # Adiciona o resultado atual de 'resultados' ao resultado final

                print(type(round(resultado[0], 3)))
                lista_resultado.append({
                    "mes": converter_mes_ano(resultado[1]),
                    "gastosEscola": float(round(resultado[0], 3)),
                    "gastosNivel": round(resultado_nivel[0], 3)
                })

                print("Resultado Ano ", resultado)
                # Avança para o próximo resultado_nivel se estivermos na mesma mes/ano
                while (
                    index_nivel < len(resultados_nivel) and
                    resultado[1].split('-')[1] == resultado_nivel[1].split('-')[1] and
                    resultado[1].split('-')[0] == resultado_nivel[1].split('-')[0]
                ):
                    index_nivel += 1
                    if index_nivel < len(resultados_nivel):
                        resultado_nivel = resultados_nivel[index_nivel]
            else:
                # Adiciona o resultado atual de 'resultados' ao resultado final sem correspondência
                lista_resultado.append({
                    "mes": converter_mes_ano(resultado[1]),
                    "gastosEscola": float(round(resultado[0], 3)),
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
                    func.concat(extract('year', ConsumoAgua.data),'-',  func.to_char(ConsumoAgua.data, 'MM')).label('ano_mes')
                ).group_by(extract('year', ConsumoAgua.data), func.to_char(ConsumoAgua.data, 'MM'))\
                 .order_by(extract('year', ConsumoAgua.data), func.to_char(ConsumoAgua.data, 'MM'))\
                 .all()
            return jsonify({
                "data": [
                    {"gastosEscola": round(l[0], 3), "mes": l[1], "gastosNivel":""} for l in consulta
                ],
                "status": True
            }), 200
     #FUNCIONANDO
    else:
            consulta = db.session.query(
                    func.avg(ConsumoAgua.consumo).label('media_escola'),
                    func.concat(extract('year', ConsumoAgua.data),'-',  func.to_char(ConsumoAgua.data, 'MM')).label('ano_mes')
                ).group_by(extract('year', ConsumoAgua.data), func.to_char(ConsumoAgua.data, 'MM'))\
                 .order_by(extract('year', ConsumoAgua.data), func.to_char(ConsumoAgua.data, 'MM'))\
                 .all()
                 
            data = []
            #para cada data na lista - percorre a lista 2021-10
            for data_intervalo in lista_com_intervalo:

                print("Data: ", data_intervalo)
                #para cada consulta na lista consulta - percorre os consulta 2021-11, 2021-12, 2024-1
                for data_resultado in consulta:
                    #comparar se data_intervalo é igual ao resultados na posição [1]
                    if data_intervalo == data_resultado[1] :
                        data.append({"gastosEscola": round(data_resultado[0], 3), "mes":converter_mes_ano(data_intervalo), "gastosNivel":""})
                        break
                    else:
                        continue
                if data_intervalo != data_resultado[1] :
                        data.append({"gastosEscola": 0, "mes":converter_mes_ano(data_intervalo), "gastosNivel":""})
    return jsonify({"data":data, "status": True}), 200


@dashboard.get('/cad-principal')
def cad_principal():

    # Total de Alunos
    populacao = db.session.query(
        func.sum(Populacao.alunos).label('alunos')
    )
    
    consumo = db.session.query(
            extract('year', ConsumoAgua.data).label('ano'),
            extract('month', ConsumoAgua.data).label('mes'),
            func.sum(ConsumoAgua.consumo).label('soma_consumo'),
            func.sum(ConsumoAgua.valor).label('soma_valor_ultimo_mes')
        ).group_by(
            extract('year', ConsumoAgua.data), extract('month', ConsumoAgua.data)
        ).order_by(desc(extract('year', ConsumoAgua.data)), desc(extract('month', ConsumoAgua.data))).first()
    print(consumo)
     # Concatenar ano e mês 
    if consumo is not None:
        mes_ano_str = f"{consumo[0]}-{consumo[1]}"
    else:
        mes_ano_str = f"00-00-2000"

    return jsonify({
        "data": [
            {"Alunos": populacao[0][0]},
            {"Consumo": consumo[2] if consumo is not None else 0},
            {"Valor": consumo[3] if consumo is not None else 0},
            {"Ano_mes": mes_ano_str if consumo is not None else 0}
        ]
    })


@dashboard.get('/cad-principal-escola/<int:id>')
def cad_principal_escola(id):
    
    #Filtro de escola
    edificios_alias = aliased(Edificios)
    populacao = db.session.query(
    func.sum(Populacao.alunos).label('alunos')
    ).join(edificios_alias, Populacao.fk_edificios == edificios_alias.id).filter(edificios_alias.fk_escola == id).all()

    # Consumo total
    consumo = db.session.query(
            extract('year', ConsumoAgua.data).label('ano'),
            extract('month', ConsumoAgua.data).label('mes'),
            func.sum(ConsumoAgua.consumo).label('soma_consumo'),
            func.sum(ConsumoAgua.valor).label('soma_valor_ultimo_mes')
        ).group_by(
            extract('year', ConsumoAgua.data), extract('month', ConsumoAgua.data)
        ).order_by(desc(extract('year', ConsumoAgua.data)), desc(extract('month', ConsumoAgua.data))
        ).filter(ConsumoAgua.fk_escola == id).first()

    mes_ano_str = f"{consumo[0]}-{consumo[1]}"

    return jsonify({
        "data": [
            {"Alunos": populacao[0][0]},
            {"Consumo": consumo[2]},
            {"Valor": consumo[3]},
            {"Ano_mes": mes_ano_str}
        ]
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


# TESTANDO RETORNO MES GRÁFICO DE LINHA
# @dashboard.get('/grafico-media-consumo-mensal-escolas_teste')
# def grafico_media_consumo_mensal_escolas_teste():
#     # maior data e menor - intervalo
#     data_consulta = db.session.query(
#         func.max(ConsumoAgua.data).label('maior_data'),
#         func.min(ConsumoAgua.data).label('menor_data')
#     )
#     # pegar resultado da consulta
#     data = data_consulta.all()
#     data_maior = data[0][0]
#     data_menor = data[0][1]
#     lista_com_intervalo = []

#     # alimentar a lista com intervalo de datas
#     while data_menor <= data_maior:
#         lista_com_intervalo.append(datetime.strftime(data_menor, "%Y-%m"))
#         if data_menor == data_maior:
#             break
#         prox_mes = data_menor.month + 1
#         if prox_mes > 12:
#             data_menor = data_menor.replace(year=data_menor.year + 1, month=1)
#         else:
#             data_menor = data_menor.replace(month=prox_mes)
#     print(lista_com_intervalo, min(lista_com_intervalo), max(lista_com_intervalo))
#     # saida atual '2024-4'
#     consulta = db.session.query(
#         func.avg(ConsumoAgua.consumo).label('media_escola'),
#         func.concat(extract('year', ConsumoAgua.data), '-',
#                     (extract('month', ConsumoAgua.data))).label('ano_mes')
#     ).group_by(extract('year', ConsumoAgua.data), extract('month', ConsumoAgua.data)).order_by(extract('year', ConsumoAgua.data), extract('month', ConsumoAgua.data))
#    # lista com mes-ano e consumo
#     resultados = consulta.all()
#     # percorrer a lista para concatenar mes e ano
#     print(resultados)
#     data = []
#     for data_intervalo in lista_com_intervalo:
#         for data_resultado in resultados:
#             # data está na lista
#             if data_intervalo == data_resultado[1]:
#                 data.append({
#                     "data": [
#                             {"gastosEscola": round(
#                                 data_resultado[0], 3), "mes": data_intervalo, "gastosNivel": ""}
#                             ],
#                     "status": True
#                 })
#             # data não está na lista
#             else:
#                 data.append({
#                     "data": [
#                         {"gastosEscola": "0", "mes_ano": data_intervalo,
#                             "gastosNivel": "0"}
#                     ],
#                     "status": True
#                 })
#     return jsonify(data), 200


#FAIXA DE CONSUMO - MAPA
@dashboard.get('/mapa_faixa_consumo_teste')
def mapa_faixa_consumo():
    
    lista = []
    
    #listar todas as escolas
    escolas = Escolas.query.all()

    #para cada escola verificar se tem consumo
    for escola in escolas:

        #pegar o ultimo consumo cadastrado da escola se tiver na tabela consumo 
        consumo_escola = db.session.query(
                func.sum(ConsumoAgua.consumo).label('consumo_escola'),
                func.concat(extract('year', ConsumoAgua.data), '-',
                            (extract('month', ConsumoAgua.data))).label('ano_mes')
            ).group_by(extract('year', ConsumoAgua.data), extract('month', ConsumoAgua.data)).order_by(desc(extract('year', ConsumoAgua.data)), desc(extract('month', ConsumoAgua.data))
            ).filter(ConsumoAgua.fk_escola == escola.id).first()
        
        print(consumo_escola, escola.id)
        
        if not consumo_escola:
            consumo_litros = 0
        
        #converter consumo em litros 
        else:
            # media = consumo_escola[0]
            consumo_litros = consumo_escola[0] * 1000
            
        #escola com consumo verde 
        if consumo_litros >= 0 and consumo_litros <= 10000:
            lista.append({
                "escola": escola.id,
                "nome_escola": escola.nome,
                # "lat": escola.lat,
                # "lon": escola.lon,
                "color": '#008000'
            })
            
        #escola com consumo amarelo
        if consumo_litros > 10000 and consumo_litros <= 30000:
            lista.append({
                "escola": escola.id,
                "nome_escola": escola.nome,
                # "lat": escola.lat,
                # "lon": escola.lon,
                "color": '#f6ef74'
            })
            
        #escola com consumo vermelho        
        if consumo_litros > 30000:
            lista.append({
                "escola": escola.id,
                "nome_escola": escola.nome,
                # "lat": escola.lat,
                # "lon": escola.lon,
                "color": '#ff0000'
            })
            
         
    return jsonify({"data":lista, "status":"ok"}), 200


@dashboard.get('/home_monig')
def home_monig():
    
    data = []
    
    #FILTRAR  ESCOLAS
    escolas = Escolas.query.all()
    
    for escola in escolas:
        #FILTRAR POPULACAO
        edificios_alias = aliased(Edificios)
        populacao = db.session.query(
            func.sum(Populacao.alunos).label('alunos')
        ).join(edificios_alias, Populacao.fk_edificios == edificios_alias.id).filter(edificios_alias.fk_escola == escola.id).all()


        #FILTRAR NIVEL
        result_nivel = db.session.query(
            EscolaNiveis.escola_id, AuxOpNiveis.nivel) \
        .join(AuxOpNiveis, AuxOpNiveis.id == EscolaNiveis.nivel_ensino_id) \
        .filter(EscolaNiveis.escola_id == escola.id) \
        .all()

        nivelRetorno = [nivel for escola_id, nivel in result_nivel]
	
 
        #FILTRAR CONSUMO E VALOR ULTIMO MÊS
        consumo = db.session.query(
            func.concat(extract('year', ConsumoAgua.data), '-',
                        extract('month', ConsumoAgua.data)).label('ano_mes'),
            func.sum(ConsumoAgua.consumo).label('soma_consumo'),
            func.sum(ConsumoAgua.valor).label('soma_valor_ultimo_mes')
        ).group_by('ano_mes')\
         .order_by(desc('ano_mes'))\
         .filter(ConsumoAgua.fk_escola == escola.id).first()
         
         
        #FILTRAR CONSUMO DOS ULTIMOS 6 MESES
        # Pega a data e hora atual
        data_atual = datetime.now()

        # Subtrai 6 meses da data atual
        mes_ano_6_meses = data_atual - timedelta(days=30 * 5)
        
        lista_intervalo = []
       #alimentar a lista com intervalo de datas
        while mes_ano_6_meses <= data_atual:
            lista_intervalo.append(mes_ano_6_meses.strftime("%Y-%m"))
            prox_mes = (mes_ano_6_meses.month % 12) + 1
            if prox_mes == 1:
                mes_ano_6_meses = mes_ano_6_meses.replace(year=mes_ano_6_meses.year + 1, month=1)
            else:
                mes_ano_6_meses = mes_ano_6_meses.replace(month=prox_mes)
                
        # Adicione a maior data à lista
        lista_intervalo.append(data_atual.strftime("%Y-%m"))
        
        #filtar os ultimos 6 meses de consumo da escola
        #retorna apenas os valores dos meses que tem no banco - ok
        consumo_seis_meses = db.session.query(
            func.sum(ConsumoAgua.consumo).label("consumo_"), 
            func.concat(extract('year', ConsumoAgua.data),'-', func.to_char(ConsumoAgua.data,'MM')).label('ano_mes_')\
        ).where(
            ConsumoAgua.data.between(
                func.date_trunc('month', func.current_date()) - func.cast(concat(5, 'months'), INTERVAL),
                func.current_date()
            )
        ).group_by(extract('year', ConsumoAgua.data), func.to_char(ConsumoAgua.data,'MM'))\
        .filter(ConsumoAgua.fk_escola == escola.id).all()
             
        consumoRetorno = []
                              
        for data_ in lista_intervalo:
            if any(data_ == i[1] for i in consumo_seis_meses):
                consumo_ = next(i[0] for i in consumo_seis_meses if data_ == i[1])
            else:
                consumo_ = 0

            consumoRetorno.append({"ano_mes": data_, "consumo_": consumo_})


        #RETORNO
        point = to_shape(escola.geom)
          
        data.append({
            "nome": escola.nome,
            "id": escola.id,
            "latitude": point.y,
            "longitude": point.x,
            "nivel_ensino": nivelRetorno,
            "numero_alunos": populacao[0][0],
            "consumo_agua": consumo[1] if consumo else 0,
            "valor_conta_agua": round(consumo[2], 2) if consumo else 0,
            'ano_mes_ultimo_consumo': consumo[0] if consumo else None,
            'consumo_ultimos_12_meses': consumoRetorno
        }) 
        
    return jsonify(data)