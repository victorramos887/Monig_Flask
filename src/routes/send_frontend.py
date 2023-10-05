from flask import Blueprint, json, jsonify, request, render_template, current_app
from ..constants.http_status_codes import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED)
from sqlalchemy import func, select, desc
from ..models import db, Escolas, Edificios, Reservatorios, AreaUmida, AuxTipoDeEventos, AuxTiposEquipamentos, Eventos, EscolaNiveis, Equipamentos, Populacao, AreaUmida, Hidrometros, AuxOpNiveis, AuxDeLocais

send_frontend = Blueprint('send_frontend', __name__,
                          url_prefix='/api/v1/send_frontend')

# # Verificar Historico de Deleção
# @send_frontend.get('/historico')
# def historico():

#     historico = Historico.query.all()
#     return jsonify([json.dumps(h.to_json()) for h in historico])
   
@send_frontend.get('/verificando')
def testeando():
    return "Docker Retorn"

# RETORNA TODAS AS ESCOLAS
@send_frontend.get('/escolas')
def escolas():
    # token = validacao_token(request.headers.get('Authorization'))

    escolas = Escolas.query.filter_by(status_do_registro=True).all()
    return jsonify({
        'return': [escola.to_json() for escola in escolas],
        'status': True,
        'mensagem': 'Escolas retornadas com sucesso'
    }), 200


# RETORNA APENAS UMA ESCOLA
@send_frontend.get('/escolas/<int:id>')
def get_escolas(id):
    escola = Escolas.query.filter_by(id=id).first()

    if not escola:
        return jsonify({
            "status": False,
            "mensagem": "Escola não encontrada."
        }), 404

    escola_json = escola.to_json() if escola is not None else ''

    edificio = Edificios.query.filter_by(fk_escola=id).first()
    edificio_json = edificio.to_json() if edificio is not None else None

    result = db.session.query(EscolaNiveis.escola_id, AuxOpNiveis.nivel) \
        .join(AuxOpNiveis, AuxOpNiveis.id == EscolaNiveis.nivel_ensino_id) \
        .filter(EscolaNiveis.escola_id == escola.id) \
        .all()

    nivelRetorno = [nivel for escola_id, nivel in result]

    if edificio is not None and escola is not None:
        enviar = {
            "cnpj": edificio_json["cnpj_edificio"],
            "email": escola_json["email"],
            "id": escola_json["id"],
            "nivel": nivelRetorno,
            "nome": escola_json["nome"],
            "status_do_registro": escola_json["status_do_registro"],
            "telefone": escola_json["telefone"],
            "logradouro": edificio_json["logradouro_edificio"],
            "bairro": edificio_json["bairro_edificio"],
            "numero": edificio_json["numero_edificio"],
            "complemento": edificio_json["complemento_edificio"],
            "estado": edificio_json["estado_edificio"],
            "cep": edificio_json["cep_edificio"],
            "cidade": edificio_json["cidade_edificio"]
        }
        return jsonify({
            "status": True,
            "escola": enviar,
            'mensagem': 'Escola retornada com sucesso!'
        }), 200

    # Adicione esta declaração de retorno caso a condição anterior não seja satisfeita
    return jsonify({
        "status": False,
        "mensagem": "Escola não encontrada."
    }), 404


# RETORNA TODOS OS EDIFICIOS DA ESCOLA PARA MONTAR A TABELA
@send_frontend.get('/edificios-table/<int:id>')
def edificios(id):

    edificios = Edificios.query.filter_by(
        fk_escola=id, status_do_registro=True).order_by(desc(Edificios.principal)).all()
    result = []

    for edificio in edificios:
        # População
        soma_colaboradores, soma_alunos = (
            db.session.query(
                func.sum(Populacao.funcionarios).label('soma_colaboradores'),
                func.sum(Populacao.alunos).label('soma_alunos')
            )
            .join(Edificios)
            .filter(Populacao.fk_edificios == edificio.id)
            .first()
        )
        soma_total = (soma_colaboradores or 0) + (soma_alunos or 0)

        # Area umida
        contador_area_umida = db.session.query(func.count(AreaUmida.id)).filter(
            AreaUmida.fk_edificios == edificio.id).scalar()

        # Reservatorios
        reservatorios = Reservatorios.query.filter(
            Reservatorios.fk_escola == id, Reservatorios.status_do_registro == True).all()
        info_reservatorios = [reservatorio.to_json()
                              for reservatorio in reservatorios]

        result.append({
            'id': edificio.id,
            'nome': edificio.nome_do_edificio,
            'populacao': soma_total or 0,
            'area_umida': contador_area_umida or 0,
            'principal': edificio.principal,
            'reservatorios': info_reservatorios
        })

    return jsonify({
        'edificios': result,
        'status': True,
        'mensagem': 'Edificio retornado com sucesso!'
    })


