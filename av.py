# cadastro de evento
@eventos.post('/eventos')
def eventos_cadastro_unitario():

    try:
        formulario = request.get_json()
    except Exception as e:
        return jsonify({
            "mensagem": "Não foi possível recuperar o formulario!",
            "status": False,
            "codigo": e
        }), 400
    
    try:
        #Verficando tipo de evento
        try:
            tipo_de_evento = formulario.get("tipo_de_evento", None)
            
            if not tipo_de_evento:
                return jsonify({
                    "mensagem": "Tipo de evento está Nulo!!!",
                    "status": False
                }), 400
                
            tipodeevento = AuxTipoDeEventos.query.filter_by(nome_do_tipo_de_evento=tipo_de_evento).first()
            
            if not tipodeevento:
                return jsonify({
                    "mensagem":f"Não foi encontrado o tipo de evento {tipo_de_evento}",
                    "status": False
                }), 400

        except Exception as e:
            return jsonify({
                "mensagem":"Não foi possível tratar o tipo de evento!",
                "codigo":str(e),
                "status":False
            }), 400


        fk_tipo = formulario.get("tipo_de_evento", None)
        nome = formulario.get("nome_do_evento", None)
        local = formulario.get("local", None)
        tipo_de_local = formulario.get("tipo_de_local", None)
        observacao = formulario.get("observacoes", None)
        
        if tipodeevento.recorrente:
            datainicio = formulario.get("data_inicio", None)
            datafim = formulario.get("data_fim", None)
            
        else:
            print("alguma coisa")
            datainicio = formulario.get("data",None)
            datafim = formulario.get("data",None)
            
        

        #Tratamento de tipo_de_local
        
        tipo_de_local_fk = AuxDeLocais.query.filter_by(nome_da_tabela=tipo_de_local).first()
        
        print(tipo_de_local_fk)
        
        if not tipo_de_local_fk:
            return jsonify({
                "mensagem":f"Não foi encontrado a tabela {formulario.get('tipo_de_local')}",
                "status":False
            }), 400
            
        
        local_fk = obter_local(tipo_de_local, local)
        
        if not local_fk:
            return jsonify({
                "mensagem":f"Não foi encontrado o local {local}",
                "status":False
            }), 400
            
            
        tipo_de_evento_fk = AuxTipoDeEventos.query.filter_by(nome_do_tipo_de_evento=fk_tipo).first()
        
        if not tipo_de_evento_fk:
            
            return jsonify({
                "mensagem":f"Não foi encontrado o tipo de evento {fk_tipo}",
                "status":False
            }), 400
            
        
        evento = Eventos(
            fk_tipo=tipo_de_evento_fk.id,
            nome=nome,
            datainicio=datainicio,
            datafim=datafim,
            local=local_fk.id,
            tipo_de_local=tipo_de_local_fk.id,
            observacao=observacao,
        )

        db.session.add(evento)
        db.session.commit()

        return jsonify({'status': True, "mensagem": "Cadastro Realizado!", "data": evento.to_json()}), HTTP_200_OK

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
