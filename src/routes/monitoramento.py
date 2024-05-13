from flask import Blueprint, request, jsonify
from ..models import Monitoramento, Hidrometros, Edificios, Escolas, Populacao, db
from sqlalchemy import desc, extract, and_, func, text
from sqlalchemy.orm import aliased
from datetime import datetime, timedelta
from flasgger import swag_from
# from flask import Blueprint, request, jsonify
# from ..models import Monitoramento, Hidrometros, Edificios, Escolas, Populacao, db
# from sqlalchemy import desc, extract, and_, func, text
from sqlalchemy.sql.functions import concat
from sqlalchemy.dialects.postgresql import INTERVAL



monitoramento = Blueprint('monitoramento', __name__,
                          url_prefix="/api/v1/monitoramento")


@swag_from('../docs/cadastros/monitoramento/leitura.yaml')
@monitoramento.post('/cadastrarleitura')
def leitura():
    try:
        formulario = request.get_json()


    except Exception as e:
        return jsonify({
            "mensagem": "Não foi possível recuperar o formulário!",
            "codigo": e,
            "status": False
        }), 400

    try:

        fk_escola = formulario["fk_escola"]
        hidrometro = formulario['hidrometro']
        leitura = f"{formulario['leitura']}"
        datahora = f"{formulario['data'].replace('/','-')} {formulario['hora']}"
        datahora = datetime.strptime(datahora, '%d-%m-%Y %H:%M:%S')
        edificios_alias = aliased(Edificios)
        print(f"\033[31m{leitura}\033[0m")
        leitura_float = float(leitura.replace(',', '.'))
        print(f"\033[32m{leitura_float}\033[0m")

        hidrometro_verificar = Hidrometros.query.join(edificios_alias).filter(and_(
            fk_escola == edificios_alias.fk_escola, Hidrometros.hidrometro == hidrometro)).first()

        if not hidrometro_verificar:
            return jsonify({"mensagem": "este hidrometro não pertence a esta escola!!!"}), 400

        escolas_com_mesmo_hidrometro = Hidrometros.query.join(
            edificios_alias).filter(Hidrometros.hidrometro == hidrometro).all()

        for escola_ in escolas_com_mesmo_hidrometro:
            # Correção
            escola_id = Edificios.query.filter_by(
                id=escola_.fk_edificios).first()

            escolamonitoramento_anterior = Monitoramento.query.filter(
                and_(
                    Monitoramento.fk_escola == fk_escola,
                    Monitoramento.datahora < datahora
                ) 
            ).order_by(desc(Monitoramento.datahora)).first()

            # escolamonitoramento_anterior = (

            #     db.session.query(
            #         Monitoramento.id,
            #         Monitoramento.datahora,
            #         Monitoramento.leitura
            #     )
            #     .filter(
            #         and_(
            #             func.extract('year', Monitoramento.datahora) == func.extract(
            #                 'year', datahora),
            #             func.extract('month', Monitoramento.datahora) == func.extract(
            #                 'month', datahora),
            #             func.extract('day', Monitoramento.datahora) == func.extract(
            #                 'day', datahora),
            #             Monitoramento.datahora < datahora,
            #             Monitoramento.fk_escola == fk_escola,
            #         )

            #     )
            #     .first()
            # )

            escolamonitoramento_posterior = Monitoramento.query.filter(
                and_(
                    Monitoramento.fk_escola == fk_escola,
                    Monitoramento.datahora > datahora
                )
            ).order_by(Monitoramento.datahora).first()

            escolamonitoramento_posterior = (

                db.session.query(
                    Monitoramento.id,
                    Monitoramento.datahora,
                    Monitoramento.leitura
                )
                .filter(
                    and_(
                        Monitoramento.datahora > datahora,
                        Monitoramento.fk_escola == fk_escola,
                    )

                )
                .order_by(Monitoramento.datahora.asc())
                .first()
            )

            if escolamonitoramento_anterior:

                if escolamonitoramento_anterior.leitura > leitura_float:
                    return jsonify({"mensagem": "Não é possível inserir um valor menor do que o anterior!!", "status": False, "Leitura": escolamonitoramento_anterior.leitura}), 400

                #verificar se a leitura anterior está com o mesmo minuto
                if escolamonitoramento_anterior.datahora == datahora.minute and datahora.second:
                    return jsonify({"mensagem": "Não é possível inserir um valor menor do que o anterior!!", "status": False}) ,400
                
            if escolamonitoramento_posterior:

                # print("Leitura posterio datahora: ",
                #       escolamonitoramento_posterior.datahora)

                if escolamonitoramento_posterior[2] < leitura_float:
                    return jsonify({"mensagem": "Não é possível inserir um valor maior do que o sucessor!!", "status": False, "Leitura": escolamonitoramento_posterior.leitura}), 400
            # Extrair o ano, mês e dia da data
            ano = extract('year', datahora)
            mes = extract('month', datahora)
            dia = extract('day', datahora)

            #print(f"\033[32m{dia}/{mes}/{ano}\033[0m")

            print(f"\033[32m{escola_id.fk_escola}\033[0m")

            # Consulta para verificar se a data é igual até o dia, mês e ano
            resultado = Monitoramento.query.filter(
                (extract('day', Monitoramento.datahora) == datahora.day) &
                (extract('month', Monitoramento.datahora) == datahora.month) &
                (extract('year', Monitoramento.datahora) == datahora.year) &
                (Monitoramento.fk_escola == fk_escola)
            ).all()


            if len(resultado) > 1:
                return jsonify({"mensagem": f"Já foram adicionadas duas leituras no dia {datahora}", "status": False}), 400

            # if escola_id != fk_escola:
           
            #     monitoramento = Monitoramento(
            #     fk_escola=escola_id.fk_escola,
            #     hidrometro=hidrometro_verificar.id,
            #     leitura=leitura_float,
            #     datahora=datahora
            #     )
            #     db.session.add(monitoramento)
            #     db.session.commit()

        monitoramento = Monitoramento(
            fk_escola=fk_escola,
            hidrometro=hidrometro_verificar.id,
            leitura=leitura_float,
            datahora=datahora
        )

        db.session.add(monitoramento)
        db.session.commit()

        return jsonify({"mensagem": "Cadastro realizado com sucesso!"}), 200

    except Exception as e:
        return jsonify({
            "mensagem": "Erro não tratado.",
            "codigo": e,
            "status": False
        }), 400