# RETORNA APENAS O EDIFICIO QUE DESEJA ATUALIZAR
@send_frontend.get('/edificio/<int:id>')
def edificio(id):

    edificio = Edificios.query.filter_by(
        id=id, status_do_registro=True).first()
    reservatorios = Reservatorios.query.filter(
        Reservatorios.fk_escola == id, Reservatorios.status_do_registro == True).all()

    if edificio is None:

        edificios_erro = Edificios.query.filter_by(
            id=id, status_do_registro=False
        ).first()

        if edificios_erro:

            return jsonify({'erro': 'Edificio não encontrado',  "status": False, "erro_edificio":edificios_erro.to_json()}), HTTP_400_BAD_REQUEST
        
        return jsonify({'erro': 'Edificio não encontrado',  "status": False}), HTTP_400_BAD_REQUEST

    return jsonify({
        "edificio": edificio.to_json(), "status": True
    }), HTTP_200_OK


# TODAS AREA UMIDAS
@send_frontend.get('/area_umidas_table/<int:id>')
def area_umidas(id):
    # fk_edificios = request.args.get('')
    areas_umidas = AreaUmida.query.filter_by(
        fk_edificios=id, status_do_registro=True).all()
    result = list()
    for area_umida in areas_umidas:
        # População
        total = (
            db.session.query(
                func.sum(Equipamentos.quantTotal).label('total'),
            )
            .join(AreaUmida)
            .filter(Equipamentos.fk_area_umida == area_umida.id)
            .first()
        )

        result.append({
            'id': area_umida.id,
            'tipo_area_umida': area_umida.tipo_area_umida_rel.tipo,
            'quant_equipamentos': total.total or 0 if total else 0,
            "status": "Aberto" if area_umida.status_area_umida else "Fechado"
        })

    return jsonify({'area_umidas': result, "status": True})

# RETORNA APENAS UMA


@send_frontend.get('/area_umida/<int:id>')
def get_area_umida(id):
    area_umida = AreaUmida.query.filter_by(id=id, status_do_registro=True).first()

    if not area_umida:

        erro_area_umida = AreaUmida.query.filter_by(id=id, status_do_registro = False).first()

        if erro_area_umida:
            return jsonify({'erro': 'Area umida não encontrado',  "status": False, "erro_area_umida":erro_area_umida.to_json()}), HTTP_400_BAD_REQUEST
        
        return jsonify({'erro': 'Area umida não encontrado',  "status": False}), HTTP_400_BAD_REQUEST
    
    return jsonify({'area_umida': area_umida.to_json() if area_umida is not None else area_umida, "status": True})

# TODOS OS EQUIPAMENTOS


@send_frontend.get('/equipamentos-table/<int:id>')
def equipamentos(id):

    equipamentos = Equipamentos.query.filter_by(
        fk_area_umida=id, status_do_registro=True).all()

    return jsonify({
        f'equipamentos': [equipamento.to_json() for equipamento in equipamentos], "status": True
    })

# RETORNA APENAS UM


