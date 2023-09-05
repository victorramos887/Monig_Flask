from flask import Blueprint, jsonify, request
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_506_VARIANT_ALSO_NEGOTIATES, HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED,HTTP_500_INTERNAL_SERVER_ERROR
from ..models import ( Escolas, Edificios, db, AreaUmida, Equipamentos, Populacao, Hidrometros, Reservatorios, Cliente,
                       Usuarios, TipoAreaUmida, TiposEquipamentos, OpNiveis, PopulacaoPeriodo, EscolaNiveis, ReservatorioEdificio, TipoDeEventos, Eventos)
from sqlalchemy import exc
from werkzeug.exceptions import HTTPException
import re

editar = Blueprint('editar', __name__, url_prefix='/api/v1/editar')


# EDITAR Cliente
@editar.put('/cliente/<id>')
def cliente_editar(id):
    cliente = Cliente.query.filter_by(id=id).first()
    body = request.get_json()

    if not cliente:
        return jsonify({'mensagem': 'cliente não encontrado', "status": False}), 404

    try:
        cliente.update(**body)

        db.session.commit()

        return jsonify({"cliente": cliente.to_json(), "status": True}), HTTP_200_OK
    except exc.DBAPIError as e:
        if e.orig.pgcode == '23503':
            match = re.search(
                r'ERROR:  insert or update on table "(.*?)" violates foreign key constraint "(.*?)".*', str(e))
            tabela = match.group(1) if match else 'tabela desconhecida'
            coluna = match.group(2) if match else 'coluna desconhecida'
            mensagem = f"A operação não pôde ser concluída devido a uma violação de chave estrangeira na tabela '{tabela}', coluna '{coluna}'. Por favor, verifique os valores informados e tente novamente."
            return jsonify({'codigo': str(e), 'status': False, 'mensagem': mensagem}), HTTP_409_CONFLICT

        if e.orig.pgcode == '23505':
            # UNIQUE VIOLATION
            match = re.search(r'Key \((.*?)\)=', str(e))
            campo = match.group(1) if match else 'campo desconhecido'
            mensagem = f"Já existe um registro com o valor informado no campo '{campo}'. Por favor, corrija o valor e tente novamente."
            return jsonify({'status': False, 'mensagem': mensagem, 'código': str(e)}), HTTP_401_UNAUTHORIZED

        if e.orig.pgcode == '01004':
            # STRING DATA RIGHT TRUNCATION
            return jsonify({'status': False, 'mensagem': "Erro no cabeçalho", 'codigo': f'{e}'}), HTTP_506_VARIANT_ALSO_NEGOTIATES

    except Exception as e:
        if isinstance(e, HTTPException) and e.code == 500:
            return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

        if isinstance(e, HTTPException) and e.code == 400:
            # flash("Erro, 4 não salva")
            return jsonify({'status': False, 'mensagem': 'Erro na requisição', 'codigo': str(e)}), HTTP_400_BAD_REQUEST


# EDITAR usuario
@editar.put('/usuario/<id>')
def usuario_editar(id):
    usuario = Usuarios.query.filter_by(id=id).first()
    body = request.get_json()

    if not usuario:
        return jsonify({'mensagem': 'usuario não encontrado', "status": False}), 404

    try:
        usuario.update(**body)

        db.session.commit()

        return jsonify({"usuario": usuario.to_json(), "status": True}), HTTP_200_OK
    except exc.DBAPIError as e:
        if e.orig.pgcode == '23503':
            match = re.search(
                r'ERROR:  insert or update on table "(.*?)" violates foreign key constraint "(.*?)".*', str(e))
            tabela = match.group(1) if match else 'tabela desconhecida'
            coluna = match.group(2) if match else 'coluna desconhecida'
            mensagem = f"A operação não pôde ser concluída devido a uma violação de chave estrangeira na tabela '{tabela}', coluna '{coluna}'. Por favor, verifique os valores informados e tente novamente."
            return jsonify({ 'codigo': str(e), 'status': False, 'mensagem': mensagem}), HTTP_409_CONFLICT

        if e.orig.pgcode == '23505':
            # UNIQUE VIOLATION
            match = re.search(r'Key \((.*?)\)=', str(e))
            campo = match.group(1) if match else 'campo desconhecido'
            mensagem = f"Já existe um registro com o valor informado no campo '{campo}'. Por favor, corrija o valor e tente novamente."
            return jsonify({'status': False, 'mensagem': mensagem, 'código': str(e)}), HTTP_401_UNAUTHORIZED

        if e.orig.pgcode == '01004':
            #STRING DATA RIGHT TRUNCATION
            return jsonify({'status':False, 'mensagem': "Erro no cabeçalho", 'codigo':f'{e}'}), HTTP_506_VARIANT_ALSO_NEGOTIATES

    except Exception as e:
        if isinstance(e, HTTPException) and e.code == 500:
            return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

        if isinstance(e, HTTPException) and e.code == 400:
            # flash("Erro, 4 não salva")
            return jsonify({'status': False, 'mensagem': 'Erro na requisição', 'codigo': str(e)}), HTTP_400_BAD_REQUEST


