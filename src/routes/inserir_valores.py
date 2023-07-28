from flask import Blueprint, request, jsonify
from ..models import Escolas, Edificios, db
import pandas as pd


valores = Blueprint('valores', __name__, url_prefix='/api/v1/valores')


@valores.post('/valor')
def inserirGuarulhos():

    escolas = request.files['csv-escola']
    areaumida = request.files['csv-areaumida']

    if escolas.filename == '':
        return "Nome de arquivo vazio", 400

    try:
        dfEscola = pd.read_csv(escolas, header=0, sep=";", encoding='latin-1')
        dfAreaUmida = pd.read_csv(
            areaumida, header=0, sep=";", encoding='latin-1')

        print(dfEscola.columns)

        for index, row in dfEscola.iterrows():

            # """
            #     'ID', 'Unidade Escolar', 'Logradouro', 'Nº do Hidrômetro',
            #     'Tipo Hidrometro', 'Data inspeção', 'Horário de início',
            #     'Horário de Termino', 'DN da Tubulação de entrada (mm)',
            #     'Ano de construição (reservatório)', 'Qnt. De Reservatório',
            #     'Precisa de Reforma', 'Alt. Reservatório (m)', 'Vol. Reservatório (L)',
            #     'Elevado', 'Enterrado', 'semi-enterrado', 'torre', 'PVC', 'CONCRETO',
            #     'METALICO', 'Se Houver', 'Reservatório de água de reuso', 'Marca',
            #     'Modelo', 'Potencia', 'Vazão', 'Marca2', 'Modelo3', 'Potencia4',
            #     'Vazão5', 'Marca6', 'Modelo7', 'Potencia8', 'Vazão9', 'Bomba reserva',
            #     'Técnico Responsável', 'Ajudante Técnico', 'Observações'
            # """

            nome = row['Unidade Escolar'].upper()
            endereco = str(row['Logradouro']).split(',')
            if len(endereco) >= 2:
                numero = endereco[1]
                logradouro = endereco[0]
            else:
                logradouro = endereco[0]
                numero = "S/N"

            hidrometro = row['Nº do Hidrômetro']
            nivelenviado = row['Se Houver']

            print(logradouro,' - nº:' ,numero)

            escolainsert = Escolas(
                nome=nome,
                cnpj='000000000000',
                telefone='0',
                email='-'
            )


            edificioinsert = Edificios(
                fk_escola = escolainsert.id,
                principal=True,
                nome_do_edificio=nome,
                logradouro_edificio=logradouro,
                numero_edificio=numero,
                cidade_edificio='Guarulhos',
                cnpj_edificio='000000000000',
                estado_edificio='SP'
            )

            db.session.add(escolainsert)
            db.session.add(edificioinsert)

        db.session.commit()
        return jsonify({"mensagem": "Valore retornado!"})

    except Exception as e:
        return jsonify({
            "mensagem": "Erro não tratado!",
            "cod": str({e})
        }), 400

    