@send_frontend.get('/equipamento/<int:id>')
def get_equipamento(id):
    equipamento = Equipamentos.query.filter_by(id=id, status_do_registro=True).first()

    if not equipamento:

        erro_equipamento = Equipamentos.query.filter_by(id=id, status_do_registro=False).first()

        if erro_equipamento:
            return jsonify({
                'erro':'Equipamento não encontrado',
                'status':False,
                'erro_equipamento':erro_equipamento.to_json()
            }), HTTP_400_BAD_REQUEST

        return jsonify({
            {'erro': 'Equipamento não encontrado',  "status": False}
        }), HTTP_400_BAD_REQUEST

    return jsonify({'equipamento': equipamento.to_json() if equipamento is not None else equipamento, "status": True}), 200


# TODAS AS POPULAÇÕES
@send_frontend.get('/populacao-table/<int:id>')
def populacao(id):
    populacoes = Populacao.query.filter_by(
        fk_edificios=id, status_do_registro=True).all()
    
    return jsonify({
        "populacao": [populacao.to_json() for populacao in populacoes],
        "status": True
    })

# RETORNA APENAS UMA
@send_frontend.get('/populacao/<int:id>')
def get_populacao(id):

    populacao = Populacao.query.filter_by(id=id, status_do_registro=True).first()

    if not populacao:

        erro_populacao = Populacao.query.filter_by(id=id, status_do_registro=False).first()

        if erro_populacao:
            return jsonify({'erro': 'População não encontrado',  "status": False, "erro_populacao":erro_populacao.to_json()}), HTTP_400_BAD_REQUEST

        return jsonify({
            'erro': 'Populacao não encontrado',  "status": False
        }), HTTP_400_BAD_REQUEST

    return jsonify({'populacao': populacao.to_json() if populacao is not None else populacao, "status": True})


# TODOS OS HIDROMETROS
@send_frontend.get('/hidrometros-table/<int:id>')
def hidrometro(id):
    hidrometros = Hidrometros.query.filter_by(
        fk_edificios=id, status_do_registro=True).all()
    
    if not hidrometros:
        return jsonify({
            'erro':'Hidrometro não encontrado',
            'status':False
        }), HTTP_400_BAD_REQUEST

    return jsonify({
        "hidrometro": [hidrometro.to_json() for hidrometro in hidrometros], "status": True
    })

# RETORNA APENAS UM


@send_frontend.get('/hidrometro/<int:id>')
def get_hidrometro(id):
    hidrometro = Hidrometros.query.filter_by(id=id).first()
    
    if not hidrometro:

        erro_hidrometro = Populacao.query.filter_by(id=id, status_do_registro=False).first()

        if erro_hidrometro:

            return jsonify({
                'erro': 'Hidrometro não encontrado',  "status": False, "erro_hidrometro":erro_hidrometro.to_json()
            }), HTTP_400_BAD_REQUEST
        return jsonify({
            'erro': 'Hidrometro não encontrado',  "status": False
        }), HTTP_400_BAD_REQUEST
    
    return jsonify({'hidrometro': hidrometro.to_json() if hidrometro is not None else hidrometro, "status": True})


@send_frontend.get('/reservatorio/<int:id>')
def get_reservatorio(id):

    reservatorio = Reservatorios.query.filter_by(
        id=id, status_do_registro=True
    ).first()

    return jsonify({
        'reservatorio': reservatorio.to_json() if reservatorio is not None else reservatorio, "status": True
    })

# TODOS OS RESERVATÓRIOS


@send_frontend.get('/reservatorios-table/<int:id>')
def reservatorios(id):
    reservatorios = Reservatorios.query.filter_by(
        fk_escola=id, status_do_registro=True).all()
    return jsonify({
        "reservatorios": [reservatorio.to_json() for reservatorio in reservatorios], "status": True
    })


@send_frontend.get('/tipo-de-eventos/<int:id>')
def tipo_de_eventos(id):  
   
    tipo_de_eventos = AuxTipoDeEventos.query.filter_by(
        recorrente = True if id == 1 else False
    ).all()

    return jsonify({
        "tipo_de_eventos":[
            tipo_de_evento.to_json() for tipo_de_evento in tipo_de_eventos
        ],
        "status":True
    }), 200