# EDITAR ESCOLA
@editar.put('/escolas/<id>')
def escolas_editar(id):
    escola = Escolas.query.filter_by(id=id).first()
    edificio = Edificios.query.filter_by(fk_escola=id).first()

    # VERIFICAR O QUE FOI ALTERADO
    body = request.get_json()

    if not escola:
        return jsonify({'mensagem': 'Escola não encontrado', "status": False}), 404

    try:

        escola_json = escola.to_json()
        escola_json['data_criacao'] = escola_json['data_criacao'].strftime('%m/%d/%Y %H:%M:%S')
        historico_escola = Historico(tabela="Escola", dados=escola_json)
        db.session.add(historico_escola)

        edificio_json = edificio.to_json()
        edificio_json['data_criacao'] = edificio_json['data_criacao'].strftime('%m/%d/%Y %H:%M:%S')
        historico_edificio = Historico(tabela="Edificio", dados=edificio_json)
        db.session.add(historico_edificio)

       #verificando niveis das escolas
        escola_niveis = EscolaNiveis.query.filter_by(escola_id=id).all()

        escola.update(
            nome=body["nome"],
            cnpj=body["cnpj"],
            email=body["email"],
            telefone=body["telefone"]
        )

        niveis=body["nivel"]
        
        niveis = [OpNiveis.query.filter_by(nivel=nivel).first().id for nivel in niveis]

        # Obtenha todos os níveis de ensino associados à escola
        niveis_atuais = [n.nivel_ensino_id for n in escola_niveis]

        # Determine os níveis a serem adicionados e removidos
        niveis_adicionados = set(niveis) - set(niveis_atuais)
        niveis_removidos = set(niveis_atuais) - set(niveis)

        for nivel in niveis_adicionados:
            op_nivel = OpNiveis.query.filter_by(id=nivel).first()
                
            if op_nivel:
                escola_nivel = EscolaNiveis(
                    escola_id=escola.id,
                    nivel_ensino_id=op_nivel.id
                )
                
                db.session.add(escola_nivel)

        # Remova os níveis de ensino que não estão mais presentes
        for nivel in niveis_removidos:
            op_nivel = OpNiveis.query.filter_by(id=nivel).first()
            if op_nivel:
                escola_nivel = EscolaNiveis.query.filter_by(
                    escola_id=escola.id,
                    nivel_ensino_id=op_nivel.id
                ).first()
                if escola_nivel:
                    db.session.delete(escola_nivel)
        edificio.update(
            numero_edificio=body["numero"],
            cep_edificio=body["cep"],
            cidade_edificio=body["cidade"],
            estado_edificio=body["estado"],
            cnpj_edificio=body["cnpj"],
            logradouro_edificio=body["logradouro"],
            complemento=body["complemento"]
        )

        db.session.commit()

        return jsonify({"escola": escola.to_json(), "status": True}), HTTP_200_OK
    
    except exc.DBAPIError as e:
        if '23503' in str(e):
            match = re.search(
                r'ERROR:  insert or update on table "(.*?)" violates foreign key constraint "(.*?)".*', str(e))
            tabela = match.group(1) if match else 'tabela desconhecida'
            coluna = match.group(2) if match else 'coluna desconhecida'
            mensagem = f"A operação não pôde ser concluída devido a uma violação de chave estrangeira na tabela '{tabela}', coluna '{coluna}'. Por favor, verifique os valores informados e tente novamente."
            return jsonify({'codigo': str(e), 'status': False, 'mensagem': mensagem}), HTTP_409_CONFLICT

        # if e.orig.pgcode == '23505':
        if '23505' in str(e):
            # UNIQUE VIOLATION
            match = re.search(r'Key \((.*?)\)=', str(e))
            campo = match.group(1) if match else 'campo desconhecido'
            mensagem = f"Já existe um registro com o valor informado no campo '{campo}'. Por favor, corrija o valor e tente novamente."
            return jsonify({'status': False, 'mensagem': mensagem, 'código': str(e)}), HTTP_401_UNAUTHORIZED

        #if e.orig.pgcode == '01004':
        if '01004' in str(e):
            #STRING DATA RIGHT TRUNCATION
            return jsonify({'status':False, 'mensagem': "Erro no cabeçalho", 'codigo':f'{e}'}), HTTP_506_VARIANT_ALSO_NEGOTIATES

        return jsonify({'status':False, 'mensagem': "Erro não tratado", 'codigo':f'{e}'}), HTTP_400_BAD_REQUEST

    except Exception as e:
        if isinstance(e, HTTPException) and e.code == 500:
            return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

        if isinstance(e, HTTPException) and e.code == 400:
            # flash("Erro, 4 não salva")
            return jsonify({'status': False, 'mensagem': 'Erro na requisição', 'codigo': str(e)}), HTTP_400_BAD_REQUEST

        return jsonify({
            "status":False,"mensagem":"Erro não tratado", "codigo":e
        }), HTTP_400_BAD_REQUEST


