import json
from flask import Blueprint, jsonify, request
import re
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_506_VARIANT_ALSO_NEGOTIATES, HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR
from sqlalchemy import exc
from werkzeug.exceptions import HTTPException
from werkzeug.security import generate_password_hash
from ..models import (Escolas, Edificios, EscolaNiveis, EscolaNiveisVersion, db, AreaUmida, Usuarios, Cliente, Equipamentos, Populacao, Hidrometros,
                      AuxOpNiveis, AuxTipoAreaUmida, AuxTiposEquipamentos, Reservatorios, AuxPopulacaoPeriodo, AuxOperacaoAreaUmida, ReservatorioEdificio, ReservatorioEdificiosVersion)
import traceback
from sqlalchemy.exc import ArgumentError
from datetime import datetime

cadastros = Blueprint('cadastros', __name__, url_prefix='/api/v1/cadastros')


# cadastro de cliente
@cadastros.post('/cliente')
def cliente():

    try:

        formulario = request.get_json()

    except Exception as e:
        return jsonify({
            "mensagem": "Não foi possível recuperar o formulario!",
            "status": False,
            "codigo": e
        }), 400

    try:
        cliente = Cliente(**formulario)
        db.session.add(cliente)
        db.session.commit()

        return jsonify({'status': True, "mensagem": "Cadastro Realizado", "data": cliente.to_json()}), HTTP_200_OK

    except ArgumentError as e:
        error_message = str(e)
        error_data = {'error': error_message}
        json_error = json.dumps(error_data)
        print(json_error)
        return json_error

    except exc.DBAPIError as e:
        db.session.rollback()
        if e.orig.pgcode == '23505':
            # extrai o nome do campo da mensagem de erro
            match = re.search(r'Key \((.*?)\)=', str(e))
            campo = match.group(1) if match else 'campo desconhecido'
            mensagem = f"Já existe um registro com o valor informado no campo '{campo}'. Por favor, corrija o valor e tente novamente."
            return jsonify({'status': False, 'mensagem': mensagem, 'código': str(e)}), HTTP_401_UNAUTHORIZED

        if e.orig.pgcode == '01004':
            return jsonify({'status': False, 'mensagem': 'Erro no cabeçalho.', 'codigo': str(e)}), HTTP_506_VARIANT_ALSO_NEGOTIATES
        return jsonify({'status': False, 'mensagem': 'Erro postgresql', 'codigo': str(e)}), 500

    except Exception as e:
        db.session.rollback()
        if isinstance(e, HTTPException) and e.code == '500':
            return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
        if isinstance(e, HTTPException) and e.code == '400':
            # flash("Erro, 4 não salva")
            return jsonify({'status': False, 'mensagem': 'Erro na requisição', 'codigo': str(e)}), HTTP_400_BAD_REQUEST
        return jsonify({
            "erro": e
        })


