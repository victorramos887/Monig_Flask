from flask import Blueprint, jsonify, request
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_506_VARIANT_ALSO_NEGOTIATES, HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED,HTTP_500_INTERNAL_SERVER_ERROR
from ..models import Escolas, Edificios, db, AreaUmida, Equipamentos, Populacao, Hidrometros, Reservatorios, Cliente, Usuarios, TipoAreaUmida, StatusAreaUmida, TiposEquipamentos, OpNiveis, PopulacaoPeriodo, EscolaNiveis, ReservatorioEdificio
from sqlalchemy import exc
from werkzeug.exceptions import HTTPException
import re
from http import HTTPStatus

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
                
            print(op_nivel.id, ' nivel')
            if op_nivel:
                escola_nivel = EscolaNiveis(
                    escola_id=escola.id,
                    nivel_ensino_id=op_nivel.id
                )
                
                db.session.add(escola_nivel)

        # Remova os níveis de ensino que não estão mais presentes
        for nivel in niveis_removidos:
            op_nivel = OpNiveis.query.filter_by(id=nivel).first()
            print(op_nivel.id)
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
    
    body = request.get_json()

    try:
        edificio.update(principal=body['principal'])
        db.session.commit()

    except Exception as e:
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
    print(umida.to_json())
    if not umida or umida is None:
        return jsonify({'mensagem': 'Area Umida não encontrado', "status": False}), 404

    try:
        fk_edificios = body['fk_edificios']
        localizacao_area_umida = body['localizacao_area_umida']
        nome_area_umida = body['nome_area_umida']

        # status_area_umida = StatusAreaUmida.query.filter_by(status =body['status_area_umida']).first()
        tipo_area_umida = TipoAreaUmida.query.filter_by(
            tipo=body['tipo_area_umida']).first()

        umida.update(
            tipo_area_umida=tipo_area_umida.id,
            status_area_umida=True,
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