# EDITAR RESERVATORIOS
@editar.put('/reservatorios/<id>')
def reservatorio_editar(id):
    reservatorio = Reservatorios.query.filter_by(id=id).first()
    body = request.get_json()

    if not reservatorio:
        return jsonify({'mensagem': 'reservatorio não encontrado', "status": False}), 404

    try:
        reservatorio_json = reservatorio.to_json()
        reservatorio_json['data_criacao'] = reservatorio_json['data_criacao'].strftime('%m/%d/%Y %H:%M:%S')
        historico_reservatorio = Historico(tabela="Reservatorio", dados=reservatorio_json)
        db.session.add(historico_reservatorio)
    
        reservatorio.update(
            nome_do_reservatorio=body['nome']
        )

        db.session.commit()

        return jsonify({"Reservatorio": reservatorio.to_json(), "status": True}), HTTP_200_OK
    except exc.DBAPIError as e:
        if e.orig.pgcode == '23503':
            match = re.search(
                r'ERROR:  insert or update on table "(.*?)" violates foreign key constraint "(.*?)".*', str(e))
            tabela = match.group(1) if match else 'tabela desconhecida'
            coluna = match.group(2) if match else 'coluna desconhecida'
            mensagem = f"A operação não pôde ser concluída devido a uma violação de chave estrangeira na tabela '{tabela}', coluna '{coluna}'. Por favor, verifique os valores informados e tente novamente."
            return jsonify({'codigo': str(e), 'status': False, 'mensagem': mensagem}), HTTP_409_CONFLICT

        if e.orig.pgcode == '23505':
            # UNIQUE VIOLATION
            match = re.search(r'Key \((.*?)\)=', str(e))
            campo = match.group(1) if match else 'campo desconhecido'
            mensagem = f"Já existe um registro com o valor informado no campo '{campo}'. Por favor, corrija o valor e tente novamente."
            return jsonify({'status': False, 'mensagem': mensagem, 'código': str(e)}), HTTP_401_UNAUTHORIZED

        if e.orig.pgcode == '01004':
            # STRING DATA RIGHT TRUNCATION
            return jsonify({'status': False, 'mensagem': "Erro no cabeçalho", 'codigo': f'{e}'}), HTTP_506_VARIANT_ALSO_NEGOTIATES

    except Exception as e:
        if isinstance(e, HTTPException) and e.code == 500:
            return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

        if isinstance(e, HTTPException) and e.code == 400:
            # flash("Erro, 4 não salva")
            return jsonify({'status': False, 'mensagem': 'Erro na requisição', 'codigo': str(e)}), HTTP_400_BAD_REQUEST

        return jsonify({
            "status":False,"mensagem":"Erro não tratado", "codigo":e
        }), HTTP_400_BAD_REQUEST