# cadastro de usuário
@cadastros.post('/usuario')
def usuario():

    try:
        formulario = request.get_json()

    except Exception as e:
        return jsonify({
            "mensagem": "Não foi possível recuperar o formulario!",
            "status": False,
            "codigo": e
        }), 400

    try:
        cod_cliente = formulario['cod_cliente']
        nome = formulario['nome']
        email = formulario['email']
        senha = formulario['senha']

    except Exception as e:
        return jsonify({
            "mensagem": "Verifique os nomes das variaveis do json enviado!!!",
            "status": False
        }), 400

    try:
        # COLOCANDO LIMITE NA SENHA
        if len(senha) < 6:
            return jsonify({'error': 'Senha muito curta'}), HTTP_400_BAD_REQUEST

        # GERANDO HASH DA SENHA
        pws_hash = generate_password_hash(senha)

        # CRIANDO O USUÁRIO
        usuario = Usuarios(
            cod_cliente=cod_cliente,
            nome=nome,
            email=email,
            senha=generate_password_hash(senha))

        db.session.add(usuario)
        db.session.commit()
        return jsonify({'status': True, "mensagem": "Cadastro Realizado", "data": usuario.to_json()}), HTTP_200_OK

    except ArgumentError as e:
        error_message = str(e)
        error_data = {'error': error_message}
        json_error = json.dumps(error_data)
        print(json_error)
        return json_error

    except exc.DBAPIError as e:
        db.session.rollback()
        if e.orig.pgcode == '23505':
            # extrai o nome do campo da mensagem de erro
            match = re.search(r'Key \((.*?)\)=', str(e))
            campo = match.group(1) if match else 'campo desconhecido'
            mensagem = f"Já existe um registro com o valor informado no campo '{campo}'. Por favor, corrija o valor e tente novamente."
            return jsonify({'status': False, 'mensagem': mensagem, 'código': str(e)}), HTTP_401_UNAUTHORIZED

        if e.orig.pgcode == '01004':
            return jsonify({'status': False, 'mensagem': 'Erro no cabeçalho.', 'codigo': str(e)}), HTTP_506_VARIANT_ALSO_NEGOTIATES
        return jsonify({'status': False, 'mensagem': 'Erro postgresql', 'codigo': str(e)}), 500

    except Exception as e:
        db.session.rollback()
        if isinstance(e, HTTPException) and e.code == '500':
            return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
        if isinstance(e, HTTPException) and e.code == '400':
            # flash("Erro, 4 não salva")
            return jsonify({'status': False, 'mensagem': 'Erro na requisição', 'codigo': str(e)}), HTTP_400_BAD_REQUEST
        return jsonify({
            "erro": e
        })


# Cadastros das escolas
@cadastros.post('/escolas')
def escolas():
    try:
        formulario = request.get_json()
    except Exception as e:
        return jsonify({
            "mensagem": "Não foi possível recuperar o formulario!",
            "status": False,
            "codigo": e
        }), 400

    try:
        nome = formulario["nome"]
        cnpj = formulario["cnpj"]
        email = formulario["email"]
        telefone = formulario["telefone"]
        logradouro = formulario["logradouro"]
        cep = formulario["cep"]
        complemento = formulario["complemento"]
        numero = formulario["numero"]
        nivel = formulario["nivel"]
        cidade = formulario["cidade"]
        estado = formulario["estado"]
        bairro = formulario["bairro"]

    except Exception as e:
        return jsonify({
            "mensagem": "Verifique os nomes das variaveis do json enviado!!!",
            "status": False
        }), 400

    try:
        escola = Escolas(
            nome=nome,
            cnpj=cnpj,
            email=email,
            telefone=telefone,
        )

        db.session.add(escola)

        # VERIFICAR NÍVEIS

        niveis_query = AuxOpNiveis.query.filter(
            AuxOpNiveis.nivel.in_(nivel)).all()
        # realizar controle, de que não foi cadastrado nível

        escola_niveis = [EscolaNiveis(
            nivel_ensino_id=nivel.id, escola_id=escola.id
        ) for nivel in niveis_query]
        db.session.add_all(escola_niveis)

        # Versionamento
        escola_niveis_version = [EscolaNiveisVersion(
            niviel_ensino_id=nivel.id,
            escola_id=escola.id,
            transacao=0,
            created_at=datetime.now()
        ) for nivel in niveis_query]

        db.session.add_all(escola_niveis_version)

        edificio = Edificios(
            fk_escola=int(escola.id),
            cnpj_edificio=cnpj,
            nome_do_edificio=nome,
            logradouro_edificio=logradouro,
            cep_edificio=cep,
            numero_edificio=numero,
            cidade_edificio=cidade,
            estado_edificio=estado,
            complemento_edificio=complemento,
            bairro_edificio=bairro
        )

        db.session.add(edificio)
        db.session.commit()

        return jsonify({'status': True, 'id': escola.id, "mensagem": "Cadastro Realizado", "data": escola.to_json(), "dada_edificio": edificio.to_json()}), HTTP_200_OK

    except ArgumentError as e:
        db.session.rollback()
        error_message = str(e)
        error_data = {'error': error_message}
        json_error = json.dumps(error_data)
        print(json_error)
        return json_error

    except exc.DBAPIError as e:
        db.session.rollback()
        if e.orig.pgcode == '23505':
            # extrai o nome do campo da mensagem de erro
            match = re.search(r'Key \((.*?)\)=', str(e))
            campo = match.group(1) if match else 'campo desconhecido'
            mensagem = f"Já existe um registro com o valor informado no campo '{campo}'. Por favor, corrija o valor e tente novamente."
            return jsonify({'status': False, 'mensagem': mensagem, 'código': str(e)}), HTTP_401_UNAUTHORIZED

        if e.orig.pgcode == '01004':
            return jsonify({'status': False, 'mensagem': 'Erro no cabeçalho.', 'codigo': str(e)}), HTTP_506_VARIANT_ALSO_NEGOTIATES
        return jsonify({'status': False, 'mensagem': 'Erro postgresql', 'codigo': str(e)}), 500

    except Exception as e:
        db.session.rollback()
        if isinstance(e, HTTPException) and e.code == '500':
            return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
        if isinstance(e, HTTPException) and e.code == '400':
            # flash("Erro, 4 não salva")
            return jsonify({'status': False, 'mensagem': 'Erro na requisição', 'codigo': str(e)}), HTTP_400_BAD_REQUEST
        return jsonify({
            "erro": e
        })