#retorna todas as leituras
@swag_from('../docs/get/monitoramento/leitura_tabela.yaml')
@monitoramento.get("/leituras-tabela/<int:id>")
def leituras_tabela(id):

    escolamonitoramento = Monitoramento.query.filter_by(
        fk_escola=id).order_by(desc(Monitoramento.datahora)).all()
    
    print("Monitoramento: ", escolamonitoramento)

    tabela = []
    if len(escolamonitoramento) > 1:
        for i in range(0, len(escolamonitoramento)):
            indexanterior = i + 1
            range_list = len(escolamonitoramento) - 1

            if indexanterior <= range_list:
                diferenca = escolamonitoramento[i].leitura - \
                    escolamonitoramento[indexanterior].leitura

            tabela.append(
                {
                    "id": escolamonitoramento[i].id, 
                    "data": escolamonitoramento[i].datahora.strftime('%d/%m/%Y'), 
                    "hora": escolamonitoramento[i].datahora.strftime('%H:%M'), 
                    "leitura": f"{escolamonitoramento[i].leitura:,.3f}" if escolamonitoramento[i].leitura is not None else "N/A", #float(escolamonitoramento[i]['leitura']).format('.3f'), 
                    "diferenca": f"{diferenca:,.3f}" if diferenca is not None else "N/A" 
                }
            )
    return jsonify({
        "tabela": tabela,
        "nome": escolamonitoramento[0].escola_monitorada.nome if len(escolamonitoramento) > 0 else ""
    })


#retorna a ultima leitura cadastrada
@swag_from('../docs/get/monitoramento/leitura_atual.yaml')
@monitoramento.get("/leitura-atual/<int:id>")
def leitura_atual(id):

    print(id)

    escola = Escolas.query.filter_by(id=id).first()
    if not escola:
        return jsonify({"mensagem": "Escola não encontrada!", "status": False}), 409

    edificios_alias = aliased(Edificios)

    # Realize a consulta usando filter e o alias
    hidrometro = Hidrometros.query.join(edificios_alias).filter(
        edificios_alias.fk_escola == id).first()

    escolamonitoramento = Monitoramento.query.filter_by(
        fk_escola=id).order_by(desc(Monitoramento.datahora)).first()

    jsonRetorno = {}
    jsonRetorno["nome"] = escola.nome
    jsonRetorno["hidrometro"] = hidrometro.hidrometro
    print(jsonRetorno)
    # if escolamonitoramento:
    #     inteiro = str(int(escolamonitoramento.leitura)).zfill(7)
    #     racional = str(int(round(abs(escolamonitoramento.leitura % 1) * 1000)))
    # else:
    #     inteiro = ""
    #     racional = ""
    print("Escola monitorada: ", escolamonitoramento)
    if escolamonitoramento is not None:
        jsonRetorno["leitura"] = escolamonitoramento.leitura
    else:
        jsonRetorno["leitura"] = "0"

    #jsonRetorno["leitura2"] = racional.zfill(3)


    return jsonRetorno