# EDITAR EDIFICIOS
@editar.put('/edificios/<id>')
def edificios_editar(id):
    edificio = Edificios.query.filter_by(id=id).first()
    print(edificio)
    body = request.get_json()

    reservatorios = body.pop('reservatorio')

    if not edificio:
        return jsonify({'mensagem': 'Edificio não encontrado', "status": False}), 404

    try:

        edificio_json = edificio.to_json()
        edificio_json['data_criacao'] = edificio_json['data_criacao'].strftime('%m/%d/%Y %H:%M:%S')
        historico_edificio = Historico(tabela="Edificio", dados=edificio_json)
        db.session.add(historico_edificio)
    
        EdificioRes = ReservatorioEdificio.query.filter_by(edificio_id=id)

        reservatorios = [Reservatorios.query.filter_by(nome_do_reservatorio=reservatorio).first().id for reservatorio in reservatorios if reservatorio is not None]
        edificio.update(**body)


        reservatorioatual = [n.reservatorio_id for n in EdificioRes]
        
        reservatorio_adicionado = set(reservatorios) - set(reservatorioatual)
        reservatorio_remover = set(reservatorioatual) - set(reservatorios)
        for reservatorio in reservatorio_adicionado:
            reservatorios_edificios = Reservatorios.query.filter_by(id=reservatorio).first()

            if reservatorios_edificios:

                edificios_reservatorio = ReservatorioEdificio(
                    edificio_id=id,
                    reservatorio_id=reservatorios_edificios.id
                )
                print(reservatorio)
                db.session.add(edificios_reservatorio)

        for reservatorio in reservatorio_remover:
            reservatorios_edificios = Reservatorios.query.filter_by(id=reservatorio).first()

            if reservatorios_edificios:

                edificios_reservatorio = ReservatorioEdificio.query.filter_by(
                    edificio_id=id,
                    reservatorio_id=reservatorios_edificios.id         
                ).first()
                if edificios_reservatorio:
                    db.session.delete(edificios_reservatorio)
  

        db.session.commit()

        return jsonify({"edificio": edificio.to_json(), "status": True}), HTTP_200_OK
    except exc.DBAPIError as e:
        if e.orig.pgcode == '23503':
            match = re.search(
                r'ERROR:  insert or update on table "(.*?)" violates foreign key constraint "(.*?)".*', str(e))
            tabela = match.group(1) if match else 'tabela desconhecida'
            coluna = match.group(2) if match else 'coluna desconhecida'
            mensagem = f"A operação não pôde ser concluída devido a uma violação de chave estrangeira na tabela '{tabela}', coluna '{coluna}'. Por favor, verifique os valores informados e tente novamente."
            return jsonify({'codigo': str(e), 'status': False, 'mensagem': mensagem}), HTTP_409_CONFLICT

        if e.orig.pgcode == '23505':
            # UNIQUE VIOLATION
            match = re.search(r'Key \((.*?)\)=', str(e))
            campo = match.group(1) if match else 'campo desconhecido'
            mensagem = f"Já existe um registro com o valor informado no campo '{campo}'. Por favor, corrija o valor e tente novamente."
            return jsonify({'status': False, 'mensagem': mensagem, 'código': str(e)}), HTTP_401_UNAUTHORIZED

        if e.orig.pgcode == '01004':
            # STRING DATA RIGHT TRUNCATION
            return jsonify({'status': False, 'mensagem': "Erro no cabeçalho", 'codigo': f'{e}'}), HTTP_506_VARIANT_ALSO_NEGOTIATES

        return jsonify({'status': False, 'mensagem': "Erro não tratado", 'codigo': f'{e}'}), HTTP_400_BAD_REQUEST
    
    except Exception as e:
        if isinstance(e, HTTPException) and e.code == 500:
            return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

        if isinstance(e, HTTPException) and e.code == 400:
            # flash("Erro, 4 não salva")
            return jsonify({'status': False, 'mensagem': 'Erro na requisição', 'codigo': str(e)}), HTTP_400_BAD_REQUEST
        
        return jsonify({'status': False, 'mensagem': 'Erro não tratado', 'codigo': str(e)}), HTTP_400_BAD_REQUEST

# EDITAR HIDROMETRO

@editar.put('/edificio-principal/<int:id>')
def edificio_principal(id):

    edificio = Edificios.query.filter_by(id=id).first()


    if not edificio:
        return jsonify({
            'mensagem':'Edificio não encontrado', 'status':False
        }), 404

    try:
        edificio_json = edificio.to_json()
        edificio_json['data_criacao'] = edificio_json['data_criacao'].strftime('%m/%d/%Y %H:%M:%S')
        historico_edificio = Historico(tabela="Edificio", dados=edificio_json)
        db.session.add(historico_edificio)

        edificio.update_principal()
        db.session.commit()

        return jsonify({
            'mensagem': 'Alteração realizada com sucesso',
            'status':True
        }), 200

    except Exception as e:

        print(e)
        db.session.rollback()
        return jsonify({
            'mensagem':'Erro não tratado',
            'codigo':str(e),
            'status':False
        }), 404



@editar.put('/hidrometros/<id>')
def hidrometro_editar(id):
    hidrometro = Hidrometros.query.filter_by(id=id).first()
    body = request.get_json()

    if not hidrometro:
        return jsonify({'mensagem': 'Hidrometro não encontrado', "status": False}), 404
    
    try:
        hidrometro_json = hidrometro.to_json()
        hidrometro_json['data_criacao'] = hidrometro_json['data_criacao'].strftime('%m/%d/%Y %H:%M:%S')
        historico_hidrometro = Historico(tabela="hidrometro", dados=hidrometro_json)
        db.session.add(historico_hidrometro)
    
        hidrometro.update(**body)

        db.session.commit()

        return jsonify({"hidrometro": hidrometro.to_json(), "status": True}), HTTP_200_OK
    except exc.DBAPIError as e:
        db.session.rollback()
        if e.orig.pgcode == '23503':
            match = re.search(
                r'ERROR:  insert or update on table "(.*?)" violates foreign key constraint "(.*?)".*', str(e))
            tabela = match.group(1) if match else 'tabela desconhecida'
            coluna = match.group(2) if match else 'coluna desconhecida'
            mensagem = f"A operação não pôde ser concluída devido a uma violação de chave estrangeira na tabela '{tabela}', coluna '{coluna}'. Por favor, verifique os valores informados e tente novamente."
            return jsonify({'codigo': str(e), 'status': False, 'mensagem': mensagem}), HTTP_409_CONFLICT
        if e.orig.pgcode == '23505':
            # UNIQUE VIOLATION
            match = re.search(r'Key \((.*?)\)=', str(e))
            campo = match.group(1) if match else 'campo desconhecido'
            mensagem = f"Já existe um registro com o valor informado no campo '{campo}'. Por favor, corrija o valor e tente novamente."
            return jsonify({'status': False, 'mensagem': mensagem, 'código': str(e)}), HTTP_401_UNAUTHORIZED

        if e.orig.pgcode == '01004':
            # STRING DATA RIGHT TRUNCATION
            return jsonify({'status': False, 'mensagem': "Erro no cabeçalho", 'codigo': f'{e}'}), HTTP_506_VARIANT_ALSO_NEGOTIATES

    except Exception as e:
        if isinstance(e, HTTPException) and e.code == 500:
            return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

        if isinstance(e, HTTPException) and e.code == 400:
            # flash("Erro, 4 não salva")
            return jsonify({'status': False, 'mensagem': 'Erro na requisição', 'codigo': str(e)}), HTTP_400_BAD_REQUEST