# cadastro de reservatorios
@cadastros.post('/reservatorios')
def reservatorios():

    try:
        formulario = request.get_json()
    except Exception as e:
        return jsonify({
            "mensagem": "Não foi possível recuperar o formulario!",
            "status": False,
            "codigo": e
        }), 400

    try:

        fk_escola = formulario['fk_escola']
        nome_do_reservatorio = formulario['nome']
    except Exception as e:
        return jsonify({
            "mensagem": "Verifique os nomes das variaveis do json enviado!!!",
            "status": False
        }), 400

    try:
        # CRIANDO O RESERVATORIO
        reservatorio = Reservatorios(
            fk_escola=fk_escola,
            nome_do_reservatorio=nome_do_reservatorio)

        db.session.add(reservatorio)
        db.session.commit()
        return jsonify({'status': True, "mensagem": "Cadastro Realizado", "data": reservatorio.to_json()}), HTTP_200_OK

    except ArgumentError as e:
        error_message = str(e)
        error_data = {'error': error_message}
        json_error = json.dumps(error_data)
        print(json_error)
        return json_error

    except exc.DBAPIError as e:
        db.session.rollback()
        if e.orig.pgcode == '23505':
            # extrai o nome do campo da mensagem de erro
            match = re.search(r'Key \((.*?)\)=', str(e))
            campo = match.group(1) if match else 'campo desconhecido'
            mensagem = f"Já existe um registro com o valor informado no campo '{campo}'. Por favor, corrija o valor e tente novamente."
            return jsonify({'status': False, 'mensagem': mensagem, 'código': str(e)}), HTTP_401_UNAUTHORIZED

        if e.orig.pgcode == '01004':
            return jsonify({'status': False, 'mensagem': 'Erro no cabeçalho.', 'codigo': str(e)}), HTTP_506_VARIANT_ALSO_NEGOTIATES
        return jsonify({'status': False, 'mensagem': 'Erro postgresql', 'codigo': str(e)}), 500

    except Exception as e:
        db.session.rollback()
        if isinstance(e, HTTPException) and e.code == '500':
            return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
        if isinstance(e, HTTPException) and e.code == '400':
            # flash("Erro, 4 não salva")
            return jsonify({'status': False, 'mensagem': 'Erro na requisição', 'codigo': str(e)}), HTTP_400_BAD_REQUEST
        return jsonify({
            "erro": e
        })