@swag_from('../docs/editar/monitoramento/leitura.yaml')
@monitoramento.patch("/edicao-monitoramento/<int:id>")
def leitura_edicao(id):
    monitoramento = Monitoramento.query.filter_by(id=id).first()

    #outras leituras iguais
    monitoramento_editar_outras = Monitoramento.query.filter(
                (extract('day', Monitoramento.datahora) == monitoramento.datahora.day) &
                (extract('month', Monitoramento.datahora) == monitoramento.datahora.month) &
                (extract('year', Monitoramento.datahora) == monitoramento.datahora.year) &
                (Monitoramento.fk_escola == monitoramento.fk_escola)
            ).all()
    
    print("Monitoramento: ", monitoramento_editar_outras)

    if not monitoramento:       
        return jsonify({"mensagem": "Não foi encontrada a leitura", "status": False}), 400

    try:
        formulario = request.get_json()
    except Exception as e:
        print(f"Não foi possível encontrar o formulário enviado \033[32m{e}\033[0m")
        return jsonify({"mensagem": "Não foi possível encontrar o formulário enviado", "status": False}), 400
    
    try:


            
        datahora = f"{formulario['dataEditar'].replace('/','-')} {formulario['horaEditar']}"
        datahora = datetime.strptime(datahora, '%d-%m-%Y %H:%M')
        
        if len(monitoramento_editar_outras)>1:
            for mon in monitoramento_editar_outras:
                mon.leitura =  float(formulario['leituraEditar'].replace(',', '.'))
                mon.datahora = datahora

                db.session.commit()

        monitoramento.leitura = float(formulario['leituraEditar'].replace(',', '.'))
        monitoramento.datahora = datahora
        db.session.commit()

        return jsonify({"mensagem": "Edição realizado com sucesso", "leitura": monitoramento.to_json()}), 200

    except Exception as e:
        print(f"Erro nas chaves do formulário enviado \033[32m{e}\033[0m")
        return jsonify({"mensagem": f"Erro nas chaves do formulário enviado \033[32m{e}\033[0m", "status": False}), 400


@swag_from('../docs/remover/monitoramento/leitura.yaml')
@monitoramento.delete("/deletar-leitura/<int:id>")
def leitura_deletar(id):
    edificios_alias = aliased(Edificios)
    monitoramento = Monitoramento.query.filter_by(id=id).first()
    hidrometro = monitoramento.hidrometro
    
    escolas_com_mesmo_hidrometro = Hidrometros.query.join(
            edificios_alias).filter(Hidrometros.id == hidrometro).all()
    
    # print("Hidrometro: ", escolas_com_mesmo_hidrometro[0])
    # # Itera sobre cada objeto Hidrometros retornado e imprime todos os seus atributos
    # for hidrometro_obj in escolas_com_mesmo_hidrometro:
    #     atributos = vars(hidrometro_obj)
    #     for atributo, valor in atributos.items():
    #         print(atributo, ":", valor)
        
    #     # Adicione uma linha em branco entre cada objeto para melhor legibilidade
    #     print()

    if not monitoramento:
        return jsonify({"mensagem": "Não foi encontrada a leitura", "status": False}), 400
    
    monitoramentos_excluir = Monitoramento.query.filter(
                # (extract('day', Monitoramento.datahora) == monitoramento.datahora.day) &
                # (extract('month', Monitoramento.datahora) == monitoramento.datahora.month) &
                # (extract('year', Monitoramento.datahora) == monitoramento.datahora.year) &
                (Monitoramento.datahora == monitoramento.datahora) &
                (Monitoramento.hidrometro == escolas_com_mesmo_hidrometro[0].id)
            ).all()
    print("Hidrometros: ", monitoramentos_excluir)         


    for mexcluir in monitoramentos_excluir:
        db.session.delete(mexcluir)
        db.session.commit()

    return jsonify({"mensagem": "Deleção realizado com sucesso"}), 200

