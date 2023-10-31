from flask import Blueprint, request, jsonify
from ..models import Monitoramento, Hidrometros, Edificios, Escolas, db
from sqlalchemy import desc
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