from functools import wraps
from flask import request, jsonify
from handlers.jwt_handler import JWTHandler


class AuthMiddleware:
    def __init__(self):
        self._jwt_handler = JWTHandler()

    def token_required(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split(" ")[1] if len(
                    request.headers['Authorization'].split(" ")) == 2 else request.headers['Authorization']

            if not token:
                return jsonify({
                    'status': 401,
                    'message': 'Unauthorized'
                }), 401

            try:
                data = self._jwt_handler.decode_token(token)
                request.user_data = data
            except Exception as e:
                return jsonify({
                    'status': 401,
                    'message': f'Token is invalid: {str(e)}'
                }), 401

            return f(*args, **kwargs)

        return decorated