# Cadastros dos edifícios.
@cadastros.post('/edificios')
def edificios():

    try:
        formulario = request.get_json()
    except Exception as e:
        return jsonify({
            "mensagem": "Não foi possível recuperar o formulario!",
            "status": False,
            "codigo": e
        }), 400

    try:
        fk_escola = formulario['fk_escola']
        agua_de_reuso = formulario['agua_de_reuso']
        area_total_edificio = formulario['area_total_edificio'] if formulario['area_total_edificio'] != "" else 0.0
        bairro_edificio = formulario['bairro_edificio']
        cep_edificio = formulario['cep_edificio']
        cidade_edificio = formulario['cidade_edificio']
        cnpj_edificio = formulario['cnpj_edificio']
        complemento_edificio = formulario['complemento_edificio']
        estado_edificio = formulario['estado_edificio']
        logradouro_edificio = formulario['logradouro_edificio']
        nome_do_edificio = formulario['nome_do_edificio']
        numero_edificio = formulario['numero_edificio']
        pavimentos_edificio = formulario['pavimentos_edificio'] if formulario['pavimentos_edificio'] != "" else 0.0
        reservatorios = formulario['reservatorio']
    except Exception as e:
        return jsonify({
            "mensagem": "Verifique os nomes das variaveis do json enviado!!!",
            "status": False
        }), 400

    try:
        edificio = Edificios(
            fk_escola=fk_escola,
            numero_edificio=numero_edificio,
            nome_do_edificio=nome_do_edificio,
            cep_edificio=cep_edificio,
            bairro_edificio=bairro_edificio,
            cidade_edificio=cidade_edificio,
            estado_edificio=estado_edificio,
            cnpj_edificio=cnpj_edificio,
            logradouro_edificio=logradouro_edificio,
            complemento_edificio=complemento_edificio,
            pavimentos_edificio=pavimentos_edificio,
            area_total_edificio=area_total_edificio,
            agua_de_reuso=agua_de_reuso,
        )

        db.session.add(edificio)

        for reservatorio_enviado in reservatorios:
            reserv = Reservatorios.query.filter_by(
                nome_do_reservatorio=reservatorio_enviado).first()

            if reserv:

                reservatorio = ReservatorioEdificio(
                    edificio_id=edificio.id,
                    reservatorio_id=reserv.id
                )

                db.session.add(reservatorio)

                reservatorio_vesion = ReservatorioEdificioVersion(
                    edificio_id=edificio.id,
                    reservatorio_id=reserv.id,
                    transacao=0,
                    created_at=datetime.now()
                )
                db.session.add(reservatorio_vesion)

            else:
                db.session.rollback()
                return jsonify({'status': False, 'mensagem': f'Reservatório não existente {reservatorio_enviado}', 'codigo': 'Falha'}), 409

        db.session.commit()

        return jsonify({'status': True, 'id': edificio.id, "mensagem": "Cadastro Realizado!", "data": edificio.to_json()}), HTTP_200_OK

    except exc.DBAPIError as e:
        db.session.rollback()
        if e.orig.pgcode == '23503':
            # FOREIGN KEY VIOLATION
            match = re.search(
                r'ERROR:  insert or update on table "(.*?)" violates foreign key constraint "(.*?)".*', str(e))
            tabela = match.group(1) if match else 'tabela desconhecida'
            coluna = match.group(2) if match else 'coluna desconhecida'
            mensagem = f"A operação não pôde ser concluída devido a uma violação de chave estrangeira na tabela '{tabela}', coluna '{coluna}'. Por favor, verifique os valores informados e tente novamente."
            return jsonify({'codigo': str(e), 'status': False, 'mensagem': mensagem}), HTTP_409_CONFLICT

        if e.orig.pgcode == '23505':
            db.session.rollback()
            # UNIQUE VIOLATION
            match = re.search(r'Key \((.*?)\)=', str(e))
            campo = match.group(1) if match else 'campo desconhecido'
            mensagem = f"Já existe um registro com o valor informado no campo '{campo}'. Por favor, corrija o valor e tente novamente."
            return jsonify({'status': False, 'mensagem': mensagem, 'código': str(e)}), HTTP_401_UNAUTHORIZED

        if e.orig.pgcode == '01004':
            # STRING DATA RIGHT TRUNCATION
            return jsonify({'status': False, 'mensagem': 'Erro no cabeçalho', 'codigo': f'{e}'}), HTTP_506_VARIANT_ALSO_NEGOTIATES
        if e.orig.pgcode == '22P02':
            return jsonify({'status': False, 'mensagem': 'Erro no tipo de informação envida', 'codigo': f'{e}'}), HTTP_500_INTERNAL_SERVER_ERROR

    except Exception as e:
        db.session.rollback()
        traceback.print_exc()  # Imprime o traceback completo no console
        print("não entrou aqui")
        return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': 'Falha'}), HTTP_500_INTERNAL_SERVER_ERROR


