from flask import Blueprint, request, jsonify
from ..models import Monitoramento, Hidrometros, Edificios, Escolas, db
from sqlalchemy import desc, extract, and_, func
from sqlalchemy.orm import aliased
from datetime import datetime, timedelta
from flasgger import swag_from


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
        datahora = datetime.strptime(datahora, '%d-%m-%Y %H:%M')
        edificios_alias = aliased(Edificios)
        leitura_float = float(leitura.replace('.', '').replace(',', '.'))

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
            ).order_by(Monitoramento.datahora).first()

            escolamonitoramento_anterior = (

                db.session.query(
                    Monitoramento.id,
                    Monitoramento.datahora,
                    Monitoramento.leitura
                )
                .filter(
                    and_(
                        func.extract('year', Monitoramento.datahora) == func.extract(
                            'year', datahora),
                        func.extract('month', Monitoramento.datahora) == func.extract(
                            'month', datahora),
                        func.extract('day', Monitoramento.datahora) == func.extract(
                            'day', datahora),
                        Monitoramento.datahora < datahora,
                        Monitoramento.fk_escola == fk_escola,
                    )

                )
                .first()
            )

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

                if escolamonitoramento_anterior[2] > leitura_float:
                    return jsonify({"mensagem": "Não é possível inserir um valor menor do que o anterior!!", "status": False, "Leitura": escolamonitoramento_anterior.leitura}), 400

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
