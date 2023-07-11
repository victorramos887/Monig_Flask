import json
from flask import Blueprint, jsonify, request
import re
from ..constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_506_VARIANT_ALSO_NEGOTIATES, HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED,HTTP_500_INTERNAL_SERVER_ERROR
from sqlalchemy import exc
from flasgger import swag_from
from werkzeug.exceptions import HTTPException
from werkzeug.security import  generate_password_hash
from ..models import Escolas, Edificios, EscolaNiveis, db, AreaUmida, Usuarios, Cliente, Equipamentos, Populacao, Hidrometros, OpNiveis, StatusAreaUmida,TipoAreaUmida, TiposEquipamentos, DescricaoEquipamentos, Reservatorios
import traceback
from sqlalchemy.exc import ArgumentError

cadastros = Blueprint('cadastros', __name__, url_prefix = '/api/v1/cadastros')



#cadastro de cliente
@cadastros.post('/cliente')
def cliente():

 try:

    formulario = request.get_json()
    cliente = Cliente(**formulario)
    db.session.add(cliente)
    db.session.commit()
        
    return jsonify({'status':True, "mensagem":"Cadastro Realizado","data":cliente.to_json()}), HTTP_200_OK
   
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
            #flash("Erro, 4 não salva")
            return jsonify({'status':False, 'mensagem': 'Erro na requisição', 'codigo':str(e)}), HTTP_400_BAD_REQUEST
        return jsonify({
            "erro":e
        })



#cadastro de usuário
@cadastros.post('/usuario')
def usuario():

    try:
        formulario = request.get_json()
        cod_cliente = formulario['cod_cliente']
        nome = formulario['nome']
        email = formulario['email']
        senha = formulario['senha']
        

        #COLOCANDO LIMITE NA SENHA
        if len(senha) < 6:
            return jsonify({'error':'Senha muito curta'}), HTTP_400_BAD_REQUEST

        #GERANDO HASH DA SENHA
        pws_hash = generate_password_hash(senha)

        #CRIANDO O USUÁRIO
        usuario = Usuarios(
            cod_cliente = cod_cliente,
            nome=nome, 
            email=email,
            senha=generate_password_hash(senha))  

        db.session.add(usuario)
        db.session.commit()
        return jsonify({'status':True, "mensagem":"Cadastro Realizado","data":usuario.to_json()}), HTTP_200_OK

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
            #flash("Erro, 4 não salva")
            return jsonify({'status':False, 'mensagem': 'Erro na requisição', 'codigo':str(e)}), HTTP_400_BAD_REQUEST
        return jsonify({
            "erro":e
        })



#Cadastros das escolas
@cadastros.post('/escolas')
@swag_from('../docs/cadastros/escolas.yaml')
def escolas():

    formulario = request.get_json()

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
        
        escola = Escolas(
            nome=nome,
            cnpj=cnpj,
            email=email,
            telefone=telefone,
        )
    
        db.session.add(escola)
        db.session.commit()

        # VERIFICAR NÍVEIS

        niveis_query = OpNiveis.query.filter(OpNiveis.nivel.in_(nivel)).all()
        #realizar controle, de que não foi cadastrado nível

        escola_niveis = [EscolaNiveis(
            nivel_ensino_id=nivel.id, escola_id=escola.id
        ) for nivel in niveis_query]
        db.session.add_all(escola_niveis)
        db.session.commit()

        edificio = Edificios(
            fk_escola = int(escola.id),
            cnpj_edificio=cnpj,
            nome_do_edificio=nome,
            logradouro_edificio = logradouro,
            cep_edificio = cep,
            numero_edificio = numero,
            cidade_edificio = cidade,
            estado_edificio = estado,
            complemento_edificio =complemento,
            bairro_edificio=bairro
        )


        db.session.add(edificio)
        db.session.commit()

        return jsonify({'status':True, 'id': escola.id, "mensagem":"Cadastro Realizado","data":escola.to_json(), "dada_edificio":edificio.to_json()}), HTTP_200_OK
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
            #flash("Erro, 4 não salva")
            return jsonify({'status':False, 'mensagem': 'Erro na requisição', 'codigo':str(e)}), HTTP_400_BAD_REQUEST
        return jsonify({
            "erro":e
        })


