from functools import wraps
from .models import db

def error_handler_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            # Personalize a resposta de erro conforme necessário
            error_message = f"Erro na função {func.__name__}: {str(e)}"
            raise ValueError(e)
    return wrapper


def error_cadstro_decorador(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        try:
            result = funct(*args, **kwargs)
            return result
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

    return wrapper