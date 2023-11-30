from sqlalchemy import func
from ..models import ConsumoAgua,EscolaNiveis
from flask import Blueprint, json, jsonify


dashboard = Blueprint('dashboard', __name__,
                          url_prefix='/api/v1/dashboard')

@dashboard.get('/media_consumo')
def consumo_escolas():
        # filtrar a media de consumo de todas as escolas mes a mes
        consumo_escolas = ConsumoAgua.query.filter(ConsumoAgua.consumo != None).all() #pegar todas as escolas
        media_consumo_escolas = func.avg(consumo_escolas)
        
        # filtrar a media de consumo de acordo com os niveis
        media_consumo_niveis = ConsumoAgua.query.join(EscolaNiveis, ConsumoAgua.fk_escola == EscolaNiveis.escola_id).filter(ConsumoAgua.consumo != None).group_by(EscolaNiveis.nivel_ensino_id).having(func.sum(ConsumoAgua.consumo) > 0).with_entities(EscolaNiveis.nivel_ensino_id, func.avg(ConsumoAgua.consumo)).all()
       
        # pegar o mes de referencia
        mes_ref = ConsumoAgua.query.filter(ConsumoAgua.consumo != None).order_by(ConsumoAgua.data.desc()).first().data.month

        gastos_nivel = []
        for nivel, gasto in media_consumo_niveis:
            # converter o nivel para string
            nivel_str = str(nivel)
            # substituir a função pelo valor real
            gastos_nivel.append({"nivel": nivel_str, "gasto": gasto})
        
        # retornar os dados no formato JSON
        dados = [{
            "mes": mes_ref,
            "gastosEscola": media_consumo_escolas,
            "gastosNivel": gastos_nivel
        }] 

        return jsonify({"data": dados}),200
        
   
    
# const data = [
#   {
#     mes: "Jan",
#     gastosEscola: 4000,
#     gastosNivel: 2400,
#   },
#   {
#     mes: "Fev",
#     gastosEscola: 3000,
#     gastosNivel: 1398,
#   },
#   {
#     mes: "Mar",
#     gastosEscola: 2000,
#     gastosNivel: 9800,
#   },
#   {
#     mes: "Abr",
#     gastosEscola: 2780,
#     gastosNivel: 3908,
#   },
#   {
#     mes: "Mai",
#     gastosEscola: 1890,
#     gastosNivel: 4800,
#   },
#   {
#     mes: "Jun",
#     gastosEscola: 2390,
#     gastosNivel: 3800,
#   },
#   {
#     mes: "Jul",
#     gastosEscola: 3490,
#     gastosNivel: 4300,
#   },
#   {
#     mes: "Ago",
#     gastosEscola: 4200,
#     gastosNivel: 2000,
#   },
#   {
#     mes: "Set",
#     gastosEscola: 3100,
#     gastosNivel: 3000,
#   },
#   {
#     mes: "Out",
#     gastosEscola: 2500,
#     gastosNivel: 4200,
#   },
#   {
#     mes: "Nov",
#     gastosEscola: 2870,
#     gastosNivel: 1500,
#   },
#   {
#     mes: "Dez",
#     gastosEscola: 1980,
#     gastosNivel: 6000,
#   },
# ];

