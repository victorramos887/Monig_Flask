from flask import Blueprint, request, jsonify
from sqlalchemy import or_, and_
from werkzeug.security import generate_password_hash
from ..models import Escolas, Edificios, Hidrometros, AuxTipoHidrometro, AreaUmida, Equipamentos, Usuarios, db
import pandas as pd
import math
from geoalchemy2 import WKTElement
from unidecode import unidecode
import random
# from flasgger import swag_from

valores = Blueprint('valores', __name__, url_prefix='/api/v1/valores')


@valores.put("/geometria")
def geometriaUpdate():

    geometria = request.files["csv-geometria"]

    if geometria.filename == '':
        return "Nome de arquivo vazio", 400

    try:

        dfGeometria = pd.read_csv(
            geometria, header=0, sep=";", encoding="latin-1")

       # Converte o campo "geom" para uma string
        dfGeometria["geom"] = dfGeometria["geom"].astype(str)
        dfGeometria['geom'] = dfGeometria['geom'].apply(
            lambda x: x.replace('MULTIPOINT ((', 'POINT(').replace('))', ')'))

        for row in dfGeometria.itertuples():
            # 'row' é um namedtuple com os valores da linha

            # Verifica se 'geom' não está vazio (nulo)
            if row.geom and row.geom != "nan":

                escola = Escolas.query.filter_by(nome=row.nome).first()

                # # Construa o objeto WKTElement apenas se 'geom' não for vazio
                geom_wkt = WKTElement(row.geom, srid=4674)

                if escola:
                    escola.update(geom=geom_wkt)

                # Construa a cláusula de atualização usando o geoalchemy2

            db.session.commit()

        return "Avaliação"
    except Exception as e:
        return jsonify({
            "mensagem": "Erro não tratado!",
            "cod": str({e})
        }), 400


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

        for index, row in dfEscola.iterrows():

            nome = row['Unidade Escolar'].upper()
            endereco = str(row['Logradouro']).split(',')
            if len(endereco) >= 2:
                numero = endereco[1]
                logradouro = endereco[0]
            else:
                logradouro = endereco[0]
                numero = "S/N"

            hidrometro = row['Nº do Hidrômetro']
            tipohidrometro = row['Tipo Hidrometro']
            nivelenviado = row['Se Houver']

            if Escolas.query.filter_by(nome=nome).first():
                pass
            else:
                escolainsert = Escolas(
                    nome=nome,
                    cnpj='000000000000',
                    telefone='0',
                    email='-'
                )

                db.session.add(escolainsert)
                db.session.commit()

                edificioinsert = Edificios(
                    fk_escola=escolainsert.id,
                    principal=True,
                    nome_do_edificio=nome,
                    logradouro_edificio=logradouro,
                    numero_edificio=numero,
                    cidade_edificio='Guarulhos',
                    cnpj_edificio='000000000000',
                    estado_edificio='SP',
                    cep_edificio='00000-XXX'
                )

                db.session.add(edificioinsert)
                db.session.commit()

                if type(tipohidrometro) == str:
                    tipo = AuxTipoHidrometro.query.filter_by(
                        tipo_hidrometro=tipohidrometro).first()

                    if tipo:
                        tipo = tipo.id

                        hidrometroinsert = Hidrometros(
                            fk_edificios=edificioinsert.id,
                            fk_hidrometro=tipo,
                            hidrometro=hidrometro
                        )
                        db.session.add(hidrometroinsert)
                        db.session.commit()

                aumida = dfAreaUmida.loc[dfAreaUmida['idEscola'] == row['ID']]

                for i, r in aumida.iterrows():
                    fk_edificio = edificioinsert.id
                    nomearea = r['Local']

                    equipamentos = {
                        'vh': r['VH'],
                        'ca': r['CA'],
                        'tc': r['TC'],
                        'ta': r['TA'],
                        'ch': r['CH'],
                        'mi': r['MI'],
                        'be': r['BE']
                    }
                    foradeusuo = r['Fora de uso']

                    if 'cozinha' in nomearea.lower() or 'refeitorio' in nomearea.lower() or 'refeitório' in nomearea.lower():
                        areainsert = AreaUmida(
                            fk_edificios=fk_edificio,
                            tipo_area_umida=2,
                            nome_area_umida=nomearea
                        )

                    elif 'banheiro' in nomearea.lower():

                        areainsert = AreaUmida(
                            fk_edificios=fk_edificio,
                            tipo_area_umida=1,
                            nome_area_umida=nomearea
                        )

                    elif 'Lavanderia' in nomearea.lower():

                        areainsert = AreaUmida(
                            fk_edificios=fk_edificio,
                            tipo_area_umida=3,
                            nome_area_umida=nomearea
                        )

                    else:

                        areainsert = AreaUmida(
                            fk_edificios=fk_edificio,
                            tipo_area_umida=6,
                            nome_area_umida=nomearea
                        )
                    db.session.add(areainsert)
                    db.session.commit()

                    for key, value in equipamentos.items():

                        if key == 'vh' and not math.isnan(value):

                            vh = Equipamentos(
                                fk_area_umida=areainsert.id,
                                tipo_equipamento=2,
                                quantTotal=value

                            )

                            db.session.add(vh)
                        elif key == 'ca' and not math.isnan(value):

                            ca = Equipamentos(
                                fk_area_umida=areainsert.id,
                                tipo_equipamento=1,
                                quantTotal=value

                            )
                            db.session.add(ca)
                        elif key == 'tc' and not math.isnan(value):

                            tc = Equipamentos(
                                fk_area_umida=areainsert.id,
                                tipo_equipamento=16,
                                quantTotal=value

                            )
                            db.session.add(tc)

                        elif key == 'ta' and not math.isnan(value):

                            ta = Equipamentos(
                                fk_area_umida=areainsert.id,
                                tipo_equipamento=16,
                                quantTotal=value

                            )
                            db.session.add(ta)
                        elif key == 'ch' and not math.isnan(value):

                            ch = Equipamentos(
                                fk_area_umida=areainsert.id,
                                tipo_equipamento=6,
                                quantTotal=value

                            )
                            db.session.add(ch)
                        elif key == 'mi' and not math.isnan(value):
                            # não foi definido qual mictório
                            mi = Equipamentos(
                                fk_area_umida=areainsert.id,
                                tipo_equipamento=10,
                                quantTotal=value

                            )
                            db.session.add(mi)

                        elif key == 'be' and not math.isnan(value):
                            # não foi definido qual mictório
                            be = Equipamentos(
                                fk_area_umida=areainsert.id,
                                tipo_equipamento=4,
                                quantTotal=value

                            )
                            db.session.add(be)

                        db.session.commit()

        return jsonify({"mensagem": "Valore retornado!"})

    except Exception as e:
        return jsonify({
            "mensagem": "Erro não tratado!",
            "cod": str({e})
        }), 400