# EDITAR POPULACAO
@editar.put('/populacao/<id>')
def populacao_editar(id):
    populacao = Populacao.query.filter_by(id=id).first()
    body = request.get_json()

    if not populacao:
        return jsonify({'mensagem': 'Populacao não encontrado', "status": False}), 404

    try:
        populacao_json = populacao.to_json()
        populacao_json['data_criacao'] = populacao_json['data_criacao'].strftime('%m/%d/%Y %H:%M:%S')
        historico_populacao = Historico(tabela="populacao", dados=populacao_json)
        db.session.add(historico_populacao)
    
        print(body)
        alunos = body['alunos']
        fk_edificios = body['fk_edificios']
        funcionarios = body['funcionarios']
        nivel = OpNiveis.query.filter_by(nivel=body['nivel']).first()
        periodo = PopulacaoPeriodo.query.filter_by(
            periodo=body['periodo']).first()

        print(periodo.id)
        populacao.update(
            alunos=alunos,
            fk_edificios=fk_edificios,
            funcionarios=funcionarios,
            fk_niveis=nivel.id,
            fk_periodo=periodo.id
        )

        db.session.commit()

        return jsonify({"populacao": populacao.to_json(), "status": True}), HTTP_200_OK

    except exc.DBAPIError as e:

        if e.orig.pgcode == '23503':
            match = re.search(
                r'ERROR:  insert or update on table "(.*?)" violates foreign key constraint "(.*?)".*', str(e))
            tabela = match.group(1) if match else 'tabela desconhecida'
            coluna = match.group(2) if match else 'coluna desconhecida'
            mensagem = f"A operação não pôde ser concluída devido a uma violação de chave estrangeira na tabela '{tabela}', coluna '{coluna}'. Por favor, verifique os valores informados e tente novamente."
            return jsonify({'codigo': str(e), 'status': False, 'mensagem': mensagem}), HTTP_409_CONFLICT

        if e.orig.pgcode == '23505':
            # UNIQUE VIOLATION
            match = re.search(r'Key \((.*?)\)=', str(e))
            campo = match.group(1) if match else 'campo desconhecido'
            mensagem = f"Já existe um registro com o valor informado no campo '{campo}'. Por favor, corrija o valor e tente novamente."
            return jsonify({'status': False, 'mensagem': mensagem, 'código': str(e)}), HTTP_401_UNAUTHORIZED

        if e.orig.pgcode == '01004':
            # STRING DATA RIGHT TRUNCATION
            return jsonify({'status': False, 'mensagem': "Erro no cabeçalho", 'codigo': f'{e}'}), HTTP_506_VARIANT_ALSO_NEGOTIATES

        return jsonify({'status': False, 'mensagem': "Erro não tratado", 'codigo': f'{e}'}), HTTP_500_INTERNAL_SERVER_ERROR

    except Exception as e:
        if isinstance(e, HTTPException) and e.code == 500:
            return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

        if isinstance(e, HTTPException) and e.code == 400:
            # flash("Erro, 4 não salva")
            return jsonify({'status': False, 'mensagem': 'Erro na requisição', 'codigo': str(e)}), HTTP_400_BAD_REQUEST

        return jsonify({'status': False, 'mensagem': 'Erro não tratado', 'codigo': str(e)}), HTTP_400_BAD_REQUEST

