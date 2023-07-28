from flask import Blueprint, request, jsonify
from ..models import Escolas, db
import pandas as pd


valores = Blueprint('valores', __name__, url_prefix = '/api/v1/valores')

@valores.post('/valor')
def inserirGuarulhos():

    escolas = request.files['csv-escola']
    areaumida = request.files['csv-areaumida']

    if escolas.filename == '':
        return "Nome de arquivo vazio", 400
    
    try:
        dfEscola = pd.read_csv(escolas, header=0, sep=";", encoding='latin-1')
        dfAreaUmida = pd.read_csv(areaumida, header=0, sep=";", encoding='latin-1')

        print(dfEscola.columns)

        for index, row in dfEscola.iterrows():
        
            nome = row['Unidade Escolar'].upper()
            escolasinsert = Escolas(nome=nome)

            db.session.add(escolasinsert)

        db.session.commit()
            
    except Exception as e:
        return jsonify({
            "mensagem":"Erro não tratado!",
            "cod":str({e})
        })

    return jsonify({
        "mensagem":"Valore retornado!"
    })