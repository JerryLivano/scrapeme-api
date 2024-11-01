from flask import jsonify, request, Flask
from pymongo.synchronous.database import Database
from dto.role.role_request_dto import RoleRequestDto
from middleware.auth_middleware import AuthMiddleware
from services.role_service import RoleService

class RoleController:
    def __init__(self, app: Flask, db: Database):
        self._role_service = RoleService(db)
        self._auth_middleware = AuthMiddleware()

        app.add_url_rule('/role', 'get_roles', self._auth_middleware.token_required(self.get_roles), methods=['GET'])
        app.add_url_rule('/role/<string:guid>', 'get_role_by_guid', self._auth_middleware.token_required(self.get_role_by_guid), methods=['GET'])
        app.add_url_rule('/role', 'create_role', self._auth_middleware.token_required(self.create_role), methods=['POST'])
        app.add_url_rule('/role/<string:guid>', 'update_role', self._auth_middleware.token_required(self.update_role), methods=['PUT'])
        app.add_url_rule('/role/<string:guid>', 'delete_role', self._auth_middleware.token_required(self.delete_role), methods=['DELETE'])

    def get_roles(self):
        """
        Get All Roles Data
        ---
        tags: ['Role']
        responses:
            200:
                description: List of all roles
            400:
                description: Failed to get all roles
            500:
                description: Internal server error
        """
        try:
            roles = self._role_service.get_all()

            if not roles:
                return jsonify({
                    'status': 400,
                    'message': 'Failed to get roles'
                }), 400

            data = [role.__dict__ for role in roles]

            return jsonify({
                'status': 200,
                'message': 'Roles get successfully',
                'data': data
            })

        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def get_role_by_guid(self, guid: str):
        """
        Get Role by GUID
        ---
        tags: ['Role']
        parameters:
          - name: guid
            in: path
            required: true
            type: string
            description: GUID of the role to retrieve
        responses:
            200:
                description: Role retrieved successfully
            404:
                description: Role not found
            500:
                description: Internal server error
        """
        try:
            role = self._role_service.get_by_guid(guid)

            if role:
                return jsonify({
                    'status': 200,
                    'message': 'Role retrieved successfully',
                    'data': role.__dict__
                }), 200
            else:
                return jsonify({
                    'status': 404,
                    'message': 'Role not found'
                }), 404

        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def create_role(self):
        """
        Create a new Role
        ---
        tags: ['Role']
        parameters:
          - name: RoleRequestDto
            in: body
            required: true
            schema:
              id: RoleRequestDto
              properties:
                role_name:
                  type: string
                  description: Name of the role to create
        responses:
            200:
                description: Role created successfully
            400:
                description: Bad request (invalid JSON or missing fields)
            500:
                description: Internal server error
        """
        try:
            data = request.get_json()

            if not data or 'role_name' not in data:
                return jsonify({
                    'status': 400,
                    'message': 'Invalid request payload or missing role_name'
                }), 400

            role_request_dto = RoleRequestDto(**data)

            new_role = self._role_service.create_role(role_request_dto)

            if new_role:
                return jsonify({
                    'status': 200,
                    'message': 'Role created successfully',
                    'data': new_role.__dict__
                }), 200
            else:
                return jsonify({
                    'status': 500,
                    'message': 'Failed to create role'
                }), 500

        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def update_role(self, guid: str):
        """
            Update Role
            ---
            tags: ['Role']
            parameters:
              - name: guid
                in: path
                required: true
                type: string
                description: GUID of the role to retrieve
              - name: RoleRequestDto
                in: body
                required: true
                schema:
                  id: RoleRequestDto
                  properties:
                    role_name:
                      type: string
                      description: Name of the role to create
            responses:
                200:
                    description: Role updated successfully
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

            role_request_dto = RoleRequestDto(**data)

            result = self._role_service.update_role(guid, role_request_dto)

            if result == 1:
                return jsonify({
                    'status': 200,
                    'message': 'Role successfully updated'
                }), 200
            elif result == -2:
                return jsonify({
                    'status': 404,
                    'message': 'Role not found'
                }), 404
            elif result == 0:
                return jsonify({
                    'status': 400,
                    'message': 'Failed to update role'
                }), 400
            elif result == -1:
                return jsonify({
                    'status': 500,
                    'message': 'Internal Server Error'
                }), 500
        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def delete_role(self, guid: str):
        """
            Delete Role
            ---
            tags: ['Role']
            parameters:
              - name: guid
                in: path
                required: true
                type: string
                description: GUID of the role to retrieve
            responses:
                200:
                    description: Role deleted successfully
                404:
                    description: Request not found
                500:
                    description: Internal server error
        """
        try:
            result = self._role_service.delete_role(guid)

            if result == 1:
                return jsonify({
                    'status': 200,
                    'message': 'Role successfully deleted'
                }), 200
            elif result == 0:
                return jsonify({
                    'status': 404,
                    'message': 'Role not found'
                }), 404
            elif result == -1:
                return jsonify({
                    'status': 500,
                    'message': 'Internal server error'
                }), 500
        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500