# EDITAR AREA UMIDA
@editar.put('/area-umida/<id>')
def area_umida_editar(id):
    umida = AreaUmida.query.filter_by(id=id).first()
    body = request.get_json()

    #print(umida.to_json())
    if not umida or umida is None:
        return jsonify({'mensagem': 'Area Umida não encontrado', "status": False}), 404

    try:
        umida_json =umida.to_json()
        umida_json['data_criacao'] =umida_json['data_criacao'].strftime('%m/%d/%Y %H:%M:%S')
        historico_umida = Historico(tabela="Area-umida", dados=umida_json)
        db.session.add(historico_umida)
    
        fk_edificios = body['fk_edificios']
        localizacao_area_umida = body['localizacao_area_umida']
        nome_area_umida = body['nome_area_umida']
        status = body['status_area_umida']

        if status == 'Aberto':
            status = True
        else:
            status = False

        tipo_area_umida = TipoAreaUmida.query.filter_by(
            tipo=body['tipo_area_umida']).first()

        umida.update(
            tipo_area_umida=tipo_area_umida.id,
            status_area_umida=status,
            nome_area_umida=nome_area_umida,
            localizacao_area_umida=localizacao_area_umida,
            fk_edificios=fk_edificios
        )

        db.session.commit()

        return jsonify({"areaumida": umida.to_json(), "status": True, 'mensagem': "Atualizado com sucesso"}), HTTP_200_OK

    except exc.DBAPIError as e:

        if e.orig.pgcode == '23503':
            match = re.search(
                r'ERROR:  insert or update on table "(.*?)" violates foreign key constraint "(.*?)".*', str(e))
            tabela = match.group(1) if match else 'tabela desconhecida'
            coluna = match.group(2) if match else 'coluna desconhecida'
            mensagem = f"A operação não pôde ser concluída devido a uma violação de chave estrangeira na tabela '{tabela}', coluna '{coluna}'. Por favor, verifique os valores informados e tente novamente."
            return jsonify({'codigo': str(e), 'status': False, 'mensagem': mensagem}), HTTP_409_CONFLICT

        if e.orig.pgcode == '23505':
            # UNIQUE VIOLATION
            match = re.search(r'Key \((.*?)\)=', str(e))
            campo = match.group(1) if match else 'campo desconhecido'
            mensagem = f"Já existe um registro com o valor informado no campo '{campo}'. Por favor, corrija o valor e tente novamente."
            return jsonify({'status': False, 'mensagem': mensagem, 'código': str(e)}), HTTP_401_UNAUTHORIZED

        if e.orig.pgcode == '01004':
            # STRING DATA RIGHT TRUNCATION
            return jsonify({'status': False, 'mensagem': "Erro no cabeçalho", 'codigo': f'{e}'}), HTTP_506_VARIANT_ALSO_NEGOTIATES

        return jsonify({'status': False, 'mensagem': "Erro não tratado 122", 'codigo': f'{e}'}), 400

    except Exception as e:
        if isinstance(e, HTTPException) and e.code == 500:
            return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

        if isinstance(e, HTTPException) and e.code == 400:
            # flash("Erro, 4 não salva")
            return jsonify({'status': False, 'mensagem': 'Erro na requisição', 'codigo': str(e)}), HTTP_400_BAD_REQUEST

        return jsonify({
            'status': False,
            'mensagem': 'Erro não tratado ',
            'codigo': str(e)
        }), HTTP_400_BAD_REQUEST


# EDITAR EQUIPAMENTO
@editar.put('/equipamentos/<id>')
def equipamento_editar(id):
    equipamento = Equipamentos.query.filter_by(id=id).first()
    body = request.get_json()

    if not equipamento:
        return jsonify({'mensagem': 'Equipamento não encontrado', "status": False}), 404
    try:

        equipamento_json = equipamento.to_json()
        equipamento_json['data_criacao'] = equipamento_json['data_criacao'].strftime('%m/%d/%Y %H:%M:%S')
        historico_equipamento = Historico(tabela="equipamento", dados=equipamento_json)
        db.session.add(historico_equipamento)
    
        fk_area_umida = body['fk_area_umida']
        tipo_equipamento = TiposEquipamentos.query.filter_by(
            aparelho_sanitario=body['tipo_equipamento']).first()
        quantTotal = body['quantTotal']
        quantProblema = body['quantProblema']
        quantInutil = body['quantInutil']

        equipamento.update(
            fk_area_umida=fk_area_umida,
            tipo_equipamento=tipo_equipamento.id,
            quantTotal=quantTotal,
            quantProblema=quantProblema,
            quantInutil=quantInutil
        )

        db.session.commit()

        return jsonify({"equipamento": equipamento.to_json(), "status": True}), HTTP_200_OK

    except exc.DBAPIError as e:

        if e.orig.pgcode == '23503':
            match = re.search(
                r'ERROR:  insert or update on table "(.*?)" violates foreign key constraint "(.*?)".*', str(e))
            tabela = match.group(1) if match else 'tabela desconhecida'
            coluna = match.group(2) if match else 'coluna desconhecida'
            mensagem = f"A operação não pôde ser concluída devido a uma violação de chave estrangeira na tabela '{tabela}', coluna '{coluna}'. Por favor, verifique os valores informados e tente novamente."
            return jsonify({'codigo': str(e), 'status': False, 'mensagem': mensagem}), HTTP_409_CONFLICT

        if e.orig.pgcode == '23505':
            # UNIQUE VIOLATION
            match = re.search(r'Key \((.*?)\)=', str(e))
            campo = match.group(1) if match else 'campo desconhecido'
            mensagem = f"Já existe um registro com o valor informado no campo '{campo}'. Por favor, corrija o valor e tente novamente."
            return jsonify({'status': False, 'mensagem': mensagem, 'código': str(e)}), HTTP_401_UNAUTHORIZED

        if e.orig.pgcode == '01004':
            # STRING DATA RIGHT TRUNCATION
            return jsonify({'status': False, 'mensagem': "Erro no cabeçalho", 'codigo': f'{e}'}), HTTP_506_VARIANT_ALSO_NEGOTIATES

        return jsonify({'status': False, 'mensagem': "Erro não Tratado", 'codigo': f'{e}'}), HTTP_400_BAD_REQUEST

    except Exception as e:
        if isinstance(e, HTTPException) and e.code == 500:
            return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

        if isinstance(e, HTTPException) and e.code == 400:
            # flash("Erro, 4 não salva")
            return jsonify({'status': False, 'mensagem': 'Erro na requisição', 'codigo': str(e)}), HTTP_400_BAD_REQUEST

        return jsonify({'status': False, 'mensagem': 'Erro não tratado', 'codigo': str(e)}), HTTP_400_BAD_REQUEST