@valores.post("/usuarios")
def usuariosguarulhos():

    try:
        escolas = Escolas.query.all()
        senhas = []
        for escola in escolas:

            caracteres = [
                random.choice("abcdefghijklmnopqrstuvwxyz"),
                random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
                random.choice("0123456789"),
                random.choice("0123456789"),
                random.choice("0123456789"),
                random.choice("0123456789"),
                random.choice("@!#$%*"),
                random.choice("@!#$%*")
            ]

            senha = "".join(caracteres)
            senhas.append({"usuario":str(escola.id).zfill(3), "senha":senha, "escola":escola.nome})
            
            usuario = Usuarios(
                nome=escola.nome,
                # unidecode("".join(escola.nome.split(" ")[1:]).lower()),
                email=str(escola.id).zfill(3),
                escola=escola.id,
                senha=generate_password_hash(senha),
                cod_cliente=1
            )

            db.session.add(usuario)
            db.session.commit()

        usuarios = Usuarios.query.all()              
       
        senhas_df = pd.DataFrame(senhas)
        senhas_df.to_csv("senhas.csv", sep=";")
        
        return jsonify({
            "Usuarios": [usuario.to_json() for usuario in usuarios]
        })

    except Exception as e:
        return jsonify({
            "erro": "Erro não tratado",
            "codigo": str(e)
        })