#cadastro de reservatorios
@cadastros.post('/reservatorios')
def reservatorios():

    formulario = request.get_json()
    try:
       
        fk_escola = formulario['fk_escola']
        nome_do_reservatorio = formulario['nome']
      
        # Criando ou obtendo o edifício associado ao reservatório
        edificio_id = formulario['fk_escola']
        edificio = Edificios.query.filter_by(id=edificio_id).first()
        if edificio is None:
            return jsonify({'status': False, "mensagem": "Edifício não encontrado."}), HTTP_400_BAD_REQUEST

        #CRIANDO O RESERVATORIO
        reservatorio = Reservatorios(
        fk_escola = fk_escola,
        nome_do_reservatorio = nome_do_reservatorio)
            
        # Associando o reservatório ao edifício
        edificio.reservatorio.append(reservatorio)    

        db.session.add(reservatorio)
        db.session.commit()
        return jsonify({'status':True, "mensagem":"Cadastro Realizado","data":reservatorio.to_json()}), HTTP_200_OK

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
            #flash("Erro, 4 não salva")
            return jsonify({'status':False, 'mensagem': 'Erro na requisição', 'codigo':str(e)}), HTTP_400_BAD_REQUEST
        return jsonify({
            "erro":e
        })


#Cadastros dos edifícios.
@cadastros.post('/edificios')
@swag_from('../docs/cadastros/edificios.yaml')
def edificios():

    try:
        formulario = request.get_json()
        edificio = Edificios(**formulario)
        db.session.add(edificio)
        db.session.commit()

        return jsonify({'status':True, 'id': edificio.id, "mensagem":"Cadastro Realizado!","data":edificio.to_json()}), HTTP_200_OK

    except exc.DBAPIError as e:
        db.session.rollback()
        if e.orig.pgcode == '23503':
            # FOREIGN KEY VIOLATION
            match = re.search(r'ERROR:  insert or update on table "(.*?)" violates foreign key constraint "(.*?)".*', str(e))
            tabela = match.group(1) if match else 'tabela desconhecida'
            coluna = match.group(2) if match else 'coluna desconhecida'
            mensagem = f"A operação não pôde ser concluída devido a uma violação de chave estrangeira na tabela '{tabela}', coluna '{coluna}'. Por favor, verifique os valores informados e tente novamente."
            return jsonify({ 'codigo': str(e), 'status': False, 'mensagem': mensagem}), HTTP_409_CONFLICT

        if e.orig.pgcode == '23505':
            db.session.rollback()
            # UNIQUE VIOLATION
            match = re.search(r'Key \((.*?)\)=', str(e))
            campo = match.group(1) if match else 'campo desconhecido'
            mensagem = f"Já existe um registro com o valor informado no campo '{campo}'. Por favor, corrija o valor e tente novamente."
            return jsonify({'status': False, 'mensagem': mensagem, 'código': str(e)}), HTTP_401_UNAUTHORIZED

        if e.orig.pgcode == '01004':
            #STRING DATA RIGHT TRUNCATION
            return jsonify({'status':False, 'mensagem': 'Erro no cabeçalho', 'codigo':f'{e}'}), HTTP_506_VARIANT_ALSO_NEGOTIATES
        if e.origin.pgcode == '22P02':
            return jsonify({'status':False, 'mensagem':'Erro no tipo de informação envida', 'codigo':f'{e}'}), HTTP_500_INTERNAL_SERVER_ERROR

    except Exception as e:
        db.session.rollback()
        traceback.print_exc()  # Imprime o traceback completo no console
        print("não entrou aqui")
        return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo':'Falha'}), HTTP_500_INTERNAL_SERVER_ERROR



@cadastros.post('/hidrometros')
@swag_from('../docs/cadastros/hidrometros.yaml')
def hidrometros():

    formulario = request.get_json()

    try:
        hidrometros = Hidrometros(**formulario)
        db.session.add(hidrometros)
        db.session.commit()

        return jsonify({'status':True, 'id': hidrometros.id, "mensagem":"Cadastro Realizado com sucesso","data":hidrometros.to_json()}), HTTP_200_OK

    except exc.DBAPIError as e:
        db.session.rollback()
        if e.orig.pgcode == '23503':
            match = re.search(r'ERROR:  insert or update on table "(.*?)" violates foreign key constraint "(.*?)".*', str(e))
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
            return jsonify({'status':False, 'mensagem': 'Erro no cabeçalho', 'codigo':f'{e}'}), HTTP_506_VARIANT_ALSO_NEGOTIATES

    except Exception as e:
        db.session.rollback()
        if isinstance(e, HTTPException) and e.code == 500:
            return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
        
        if isinstance(e, HTTPException) and e.code == 400:
            #flash("Erro, 4 não salva")
            return jsonify({'status':False, 'mensagem': 'Erro na requisição', 'codigo':str(e)}), HTTP_400_BAD_REQUEST