# EDITAR EVENTOS
@editar.put('/tipo-evento/<id>')
def tipo_evento_editar(id):
    tipo_evento = TipoDeEventos.query.filter_by(id=id).first()
    formulario = request.get_json()

    meses_dict = {
        "Janeiro": 1,
        "Fevereiro": 2,
        "Março": 3,
        "Abril": 4,
        "Maio": 5,
        "Junho": 6,
        "Julho": 7,
        "Agosto": 8,
        "Setembro": 9,
        "Outubro": 10,
        "Novembro": 11,
        "Dezembro": 12
    }

    periodicidade = {
            "Ocasional":False, 
            "Recorrente":True
        }

    if not tipo_evento:
        return jsonify({'mensagem': 'tipo não encontrado', "status": False}), 404

    try:

        tipo_json = tipo_evento.to_json()
        tipo_json['data_criacao'] = tipo_json['data_criacao'].strftime('%m/%d/%Y %H:%M:%S')
        tipo_json['created_at'] = tipo_json['created_at'].strftime('%m/%d/%Y %H:%M:%S') if tipo_json['updated_at'] else None
        #tipo_json['updated_at'] = tipo_json['updated_at'].strftime('%m/%d/%Y %H:%M:%S') if tipo_json['updated_at'] else None

        historico_tipo_evento = Historico(tabela="tipo_evento", dados=tipo_json)
        db.session.add(historico_tipo_evento)
        
        fk_cliente = formulario.get("fk_cliente")
        nome_do_tipo_de_evento = formulario.get("nome_do_evento")
        periodicidade = periodicidade.get(formulario.get('periodicidade')) if formulario.get('periodicidade') is not None else False
        dia = formulario.get("dataRecorrente") if formulario.get('dataRecorrente') and formulario.get("dataRecorrente") !="" else None
        mes = meses_dict.get(formulario.get('mesRecorrente')) if formulario.get('mesRecorrente') and formulario.get('mesRecorrente') != "" else None
        requer_acao = formulario.get('requerResposta', None) if formulario.get('requerResposta') is not None else False
        tempo = formulario.get('tolerancia') if formulario.get('tolerancia') else None
        unidade = formulario.get('unidade') if formulario.get('unidade') else None
        acao = formulario.get('ehResposta') if formulario.get('ehResposta') is not None else False


        tipo_evento.update(
            fk_cliente=fk_cliente,
            nome_do_tipo_de_evento=nome_do_tipo_de_evento,
            recorrente=periodicidade,
            dia=dia,
            mes= mes,
            requer_acao=requer_acao,
            tempo=tempo,
            unidade=unidade,
            acao=acao
        )

        db.session.commit()

        return jsonify({"tipo":tipo_evento.to_json(), "status": True}), HTTP_200_OK
    
    except exc.DBAPIError as e:
        if e.orig.pgcode == '23503':
            match = re.search(
                r'ERROR:  insert or update on table "(.*?)" violates foreign key constraint "(.*?)".*', str(e))
            tabela = match.group(1) if match else 'tabela desconhecida'
            coluna = match.group(2) if match else 'coluna desconhecida'
            mensagem = f"A operação não pôde ser concluída devido a uma violação de chave estrangeira na tabela '{tabela}', coluna '{coluna}'. Por favor, verifique os valores informados e tente novamente."
            return jsonify({'codigo': str(e), 'status': False, 'mensagem': mensagem}), HTTP_409_CONFLICT

        if e.orig.pgcode == '23505':
            # UNIQUE VIOLATION
            match = re.search(r'Key \((.*?)\)=', str(e))
            campo = match.group(1) if match else 'campo desconhecido'
            mensagem = f"Já existe um registro com o valor informado no campo '{campo}'. Por favor, corrija o valor e tente novamente."
            return jsonify({'status': False, 'mensagem': mensagem, 'código': str(e)}), HTTP_401_UNAUTHORIZED

        if e.orig.pgcode == '01004':
            # STRING DATA RIGHT TRUNCATION
            return jsonify({'status': False, 'mensagem': "Erro no cabeçalho", 'codigo': f'{e}'}), HTTP_506_VARIANT_ALSO_NEGOTIATES
        return jsonify({"status":False, "mensagem":"Erro não tratado", "codigo":str(e)})

    except Exception as e:
        if isinstance(e, HTTPException) and e.code == 500:
            return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

        if isinstance(e, HTTPException) and e.code == 400:
            # flash("Erro, 4 não salva")
            return jsonify({'status': False, 'mensagem': 'Erro na requisição', 'codigo': str(e)}), HTTP_400_BAD_REQUEST

        return jsonify({'status': False, 'mensagem': 'Erro não tratado', 'codigo': str(e)}), HTTP_400_BAD_REQUEST



