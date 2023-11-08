from flask import Blueprint, request, jsonify
from ..models import Monitoramento, Hidrometros, Edificios, Escolas, db
from sqlalchemy import desc, extract
from sqlalchemy.orm import aliased
from datetime import datetime

monitoramento = Blueprint('monitoramento', __name__, url_prefix="/api/v1/monitoramento")

@monitoramento.post('/cadastrarleitura')
def leitura():
    try:
        formulario = request.get_json()
    
    except Exception as e:
        return jsonify({
            "mensagem":"Não foi possível recuperar o formulário!",
            "codigo":e,
            "status":False
        }), 400

    try:
        
        fk_escola = formulario["fk_escola"]
        hidrometro = formulario['hidrometro']
        leitura =f"{formulario['leitura']}{formulario['leitura2']}"
        print("leitura: ", leitura)
        datahora = f"{formulario['data'].replace('/','-')} {formulario['hora']}"
        datahora = datetime.strptime(datahora, '%d-%m-%Y %H:%M')
        
        # Extrair o ano, mês e dia da data
        ano = extract('year', datahora)
        mes = extract('month', datahora)
        dia = extract('day', datahora)

        # Consulta para verificar se a data é igual até o dia, mês e ano
        resultado = Monitoramento.query.filter(
            (ano == datahora.year) &
            (mes == datahora.month) &
            (dia == datahora.day) &
            (Monitoramento.fk_escola==fk_escola)
        ).all()
        
        if resultado > 1:
            print('Validação!!!')
            return jsonify({"mensagem":"Já foi realizado o envio hoje!", "status":False}), 400
        
        fk_hidrometro = Hidrometros.query.filter_by(hidrometro=hidrometro).first()
        
        if not fk_hidrometro:
            return jsonify({
                "mensagem":"Não foi encontrado o hidrometro",
                "status":False,
                "codigo":e
            }), 400
        
        monitoramento = Monitoramento(
            fk_escola=fk_escola,
            hidrometro=fk_hidrometro.id,
            leitura=leitura,
            datahora=datahora
        )
        
        db.session.add(monitoramento)
        db.session.commit()
        
        return jsonify({"formulario":monitoramento.to_json(), "mensagem":"Cadastro realizado com sucesso!"}), 200
    except Exception as e:
        return jsonify({
            "mensagem":"Erro não tratado.",
            "codigo":e,
            "status":False
        }), 400
        
    
@monitoramento.get("/leituras-tabela/<int:id>")
def leituras_tabela(id):
   
    escolamonitoramento = Monitoramento.query.filter_by(fk_escola = id).order_by(desc(Monitoramento.datahora)).all()  
    
    tabela = [{"id":leitura.id, "data": leitura.datahora.strftime('%d/%m/%Y'), "hora":leitura.datahora.strftime('%H:%M'), "leitura":leitura.leitura} for leitura in escolamonitoramento]
    
    return jsonify({
        "tabela":tabela,
        "nome":escolamonitoramento[0].escola_monitorada.nome if len(escolamonitoramento) > 0  else ""
    })

@monitoramento.get("/leitura-atual/<int:id>")
def leitura_atual(id):
    
    escola = Escolas.query.filter_by(id = id).first()
    
    edificios_alias = aliased(Edificios)

    # Realize a consulta usando filter e o alias
    hidrometro = Hidrometros.query.join(edificios_alias).filter(edificios_alias.fk_escola == id).first()
    
    escolamonitoramento = Monitoramento.query.filter_by(fk_escola = id).order_by(desc(Monitoramento.datahora)).first()
    
    jsonRetorno = {}
    jsonRetorno["nome"] = escola.nome
    jsonRetorno["hidrometro"] = hidrometro.hidrometro
    jsonRetorno["leitura"] = str(escolamonitoramento.leitura)[:3] if escolamonitoramento is not None else ""
    jsonRetorno["leitura2"] = str(escolamonitoramento.leitura)[3:] if escolamonitoramento is not None else ""

    return jsonRetorno

@monitoramento.patch("/edicao-monitoramento/<int:id>")
def leitura_edicao(id):
    
    monitoramento = Monitoramento.query.filter_by(id=id).first()
    if not monitoramento:
        
        return jsonify({"mensagem":"Não foi encontrada a leitura", "status":False}), 400
    
    try:
        formulario = request.get_json()
    except Exception as e:
        return jsonify({"mensagem":"Não foi possível encontrar o formulário enviado", "status":False}), 400
    
    try:

        datahora = f"{formulario['dataEditar'].replace('/','-')} {formulario['horaEditar']}"
        datahora = datetime.strptime(datahora, '%d-%m-%Y %H:%M')

        monitoramento.leitura = formulario['leituraEditar']
        monitoramento.datahora = datahora
        db.session.commit()
        
        return jsonify({"mensagem":"Edição realizado com sucesso", "leitura":monitoramento.to_json()}), 200

    except Exception as e:
        return jsonify({"mensagem":"Erro nas chaves do formulário enviado", "status":False}), 400
    
@monitoramento.delete("/deletar-leitura/<int:id>")
def leitura_deletar(id):
    
    monitoramento = Monitoramento.query.filter_by(id=id).first()
    
    if not monitoramento:
        return jsonify({"mensagem":"Não foi encontrada a leitura", "status":False}), 400
    
    db.session.delete(monitoramento)
    db.session.commit()
    
    return jsonify({"mensagem":"Deleção realizado com sucesso"}), 200