@cadastros.post('/populacao')
@swag_from('../docs/cadastros/populacao.yaml')
def populacao():

    formulario = request.get_json()

    try:
        populacao = Populacao(**formulario)
        db.session.add(populacao)
        db.session.commit()

        return jsonify({'status':True, 'id': populacao.id, "mensagem":"Cadastrado realizado com sucesso","data":populacao.to_json()}), HTTP_200_OK

    except exc.DBAPIError as e:
        db.session.rollback()
        if e.orig.pgcode == '23503':
            match = re.search(r'ERROR:  insert or update on table "(.*?)" violates foreign key constraint "(.*?)".*', str(e))
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
            return jsonify({'status':False, 'mensagem': 'Erro no cabeçalho', 'codigo':f'{e}'}), HTTP_506_VARIANT_ALSO_NEGOTIATES
        
        return jsonify({'status':False, 'mensagem': 'Erro não tratado', 'codigo':f'{e}'}), HTTP_500_INTERNAL_SERVER_ERROR
        

    except Exception as e:
        db.session.rollback()   
        if isinstance(e, HTTPException) and e.code == 500:
            return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
        
        if isinstance(e, HTTPException) and e.code == 400:
            #flash("Erro, 4 não salva")
            return jsonify({'status':False, 'mensagem': 'Erro na requisição', 'codigo':str(e)}), HTTP_400_BAD_REQUEST


#Cadastros das areas umidas
@cadastros.post('/area-umida')
@swag_from('../docs/cadastros/area-umida.yaml')
def area_umida():

    formulario = request.get_json()

    try:
        fk_edificios = formulario['fk_edificios']
        tipo_area_umida = formulario['tipo_area_umida']
        nome_area_umida = formulario['nome_area_umida']
        localizacao_area_umida = formulario['localizacao_area_umida']
        status_area_umida = formulario['status_area_umida']

        tipos = TipoAreaUmida.query.filter_by(tipo=tipo_area_umida).first()
        status = StatusAreaUmida.query.filter_by(status=status_area_umida).first()

        umida = AreaUmida(
            fk_edificios = fk_edificios,
            tipo_area_umida = tipos.id,
            nome_area_umida = nome_area_umida,
            localizacao_area_umida = localizacao_area_umida,
            status_area_umida = status.id
        )

        db.session.add(umida)
        db.session.commit()

        return jsonify({'status':True, 'id': umida.id, "mensagem":"Cadastrado realizado com sucesso","data":umida.to_json()}), HTTP_200_OK

    except exc.DBAPIError as e:
        db.session.rollback()
        if e.orig.pgcode == '23503':
            match = re.search(r'ERROR:  insert or update on table "(.*?)" violates foreign key constraint "(.*?)".*', str(e))
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
        db.session.rollback()
        if isinstance(e, HTTPException) and e.code == 500:
            return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
        
        if isinstance(e, HTTPException) and e.code == 400:
            #flash("Erro, 4 não salva")
            return jsonify({'status':False, 'mensagem': 'Erro na requisição', 'codigo':str(e)}), HTTP_400_BAD_REQUEST


@cadastros.post('/equipamentos')
@swag_from('../docs/cadastros/equipamentos.yaml')
def equipamentos():

    formulario = request.get_json()

    #CONTINUAR DAQUI
    try:
        fk_area_umida = formulario['fk_area_umida']
        tipo_equipamento = formulario['tipo_equipamento']
        descricao_equipamento = formulario['descricao_equipamento']
        quantTotal = formulario['quantTotal']
        quantProblema = formulario['quantProblema']
        quantInutil = formulario['quantInutil']

        tipo_equipamento = TiposEquipamentos.query.filter_by(equipamento=tipo_equipamento).first().id

        descricao_equipamento = DescricaoEquipamentos.query.filter_by(descricao=descricao_equipamento).first().id

        equipamento = Equipamentos(
            fk_area_umida=fk_area_umida,
            tipo_equipamento=tipo_equipamento,
            descricao_equipamento=descricao_equipamento,
            quantTotal=quantTotal,
            quantProblema=quantProblema,
            quantInutil=quantInutil
        )
        db.session.add(equipamento)
        db.session.commit()

        return jsonify({'status':True, 'id': equipamento.id, "mensagem":"Cadastrado realizado com sucesso","data":equipamento.to_json()}), HTTP_200_OK

    except exc.DBAPIError as e:
        db.session.rollback()
        if e.orig.pgcode == '23503':
            match = re.search(r'ERROR:  insert or update on table "(.*?)" violates foreign key constraint "(.*?)".*', str(e))
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

        if e.origin.pgcode == '22P02':
            return jsonify({'status':False, 'mensagem':'Erro no tipo de informação envida', 'codigo':f'{e}'}), HTTP_500_INTERNAL_SERVER_ERROR

    except Exception as e:
        db.session.rollback()
        if isinstance(e, HTTPException) and e.code == 500:
            return jsonify({'status': False, 'mensagem': 'Erro interno do servidor', 'codigo': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
        
        if isinstance(e, HTTPException) and e.code == 400:
            #flash("Erro, 4 não salva")
            return jsonify({'status':False, 'mensagem': 'Erro na requisição', 'codigo':str(e)}), HTTP_400_BAD_REQUEST