# EVENTOS
@editar.put('/evento/<id>')
def evento_editar(id):
    evento = Eventos.query.filter_by(id=id).first()
    formulario = request.get_json()

    if not evento:
        return jsonify({'mensagem':'evento não encontrado', "status": False}), 404

    try:
        evento_json = evento.to_json()
        evento_json['data_criacao'] = evento_json['data_criacao'].strftime('%m/%d/%Y %H:%M:%S')
        evento_json['created_at'] = evento_json['created_at'].strftime('%m/%d/%Y %H:%M:%S')
        historico_evento = Historico(tabela="Evento", dados=evento_json)
        db.session.add(historico_evento)

        fk_tipo = formulario['fk_tipo']
        nome = formulario['nome']
        datainicio = formulario['datainicio']
        datafim = formulario["datafim"]
        prioridade = formulario["prioridade"]
        local = formulario['local']
        tipo_de_local = formulario['tipo_de_local']
        observacao = formulario["observacao"]
    

        evento.update(
            fk_tipo=fk_tipo,
            nome=nome,
            datainicio=datainicio,
            datafim=datafim,
            prioridade=prioridade,
            local=local,
            tipo_de_local=tipo_de_local,
            observacao=observacao
        )

        db.session.commit()

        return jsonify({"evento":evento.to_json(), "status": True}), HTTP_200_OK
    except exc.DBAPIError as e:
        if e.orig.pgcode == '23503':
            match = re.search(
                r'ERROR:  insert or update on table "(.*?)" violates foreign key constraint "(.*?)".*', str(e))
            tabela = match.group(1) if match else 'tabela desconhecida'
            coluna = match.group(2) if match else 'coluna desconhecida'
            mensagem = f"A operação não pôde ser concluída devido a uma violação de chave estrangeira na tabela '{tabela}', coluna '{coluna}'. Por favor, verifique os valores informados e tente novamente."
            return jsonify({'codigo': str(e), 'status': False, 'mensagem': mensagem}), HTTP_409_CONFLICT

        if e.orig.pgcode == '23505':
            # UNIQUE VIOLATION
            match = re.search(r'Key \((.*?)\)=', str(e))
            campo = match.group(1) if match else 'campo desconhecido'
            mensagem = f"Já existe um registro com o valor informado no campo '{campo}'. Por favor, corrija o valor e tente novamente."
            return jsonify({'status': False, 'mensagem': mensagem, 'código': str(e)}), HTTP_401_UNAUTHORIZED

        if e.orig.pgcode == '01004':
            # STRING DATA RIGHT TRUNCATION
            return jsonify({'status': False, 'mensagem': "Erro no cabeçalho", 'codigo': f'{e}'}), HTTP_506_VARIANT_ALSO_NEGOTIATES

    except Exception as e:
        if isinstance(e, HTTPException) and e.code == 500:
            return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

        if isinstance(e, HTTPException) and e.code == 400:
            # flash("Erro, 4 não salva")
            return jsonify({'status': False, 'mensagem': 'Erro na requisição', 'codigo': str(e)}), HTTP_400_BAD_REQUEST

        return jsonify({'status': False, 'mensagem': 'Erro não tratado', 'codigo': str(e)}), HTTP_400_BAD_REQUEST