@send_frontend.get('/tipo-de-evento/<int:id>')
def get_tipo_de_eventos(id):

    tipo_de_evento = AuxTipoDeEventos.query.filter_by(
        id=id
    ).first()

    if tipo_de_evento is not None:
        return jsonify({
            'tipo_de_evento': tipo_de_evento.to_json(),
            "status":True
        })

    else:
        return jsonify({
            'message': 'Tipo de evento não encontrado'
        }), 404


@send_frontend.get('/eventos')
def get_eventos():

    eventos = Eventos.query.all()
    
    return jsonify({
            "eventos":[
                evento.retornoFullCalendar() for evento in eventos
            ],
            "status":True
        }), 200


@send_frontend.get('/evento/<int:id>')
def get_evento(id):

    evento = Eventos.query.filter_by(
        id=id
    ).first()
    print(evento)
    
    if evento is not None:
        return jsonify({'status':True, "mensagem":"Retorno de evento.","data":evento.to_json()}), HTTP_200_OK
    else:
        return jsonify({
            'message': 'Evento não encontrado'
        }), 404
        
        

@send_frontend.get('/eventos-tipo/<int:recorrente>')
def get_tipos_recorrente_ocasional(recorrente):

        #ocasional
        if recorrente == 0:
            tipo_ocasional = AuxTipoDeEventos.query.filter_by(
                recorrente=False
            ).all()
            
            return jsonify({
            "tipo_ocasional":[
                {"nome":tipo.nome_do_tipo_de_evento, "id":tipo.id} for tipo in tipo_ocasional
            ],
                "status":True
            }), 200

 
        if recorrente == 1:
            tipo_recorrente = AuxTipoDeEventos.query.filter_by(
                recorrente=True
            ).all()
            
            return jsonify({
            "tipo_recorrente":[
                {"nome":tipo.nome_do_tipo_de_evento, "id":tipo.id} for tipo in tipo_recorrente
            ],
                "status":True
            }), 200
            
        else:
            return jsonify({
            'message': 'verifique o valor informado'
        }), 404
           

        
#retorno tipo_de_local
@send_frontend.get('/tipo-de-local')
def get_tipo_local():

            tipo_local = AuxDeLocais.query.all()
            
            return jsonify({
            "tipo_de_local":[
                {"id":local.id, "nome":local.nome_da_tabela } for local in tipo_local
            ],
                "status":True
            }), 200
            
        
        
@send_frontend.get('/local/<string:tipo>')
def get_local(tipo):
    
    #filtrar o tipo
    tipo_local = AuxDeLocais.query.filter_by(nome_da_tabela=tipo).first() 

    if tipo_local is None:
         return jsonify({
             "message": "Tipo de local não encontrado",
             "status": False
         }), 400
         
    tabela = tipo_local.nome_da_tabela
    
    tabelas = {
        'Escola': Escolas,
        'Edificação': Edificios,
        'Área Úmida': AreaUmida,
        'Reservatório': Reservatorios,
        'Equipamento': Equipamentos,
        'Hidrômetro': Hidrometros
    }
        
    modelo = tabelas.get(tabela) 
    
    if modelo == Escolas:
        tabela = modelo.query.with_entities(Escolas.id, Escolas.nome).all()
    elif modelo == Edificios:
        tabela = modelo.query.with_entities(Edificios.id, Edificios.nome_do_edificio).all()
    elif modelo == AreaUmida:
        tabela = modelo.query.with_entities(AreaUmida.id, AreaUmida.nome_area_umida).all()
    elif modelo == Reservatorios:
        tabela = modelo.query.with_entities(Reservatorios.id, Reservatorios.nome_do_reservatorio).all()
    elif modelo == Equipamentos:
        tabela = modelo.query.with_entities(AuxTiposEquipamentos.id, AuxTiposEquipamentos.aparelho_sanitario).all()
    elif modelo == Hidrometros:
        tabela = modelo.query.with_entities(Hidrometros.id, Hidrometros.hidrometro).all()
        
    else:
         return jsonify({
             "message": "Tabela não encontrada",
             "status": False
         }), 400
        
    
    return jsonify({
    "local": [
        {"id": l[0], "nome": l[1]} for l in tabela
    ],
        "status":True
    }), 200