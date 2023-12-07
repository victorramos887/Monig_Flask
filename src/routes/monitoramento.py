from flask import Blueprint, request, jsonify
from ..models import Monitoramento, Hidrometros, Edificios, Escolas, db
from sqlalchemy import desc, extract, and_
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
        leitura = f"{formulario['leitura']}{formulario['leitura2']}"
        datahora = f"{formulario['data'].replace('/','-')} {formulario['hora']}"
        datahora = datetime.strptime(datahora, '%d-%m-%Y %H:%M')

        print(hidrometro)

        # fk_hidrometro = Hidrometros.query.filter_by(hidrometro=hidrometro).first()
        edificios_alias = aliased(Edificios)

        hidrometro_verificar = Hidrometros.query.join(edificios_alias).filter(and_(
            fk_escola == edificios_alias.fk_escola, Hidrometros.id == hidrometro)).first()

        if not hidrometro_verificar:
            return jsonify({"mensagem": "este hidrometro não pertence a esta escola!!!"}), 400

        escolas_com_mesmo_hidrometro = Hidrometros.query.join(
            edificios_alias).filter(Hidrometros.id == hidrometro).all()

        for escola_ in escolas_com_mesmo_hidrometro:

            escola_id = Edificios.query.filter_by(
                id=escola_.fk_edificios).first()

            escolamonitoramento_anterior = Monitoramento.query.filter(
                and_(
                    Monitoramento.fk_escola == escola_id.fk_escola,
                    Monitoramento.datahora < datahora
                )
            ).order_by(desc(Monitoramento.datahora)).first()

            escolamonitoramento_posterior = Monitoramento.query.filter(
                and_(
                    Monitoramento.fk_escola == escola_id.fk_escola,
                    Monitoramento.datahora > datahora
                )
            ).order_by(Monitoramento.datahora).first()

            if escolamonitoramento_anterior:
                # print("leitura enviada: ", int(leitura))
                # print("Ultima Leitura", escolamonitoramento.leitura)
                print("Escola datahora: ", escolamonitoramento_anterior.datahora)

                if escolamonitoramento_anterior.leitura > int(leitura):
                    return jsonify({"mensagem": "Não é possível inserir um valor menor do que o anterior!!", "status": False, "Leitura":escolamonitoramento_anterior.leitura}), 400
                
            if escolamonitoramento_posterior:
               
                print("Escola datahora: ", escolamonitoramento_posterior.datahora)
                
                if escolamonitoramento_posterior.leitura < int(leitura):
                    return jsonify({"mensagem": "Não é possível inserir um valor maior do que o sucessor!!", "status": False, "Leitura":escolamonitoramento_posterior.leitura}), 400
            # Extrair o ano, mês e dia da data
            ano = extract('year', datahora)
            mes = extract('month', datahora)
            dia = extract('day', datahora)

            # Consulta para verificar se a data é igual até o dia, mês e ano

            resultado = Monitoramento.query.filter(
                (extract('day', Monitoramento.datahora) == datahora.day) &
                (extract('month', Monitoramento.datahora) == datahora.month) &
                (extract('year', Monitoramento.datahora) == datahora.year) &
                (Monitoramento.fk_escola == escola_id.fk_escola)
            ).all()

            if len(resultado) > 1:
                return jsonify({"mensagem": f"Já foram adicionadas duas leituras no dia {datahora}", "status": False}), 400

            if len(resultado) == 1 and resultado[0].datahora >= datahora:
                return jsonify({"mensagem": "A segunda leitura deve ter um horário maior que a primeira", "status": False}), 400

            monitoramento = Monitoramento(
                fk_escola=escola_id.fk_escola,
                hidrometro=hidrometro_verificar.id,
                leitura=leitura,
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


@monitoramento.get("/leituras-tabela/<int:id>")
def leituras_tabela(id):

    escolamonitoramento = Monitoramento.query.filter_by(
        fk_escola=id).order_by(desc(Monitoramento.datahora)).all()

    tabela = [{"id": leitura.id, "data": leitura.datahora.strftime(
        '%d/%m/%Y'), "hora": leitura.datahora.strftime('%H:%M'), "leitura": leitura.leitura} for leitura in escolamonitoramento]

    return jsonify({
        "tabela": tabela,
        "nome": escolamonitoramento[0].escola_monitorada.nome if len(escolamonitoramento) > 0 else ""
    })


@monitoramento.get("/leitura-atual/<int:id>")
def leitura_atual(id):


    print(id)

    escola = Escolas.query.filter_by(id=id).first()
    if not escola:
        return jsonify({"mensagem":"Escola não encontrada!", "status":False}), 409

    edificios_alias = aliased(Edificios)

    # Realize a consulta usando filter e o alias
    hidrometro = Hidrometros.query.join(edificios_alias).filter(
        edificios_alias.fk_escola == id).first()

    escolamonitoramento = Monitoramento.query.filter_by(
        fk_escola=id).order_by(desc(Monitoramento.datahora)).first()

    jsonRetorno = {}
    jsonRetorno["nome"] = escola.nome
    jsonRetorno["hidrometro"] = hidrometro.hidrometro

    if escolamonitoramento:
        strinleitura = str(escolamonitoramento.leitura).zfill(8)
    else:
        strinleitura = ""


    print(strinleitura)
    jsonRetorno["leitura"] = strinleitura[0:4].zfill(5)
    jsonRetorno["leitura2"] = strinleitura[4:7].zfill(3)

    return jsonRetorno


@monitoramento.patch("/edicao-monitoramento/<int:id>")
def leitura_edicao(id):

    monitoramento = Monitoramento.query.filter_by(id=id).first()
    if not monitoramento:

        return jsonify({"mensagem": "Não foi encontrada a leitura", "status": False}), 400

    try:
        formulario = request.get_json()
    except Exception as e:
        return jsonify({"mensagem": "Não foi possível encontrar o formulário enviado", "status": False}), 400

    try:

        datahora = f"{formulario['dataEditar'].replace('/','-')} {formulario['horaEditar']}"
        datahora = datetime.strptime(datahora, '%d-%m-%Y %H:%M')

        monitoramento.leitura = formulario['leituraEditar']
        monitoramento.datahora = datahora
        db.session.commit()

        return jsonify({"mensagem": "Edição realizado com sucesso", "leitura": monitoramento.to_json()}), 200

    except Exception as e:
        return jsonify({"mensagem": "Erro nas chaves do formulário enviado", "status": False}), 400


@monitoramento.delete("/deletar-leitura/<int:id>")
def leitura_deletar(id):

    monitoramento = Monitoramento.query.filter_by(id=id).first()

    if not monitoramento:
        return jsonify({"mensagem": "Não foi encontrada a leitura", "status": False}), 400

    db.session.delete(monitoramento)
    db.session.commit()

    return jsonify({"mensagem": "Deleção realizado com sucesso"}), 200
