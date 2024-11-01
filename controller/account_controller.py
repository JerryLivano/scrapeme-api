from flask import request, jsonify, Flask
from pymongo.database import Database
from dto.account.account_update_request_dto import AccountUpdateRequestDto
from dto.account.change_password_request_dto import ChangePasswordRequestDto
from dto.account.login_request_dto import LoginRequestDto
from dto.account.login_response_dto import LoginResponseDto
from dto.account.register_request_dto import RegisterRequestDto
from dto.account.token_request_dto import TokenRequestDto
from entities.role import Role
from handlers.jwt_handler import JWTHandler
from middleware.auth_middleware import AuthMiddleware
from services.account_service import AccountService

class AccountController:
    def __init__(self, app: Flask, db: Database):
        self._account_service = AccountService(db)
        self._jwt_handler = JWTHandler()
        self._auth_middleware = AuthMiddleware()

        app.add_url_rule('/account', 'get_all', self._auth_middleware.token_required(self.get_all), methods=['GET'])
        app.add_url_rule('/account/<string:guid>', 'get_account_by_guid', self._auth_middleware.token_required(self.get_account_by_guid), methods=['GET'])
        app.add_url_rule('/account', 'update_account', self._auth_middleware.token_required(self.update_account), methods=['PUT'])
        app.add_url_rule('/account/<string:guid>', 'delete_account', self._auth_middleware.token_required(self.delete_account), methods=['DELETE'])
        app.add_url_rule('/register', 'register', self.register, methods=['POST'])
        app.add_url_rule('/login', 'login', self.login, methods=['POST'])
        app.add_url_rule('/account/change-password', 'change_password', self._auth_middleware.token_required(self.change_password), methods=['PUT'])

    def get_all(self):
        """
            Get All Accounts Data
            ---
            tags: ['Account']
            parameters:
              - name: search
                in: query
                type: string
                description: Search query
              - name: page
                in: query
                type: integer
                description: Page query
              - name: limit
                in: query
                type: integer
                description: Limit query
              - name: is_active
                in: query
                type: integer
                description: Status query
              - name: role_name
                in: query
                type: string
                description: Role query
              - name: order_by
                in: query
                type: integer
                description: Order by query
              - name: column_name
                in: query
                type: string
                description: Column name query
            responses:
                200:
                    description: List of all accounts
                500:
                    description: Internal server error
        """
        try:
            page = int(request.args.get('page'))
            limit = int(request.args.get('limit'))
            search = request.args.get('search', '')
            is_active = request.args.get('is_active', -1)
            role_name = request.args.get('role_name', None)
            order_by = request.args.get('order_by', 0)
            column_name = request.args.get('column_name', None)

            response = self._account_service.get_all(search, page, limit, is_active, role_name, order_by, column_name)

            return jsonify({
                'status': 200,
                'message': 'Accounts get successfully',
                'data': response.data,
                'pagination': vars(response.pagination)
            })

        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def get_account_by_guid(self, guid: str):
        """
        Get Account by GUID
        ---
        tags: ['Account']
        parameters:
          - name: guid
            in: path
            required: true
            type: string
            description: GUID of the account to retrieve
        responses:
            200:
                description: Account retrieved successfully
            404:
                description: Account not found
            500:
                description: Internal server error
        """
        try:
            account = self._account_service.get_by_guid(guid)

            if account:
                return jsonify({
                    'status': 200,
                    'message': 'Account retrieved successfully',
                    'data': account.__dict__
                }), 200
            else:
                return jsonify({
                    'status': 404,
                    'message': 'Account not found'
                }), 404

        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def update_account(self):
        """
            Update Account
            ---
            tags: ['Account']
            parameters:
              - name: AccountUpdateRequestDto
                in: body
                required: true
                schema:
                  id: AccountUpdateRequestDto
                  properties:
                    guid:
                      type: string
                      description: Account Guid
                    first_name:
                      type: string
                      description: First name
                    last_name:
                      type: string
                      description: Last name
                    email:
                      type: string
                      description: Email
                    is_active:
                      type: boolean
                      description: First name
                    role_guid:
                      type: string
                      description: Role guid
            responses:
                200:
                    description: Account updated successfully
                400:
                    description: Failed to update
                404:
                    description: Request not found
                500:
                    description: Internal server error
        """
        try:
            data = request.get_json()

            if not data:
                return jsonify({
                    'status': 400,
                    'message': 'Invalid request payload'
                }), 400

            account_request = AccountUpdateRequestDto(**data)

            result = self._account_service.update_account(account_request)

            if result == -2:
                return jsonify({
                    'status': 404,
                    'message': 'Account not found'
                }), 404

            if result == -3:
                return jsonify({
                    'status': 404,
                    'message': 'Email already exist'
                }), 404

            if result == -1:
                return jsonify({
                    'status': 500,
                    'message': 'Internal Server Error'
                }), 500

            if result == 0:
                return jsonify({
                    'status': 400,
                    'message': 'Failed to update account'
                }), 400

            return jsonify({
                'status': 200,
                'message': 'Successfully updated account'
            }), 200

        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def delete_account(self, guid: str):
        """
            Delete Account
            ---
            tags: ['Account']
            parameters:
              - name: guid
                in: path
                required: true
                type: string
                description: GUID of the account to retrieve
            responses:
                200:
                    description: Account deleted successfully
                404:
                    description: Request not found
                400:
                    description: Failed to delete
                500:
                    description: Internal server error
        """
        try:
            result = self._account_service.delete_account(guid)

            if result == -2:
                return jsonify({
                    'status': 404,
                    'message': 'Account not found'
                }), 404

            if result == -1:
                return jsonify({
                    'status': 500,
                    'message': 'Internal server error'
                }), 500

            if result == 0:
                return jsonify({
                    'status': 400,
                    'message': 'Failed to delete account'
                }), 400

            return jsonify({
                'status': 200,
                'message': 'Account deleted successfully'
            }), 200
        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def register(self):
        """
            Register a new user
            ---
            tags: ['Account']
            parameters:
              - name: body
                in: body
                required: true
                schema:
                  id: RegisterRequestDto
                  properties:
                    first_name:
                      type: string
                      description: The first name of the user
                    last_name:
                      type: string
                      description: The last name of the user
                    email:
                      type: string
                      description: The email of the user
                    password:
                      type: string
                      description: The password of the user
                    confirm_password:
                      type: string
                      description: The confirmation password
                    created_by:
                      type: string
                      description: The creator of the user (optional)
                    role_guid:
                      type: string
                      description: role id
            responses:
                201:
                    description: Registration successful
                400:
                    description: Registration failed
                403:
                    description: Invalid payload
                404:
                    description: Data not found
                500:
                    description: Internal server error
        """
        try:
            data = request.get_json()

            register_request = RegisterRequestDto(**data)

            result = self._account_service.register(register_request)

            if result == 0:
                return jsonify({
                    'status': 400,
                    'message': 'Failed to register'
                }), 400

            if result == -2:
                return jsonify({
                    'status': 403,
                    'message': 'Password not match'
                }), 403

            if result == -3:
                return jsonify({
                    'status': 404,
                    'message': 'Account already exist'
                }), 404

            if result == -1:
                return jsonify({
                    'status': 500,
                    'message': 'Internal server error'
                }), 500

            if result == 1:
                return jsonify({
                    'status': 200,
                    'message': 'Register success',
                }), 200

        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def login(self):
        """
            Login User
            ---
            tags: ['Auth']
            parameters:
              - name: body
                in: body
                required: true
                schema:
                  id: LoginRequestDto
                  properties:
                    email:
                      type: string
                      description: The email of the user
                    password:
                      type: string
                      description: The password of the user
            responses:
                201:
                    description: Registration successful
                404:
                    description: Invalid credentials
                403:
                    description: Permission invalid
                500:
                    description: Internal server error
        """
        try:
            data = request.get_json()

            login_request = LoginRequestDto(**data)

            result = self._account_service.login(login_request)

            if result == -1:
                return jsonify({
                    'status': 500,
                    'message': 'Failed to login'
                }), 500

            if result == 0:
                return jsonify({
                    'status': 404,
                    'message': 'Incorrect email or password'
                }), 404

            if result == -2:
                return jsonify({
                    'status': 403,
                    'message': 'Your account is inactive'
                }), 403

            if result == -3:
                return jsonify({
                    'status': 403,
                    'message': "You don't have permission"
                }), 403

            account = self._account_service.get_by_email(data['email'])

            token_request: TokenRequestDto = TokenRequestDto(
                guid=account.guid,
                sub_guid=account.user['guid'],
                fullname=(account.user['first_name'].strip()) + (
                    (" " + account.user['last_name'].strip()) if account.user[
                        'last_name'] else ""),
                email=account.user['email'],
                role=Role(
                    account.role['guid'],
                    account.role['role_name']
                )
            )

            token = self._jwt_handler.generate_token(token_request)

            return jsonify({
                'status': 200,
                'message': 'Login success',
                'data': LoginResponseDto(token).__dict__
            }), 200

        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def change_password(self):
        """
            Change password
            ---
            tags: ['Account']
            parameters:
              - name: body
                in: body
                required: true
                schema:
                  id: ChangePasswordRequestDto
                  properties:
                    guid:
                      type: string
                      description: account guid
                    password:
                      type: string
                      description: password
                    confirm_password:
                      type: string
                      description: confirm password
            responses:
                200:
                    description: Success
                400:
                    description: Failed
                403:
                    description: Invalid payload
                404:
                    description: Data not found
                500:
                    description: Internal server error
        """
        try:
            data = request.get_json()
            change_password_request = ChangePasswordRequestDto(**data)
            result = self._account_service.change_password(change_password_request)

            if result == -3:
                return jsonify({
                    'status': 403,
                    'message': 'Password not match'
                }), 403
            if result == -2:
                return jsonify({
                    'status': 404,
                    'message': 'Account not found'
                }), 404
            if result == -1:
                return jsonify({
                    'status': 500,
                    'message': 'Internal server error'
                }), 500
            if result == 0:
                return jsonify({
                    'status': 400,
                    'message': 'Failed to change password'
                }), 400
            return jsonify({
                'status': 200,
                'message': 'Change password successfully'
            }), 200
        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500