@cadastros.post('/hidrometros')
def hidrometros():

    try:
        formulario = request.get_json()

    except Exception as e:
        return jsonify({
            "mensagem": "Não foi possível recuperar o formulario!",
            "status": False,
            "codigo": e
        }), 400

    try:
        hidrometros = Hidrometros(**formulario)
        db.session.add(hidrometros)
        db.session.commit()

        return jsonify({'status': True, 'id': hidrometros.id, "mensagem": "Cadastro Realizado com sucesso", "data": hidrometros.to_json()}), HTTP_200_OK

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
            return jsonify({'status': False, 'mensagem': 'Erro no cabeçalho', 'codigo': str(e)}), HTTP_506_VARIANT_ALSO_NEGOTIATES
        return jsonify({
            'status': False,
            'mensagem': 'Erro no banco não tratao!',
            'codigo': f'{e}'
        }), 500

    except Exception as e:
        db.session.rollback()
        if isinstance(e, HTTPException) and e.code == 500:
            return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

        if isinstance(e, HTTPException) and e.code == 400:
            # flash("Erro, 4 não salva")
            return jsonify({'status': False, 'mensagem': 'Erro na requisição', 'codigo': str(e)}), HTTP_400_BAD_REQUEST
        return jsonify({
            'status': False,
            'mensagem': 'Erro não tratado.',
            'codigo': str(e)
        })


@cadastros.post('/populacao')
def populacao():

    try:
        formulario = request.get_json()
    except Exception as e:
        return jsonify({
            "mensagem": "Não foi possível recuperar o formulario!",
            "status": False,
            "codigo": e
        }), 400

    try:

        alunos = formulario['alunos']
        nivel = formulario['nivel']
        periodo = formulario['periodo']
        funcionarios = formulario['funcionarios']
        fk_edificios = formulario['fk_edificios']

    except Exception as e:
        return jsonify({
            "mensagem": "Verifique os nomes das variaveis do json enviado!!!",
            "status": False
        }), 400

    try:
        nivel = db.session.query(AuxOpNiveis.id).filter_by(
            nivel=formulario['nivel']).scalar()
        periodo = db.session.query(AuxPopulacaoPeriodo.id).filter_by(
            periodo=formulario['periodo']).scalar()

        populacao = Populacao(
            alunos=alunos,
            funcionarios=funcionarios,
            fk_periodo=periodo,
            fk_edificios=fk_edificios,
            fk_niveis=nivel
        )
        db.session.add(populacao)
        db.session.commit()

        return jsonify({'status': True, 'id': populacao.id, "mensagem": "Cadastrado realizado com sucesso", "data": populacao.to_json()}), HTTP_200_OK

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
            return jsonify({'status': False, 'mensagem': 'Erro no cabeçalho', 'codigo': f'{e}'}), HTTP_506_VARIANT_ALSO_NEGOTIATES

        return jsonify({'status': False, 'mensagem': 'Erro não tratado', 'codigo': f'{e}'}), HTTP_500_INTERNAL_SERVER_ERROR

    except Exception as e:
        db.session.rollback()
        if isinstance(e, HTTPException) and e.code == 500:
            return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

        if isinstance(e, HTTPException) and e.code == 400:
            # flash("Erro, 4 não salva")
            return jsonify({'status': False, 'mensagem': 'Erro na requisição', 'codigo': str(e)}), HTTP_400_BAD_REQUEST
        return jsonify({
            'status': False, 'mensagem': 'Erro não tratado', 'codigo': str(e)
        }), HTTP_400_BAD_REQUEST


