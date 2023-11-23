from flask import request
from flask_praetorian import current_user
from functools import wraps
from flask import jsonify

def refresh_token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Obter o token do cabeçalho de autorização
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Token missing or invalid'}), 401

        token = auth_header.split(' ')[1]

        # Verify the old token
        try:
            new_token = guard.refresh_jwt_token(token)
        except Exception as e:
            return jsonify({'error': str(e)}), 401

        # Adicionar o novo token aos argumentos da função
        kwargs['new_token'] = new_token

        # Chamar a função original com o novo token
        result = f(*args, **kwargs)

        return result

    return decorated_function