#retorna 
# @swag_from('')
@monitoramento.get("/monitoramento-volumes/<int:id>")
def leituras_volumes(id):

    # query = Monitoramento.query.filter_by(fk_escola=id).all()
    escola = Escolas.query.filter_by(id=id).first()

    query = db.session.query(
        Monitoramento.id,
        Monitoramento.datahora,
        Monitoramento.leitura,
        func.lag(Monitoramento.datahora).over(
            order_by=Monitoramento.datahora).label('datalog'),
        func.lag(Monitoramento.leitura).over(
            order_by=Monitoramento.datahora).label('leituralag')
    ).filter(Monitoramento.fk_escola == id).all()

    dicionario = {}
    retorno = []
    for row in query:

        id = row[0]
        data = row[1]
        letura = row[2]
        dataanterior = row[3]
        leituraanterior = row[4]

        # print(f"Data: {data}  --  Data anterior: {dataanterior}")
        # print(f"Leitura: {letura}  --   Leitura anterior: {leituraanterior}")

        if data is not None and dataanterior is not None:

            diferenca = data-dataanterior

            diferenca_horas = abs(diferenca).total_seconds() / 3600

            print(f"Dias: {data.day} -- Segundos: {diferenca_horas}")
            diferenca = None

            if data.day == dataanterior.day and data.month == dataanterior.month and data.year == dataanterior.year:
                diferenca = letura - leituraanterior
            elif diferenca_horas < 16:
                diferenca = letura - leituraanterior

            dicionario = {
                "id": id,
                "Data": data.strftime('%d/%m/%Y'),
                "Hora": data.strftime("%H:%M"),
                "Leitura": f"{letura:,.3f}",
                "DataAnterior": dataanterior.strftime('%d/%m/%Y'),
                "HoraAnterior": dataanterior.strftime("%H:%M"),
                "LeituraAnterior": f"{leituraanterior:,.3f}",
                "Diferenca": f"{diferenca:,.3f}" if diferenca is not None and type(diferenca) in (int, float) else "N/A"
            }

            # print(dicionario)
        else:
            dicionario = {
                "id": id,
                "Data": data.strftime('%d/%m/%Y'),
                "Hora": data.strftime("%H:%M"),
                "Leitura": letura,
                "DataAnterior": None,
                "HoraAnterior": None,
                "LeituraAnterior": None,
                "Diferenca": None
            }

        retorno.append(dicionario)


    #Ordenar por data e hora
    retorno = sorted(retorno, key=lambda x: datetime.strptime(f"{x['Data']} {x['Hora']}", '%d/%m/%Y %H:%M'), reverse=True)


    return {
        "tabela": retorno,
        "nome": escola.nome if escola is not None else ""
    }


#Retornar escolas com leituras diurnas e noturnas no início

# RETORNA TODAS AS ESCOLAS
@monitoramento.get('/escolas')
def escolas():
    

    #Returno da ultima leitura diurna e noturna
    

    escolas = Escolas.query.all()
    return jsonify({
        'return': [escola.to_json() for escola in escolas],
        'status': True,
        'mensagem': 'Escolas retornadas com sucesso'
    }), 200