# Cadastros das areas umidas
@cadastros.post('/area-umida')
def area_umida():

    try:
        formulario = request.get_json()
    except Exception as e:
        return jsonify({
            "mensagem": "Não foi possível recuperar o formulario!",
            "status": False,
            "codigo": e
        }), 400

    try:
        fk_edificios = formulario['fk_edificios']
        tipo_area_umida = formulario['tipo_area_umida']
        nome_area_umida = formulario['nome_area_umida']
        localizacao_area_umida = formulario['localizacao_area_umida']
        status_area_umida = formulario['status_area_umida']
        operacao_area_umida = formulario['operacao_area_umida']
    except Exception as e:
        return jsonify({
            "mensagem": "Verifique os nomes das variaveis do json enviado!!!",
            "status": False
        }), 400

    try:
        tipos = AuxTipoAreaUmida.query.filter_by(tipo=tipo_area_umida).first()

        if status_area_umida == "Aberto":
            status_area_umida = True
        else:
            status_area_umida = False

        tipos = AuxTipoAreaUmida.query.filter_by(tipo=tipo_area_umida).first()
        operacao = AuxOperacaoAreaUmida.query.filter_by(
            operacao=operacao_area_umida).first()

        print(tipos, ' -- tipos')

        umida = AreaUmida(
            fk_edificios=fk_edificios,
            tipo_area_umida=tipos.id,
            nome_area_umida=nome_area_umida,
            localizacao_area_umida=localizacao_area_umida,
            status_area_umida=status_area_umida,
            operacao_area_umida=operacao.id
        )

        db.session.add(umida)
        db.session.commit()

        return jsonify({'status': True, 'id': umida.id, "mensagem": "Cadastrado realizado com sucesso", "data": umida.to_json()}), HTTP_200_OK

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

        return jsonify({'status': False, 'mensagem': "Erro não Tratado", 'codigo': f'{e}'}), HTTP_500_INTERNAL_SERVER_ERROR

    except Exception as e:
        db.session.rollback()
        if isinstance(e, HTTPException) and e.code == 500:
            return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

        if isinstance(e, HTTPException) and e.code == 400:
            # flash("Erro, 4 não salva")
            return jsonify({'status': False, 'mensagem': 'Erro na requisição', 'codigo': str(e)}), HTTP_400_BAD_REQUEST

        return jsonify({'status': False, 'mensagem': 'Erro não Tratado', 'codigo': str(e)}), HTTP_400_BAD_REQUEST


@cadastros.post('/equipamentos')
def equipamentos():

    try:
        formulario = request.get_json()
    except Exception as e:
        return jsonify({
            "mensagem": "Não foi possível recuperar o formulario!",
            "status": False,
            "codigo": e
        }), 400

    try:
        fk_area_umida = formulario['fk_area_umida']
        tipo_equipamento = formulario['tipo_equipamento']
        # descricao_equipamento = formulario['descricao_equipamento']
        quantTotal = formulario['quantTotal']
        quantProblema = formulario['quantProblema']
        quantInutil = formulario['quantInutil']
    except Exception as e:
        return jsonify({
            "mensagem": "Verifique os nomes das variaveis do json enviado!!!",
            "status": False
        }), 400

    try:
        tipo_equipamento = AuxTiposEquipamentos.query.filter_by(
            aparelho_sanitario=tipo_equipamento).first().id

        # descricao_equipamento = DescricaoEquipamentos.query.filter_by(descricao=descricao_equipamento).first().id

        equipamento = Equipamentos(
            fk_area_umida=fk_area_umida,
            tipo_equipamento=tipo_equipamento,
            # descricao_equipamento=descricao_equipamento,
            quantTotal=quantTotal,
            quantProblema=quantProblema,
            quantInutil=quantInutil
        )

        db.session.add(equipamento)
        db.session.commit()

        return jsonify({'status': True, 'id': equipamento.id, "mensagem": "Cadastrado realizado com sucesso", "data": equipamento.to_json()}), HTTP_200_OK

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

        if e.origin.pgcode == '22P02':
            return jsonify({'status': False, 'mensagem': 'Erro no tipo de informação envida', 'codigo': f'{e}'}), HTTP_500_INTERNAL_SERVER_ERROR

    except Exception as e:
        db.session.rollback()
        if isinstance(e, HTTPException) and e.code == 500:
            return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

        if isinstance(e, HTTPException) and e.code == 400:
            # flash("Erro, 4 não salva")
            return jsonify({'status': False, 'mensagem': 'Erro na requisição', 'codigo': str(e)}), HTTP_400_BAD_REQUEST
        print(e)
        return jsonify({
            'status': False,
            'mensagem': 'Erro não tratado.', 'codigo': str(e)
        }), HTTP_400_BAD_REQUEST