# RETORNA TODAS AS ESCOLAS
@monitoramento.get('/relatorio_escolas/<int:h>')
def relatorio_escolas(h):

    #buscar na tabela - registro do hidrometro passado
    monitoramento = Monitoramento.query.filter_by(hidrometro=h).all()
   
    if not monitoramento:
        return jsonify('Hidrometro sem registro de consumo'), 400

    data = []
 
    #calcular consumo dos últimos 30 dias
    consumo_30 = db.session.query(
        func.min(Monitoramento.datahora).label('inicio_intervalo'),
        func.max(Monitoramento.datahora).label('fim_intervalo'),
        func.max(Monitoramento.leitura) - func.min(Monitoramento.leitura).label('consumo_30_dias')
    ).where(
        Monitoramento.datahora.between(
            func.date_trunc('days', func.current_date()) - func.cast(concat(30, 'days'), INTERVAL),
            func.current_date()
        )
    ).filter(Monitoramento.hidrometro==h).all()

    #consumo do dia - 2 leitura do dia
    consumo_dia = text("""
        select
            MAX(tb.datahora) AS maior_data,
            MIN(tb.datahora) AS menor_data,
            MAX(tb.leitura) - MIN(tb.leitura)AS consumo_dia
            from(select *, 
                RANK() OVER (ORDER BY DATE(datahora) DESC) AS rank_data
                from main.monitoramento
                where hidrometro = :hid
        limit 3)as tb
        group by rank_data 
        having count(rank_data)>1 
        limit 2;
        """).bindparams(hid=h)
                  
    consumo_dia_ = db.session.execute(consumo_dia)
    resultado_consumo_dia = consumo_dia_.fetchall()
    
    #consumo noturno - 2º leitura
    consumo_noturno = text("""
            WITH retorno AS (SELECT m.id,
                        m.hidrometro,
                        m.leitura,
                        lag(m.leitura) OVER (PARTITION BY m.hidrometro ORDER BY m.datahora) AS leitura_lag,
                            CASE
                                WHEN date_part('hour'::text, m.datahora) <= 9::double precision AND (m.datahora - '16:00:00'::interval) <= lag(m.datahora) OVER (PARTITION BY m.hidrometro ORDER BY m.datahora) THEN
                                NULLIF(m.leitura - lag(m.leitura) OVER (PARTITION BY m.hidrometro ORDER BY m.datahora), 0::double precision)
                                ELSE NULL::double precision
                            END AS diferenca,
                        m.datahora AS dataatual,
                        lag(m.datahora) OVER (PARTITION BY m.hidrometro ORDER BY m.datahora) AS datalag,
                        row_number() OVER (PARTITION BY m.hidrometro ORDER BY m.datahora) AS row_num
                    FROM main.monitoramento m
                    WHERE m.hidrometro =:hid
                    ORDER BY m.datahora DESC)
            SELECT re.* FROM retorno re WHERE re.diferenca IS NOT NULL LIMIT 1;""").bindparams(hid=h)
        
            
    consumo_not = db.session.execute(consumo_noturno)
    resultado_consumo_not = consumo_not.fetchall()
  
    #retorna populacao do edificio que contem esse hidrometro
    alunos = db.session.query(
            Hidrometros.id,
            Hidrometros.hidrometro,
            Hidrometros.fk_edificios,
            func.sum(Populacao.alunos).label('total_alunos')
        ).join(Populacao, Populacao.fk_edificios == Hidrometros.fk_edificios, isouter=True) \
        .filter(Hidrometros.id == h)\
        .group_by(Populacao.fk_edificios, Hidrometros.id).all()

    edificio = Edificios.query.filter_by(id=alunos[0][2]).first()
    escola_id = edificio.fk_escola if edificio.fk_escola is not None else None

    #consumo dia
    consumo_ = round(resultado_consumo_dia[0][2],2) if len(resultado_consumo_dia) > 0 else 0
    consumo_lts = consumo_ * 1000
    total_alunos_ = alunos[0][3] if len(alunos) > 0 else None
    consumo_alunos_ = round((consumo_lts/ total_alunos_), 2) if total_alunos_ is not None else None

    #consumo alunos mensal
    consumo = round(consumo_30[0][2],2) if consumo_30[0][2] is not None else 0
    consumo_lts = consumo * 1000
    total_alunos = alunos[0][3] if len(alunos) > 0 else None
    consumo_alunos = (consumo_lts/ total_alunos) if total_alunos is not None else None
    consumo_alunos_mensal = round(consumo_alunos/30, 2) if consumo_alunos is not None else None

    
    data.append({
        "id_hidrometro": alunos[0][0] if len(alunos) > 0 else None,
        "hidrometro": alunos[0][1] if len(alunos) > 0 else None,
        "edificio_id":alunos[0][2] if len(alunos) > 0 else None,
        "escola_id": escola_id,
        "total_alunos": total_alunos,
        "consumo_30_dias":{
            "data_inicio": f'{consumo_30[0][0]:%d/%m/%Y %H:%M}' if consumo_30[0][0] else None,
            "data_fim": f'{consumo_30[0][1]:%d/%m/%Y %H:%M}' if consumo_30[0][1] else None,
            "consumo_m3": consumo,
            "consumo_por_aluno_lt": consumo_alunos_mensal
            },
        "consumo_dia": {
            "consumo_1_dia_m3": consumo_,
            "consumo_1_dia_lt": consumo_alunos_,
            "data": f'{resultado_consumo_dia[0][0]:%d/%m/%Y}'if len(resultado_consumo_dia) > 0 else None
        },
        "consumo_noturno":{
            "consumo_m3": round(resultado_consumo_not[0][4] if len(resultado_consumo_not) > 0 else 0, 2),
            "ultimo_consumo": f'{resultado_consumo_not[0][6]:%d/%m/%Y %H:%M}' if len(resultado_consumo_not) > 0 else None
            }})
    
    return jsonify(data), 200
   