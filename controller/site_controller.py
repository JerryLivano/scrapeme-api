from flask import Flask, request, jsonify
from pymongo.database import Database
from dto.site.create_url_dto import CreateUrlDto
from dto.site.site_active_update_dto import SiteUpdateActiveDto
from dto.site.site_request_dto import SiteRequestDto
from dto.site.site_update_request_dto import SiteUpdateRequestDto
from middleware.auth_middleware import AuthMiddleware
from services.site_service import SiteService


class SiteController:
    def __init__(self, app: Flask, db: Database):
        self._site_service = SiteService(db)
        self._auth_middleware = AuthMiddleware()

        app.add_url_rule('/site/create-url', "create_url", self._auth_middleware.token_required(self.create_url),
                         methods=['POST'])
        app.add_url_rule("/site", "get_sites", self._auth_middleware.token_required(self.get_sites), methods=['GET'])
        app.add_url_rule("/site", "create_site", self._auth_middleware.token_required(self.create_site),
                         methods=['POST'])
        app.add_url_rule("/site", "update_site", self._auth_middleware.token_required(self.update_site),
                         methods=['PUT'])
        app.add_url_rule("/site/active-status", "update_active_site", self._auth_middleware.token_required(self.update_active_site),
                         methods=['PUT'])
        app.add_url_rule("/site/<string:guid>", "delete_site", self._auth_middleware.token_required(self.delete_site),
                         methods=['DELETE'])

    def create_url(self):
        """
            Create URL Site
            ---
            tags: ['Site']
            parameters:
              - name: CreateUrlDto
                in: body
                required: true
                schema:
                  id: CreateUrlDto
                  properties:
                    site_url:
                      type: string
                      description: Site Guid
                    space_rule:
                      type: string
                      description: Space rule
                    url_pattern:
                      type: array
                      description: List of URL Pattern
                      items:
                        type: object
                        properties:
                          identifier:
                            type: string
                            description: Endpoint Identifier
                          form_id:
                            type: string
                            nullable: True
                            description: Form Identifier
                          form_type:
                            type: integer
                            nullable: True
                            description: Form Type
                          selection:
                            type: array
                            description: Selection Value
                            nullable: True
                            items:
                              type: object
                              properties:
                                  key:
                                    type: string
                                    description: Key selection
                                  value:
                                    type: string
                                    nullable: True
                                    description: Value selection
            responses:
                200:
                    description: URL Created
                400:
                    description: Invalid request
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

            request_dto = CreateUrlDto(**data)
            result = self._site_service.create_url(request_dto)

            return jsonify({
                'status': 200,
                'message': 'URL generated',
                'data': result
            }), 200

        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def get_sites(self):
        """
            Get All Data
            ---
            tags: ['Site']
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
                    description: List of all data
                500:
                    description: Internal server error
        """
        try:
            page = int(request.args.get('page'))
            limit = int(request.args.get('limit'))
            search = request.args.get('search', "")
            order_by = request.args.get('order_by', 0)
            column_name = request.args.get('column_name', None)

            response = self._site_service.get_all(search, page, limit, order_by, column_name)

            return jsonify({
                'status': 200,
                'message': 'Site get successfully',
                'data': response.data,
                'pagination': vars(response.pagination)
            }), 200

        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def create_site(self):
        """
            Create a new Site
            ---
            tags: ['Site']
            parameters:
              - name: SiteRequestDto
                in: body
                required: true
                schema:
                  id: SiteRequestDto
                  properties:
                    admin_guid:
                      type: string
                      description: Admin Guid
                    site_name:
                      type: string
                      description: Site Name
                    site_url:
                      type: string
                      description: Site URL
                    space_rule:
                      type: string
                      description: Space rule
                      nullable: True
                    url_pattern:
                      type: array
                      description: List of URL Pattern
                      items:
                        type: object
                        properties:
                          identifier:
                            type: string
                            description: Endpoint Identifier
                          form_id:
                            type: string
                            nullable: True
                            description: Form Identifier
                          form_type:
                            type: integer
                            nullable: True
                            description: Form Type
                          selection:
                            type: array
                            description: Selection Value
                            nullable: True
                            items:
                              type: object
                              properties:
                                  key:
                                    type: string
                                    description: Key selection
                                  value:
                                    type: string
                                    nullable: True
                                    description: Value selection
                    data_url_pattern:
                      type: array
                      description: List of Data URL Pattern
                      nullable: True
                      items:
                        type: object
                        properties:
                          identifier:
                            type: string
                            description: Endpoint Identifier
                          value:
                            type: string
                            description: Endpoint Value
                            nullable: True
            responses:
                200:
                    description: Site created successfully
                400:
                    description: Bad request (invalid JSON or missing fields)
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

            request_dto = SiteRequestDto(**data)
            response = self._site_service.create_site(request_dto)

            if not response:
                return jsonify({
                    'status': 500,
                    'message': 'Failed to create data'
                }), 500

            return jsonify({
                'status': 200,
                'message': 'Data created successfully',
                'data': response.to_dict()
            }), 200

        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def update_site(self):
        """
            Update Site
            ---
            tags: ['Site']
            parameters:
              - name: SiteUpdateRequestDto
                in: body
                required: true
                schema:
                  id: SiteUpdateRequestDto
                  properties:
                    guid:
                      type: string
                      description: Site Guid
                    categories_guid:
                      type: array
                      items:
                        type: string
                      description: Categories Guid
                    site_name:
                      type: string
                      description: Site Name
                    site_url:
                      type: string
                      description: Site URL
                    space_rule:
                      type: string
                      description: Space rule
                      nullable: True
                    url_pattern:
                      type: array
                      description: List of URL Pattern
                      items:
                        type: object
                        properties:
                          identifier:
                            type: string
                            description: Endpoint Identifier
                          form_id:
                            type: string
                            nullable: True
                            description: Form Identifier
                          form_type:
                            type: integer
                            nullable: True
                            description: Form Type
                          selection:
                            type: array
                            description: Selection Value
                            nullable: True
                            items:
                              type: object
                              properties:
                                  key:
                                    type: string
                                    description: Key selection
                                  value:
                                    type: string
                                    nullable: True
                                    description: Value selection
                    data_url_pattern:
                      type: array
                      description: List of Data URL Pattern
                      nullable: True
                      items:
                        type: object
                        properties:
                          identifier:
                            type: string
                            description: Endpoint Identifier
                          value:
                            type: string
                            description: Endpoint Value
                            nullable: True
            responses:
                200:
                    description: Site created successfully
                400:
                    description: Bad request (invalid JSON or missing fields)
                404:
                    description: Data not found
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

            request_dto = SiteUpdateRequestDto(**data)

            response = self._site_service.update_site(request_dto)

            if response == -2:
                return jsonify({
                    'status': 404,
                    'message': 'Site not found'
                }), 404
            elif response == 0:
                return jsonify({
                    'status': 400,
                    'message': 'Failed to update'
                }), 400
            elif response == -1:
                return jsonify({
                    'status': 500,
                    'message': 'Internal Server Error'
                }), 500
            return jsonify({
                'status': 200,
                'message': 'Site successfully updated'
            }), 200
        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def update_active_site(self):
        """
            Update Active Site
            ---
            tags: ['Site']
            parameters:
              - name: SiteActiveUpdateDto
                in: body
                required: true
                schema:
                  id: SiteActiveUpdateDto
                  properties:
                    guid:
                      type: string
                      description: Site Guid
                    is_active:
                      type: boolean
                      description: Active Status
            responses:
                200:
                    description: Site updated successfully
                400:
                    description: Bad request (invalid JSON or missing fields)
                404:
                    description: Data not found
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
            request_dto = SiteUpdateActiveDto(**data)
            response = self._site_service.update_active_site(request_dto)
            if response == -2:
                return jsonify({
                    'status': 404,
                    'message': 'Site not found'
                }), 404
            elif response == 0:
                return jsonify({
                    'status': 400,
                    'message': 'Failed to update'
                }), 400
            elif response == -1:
                return jsonify({
                    'status': 500,
                    'message': 'Internal Server Error'
                }), 500
            return jsonify({
                'status': 200,
                'message': 'Site successfully updated'
            }), 200
        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def delete_site(self, guid: str):
        """
            Delete Site
            ---
            tags: ['Site']
            parameters:
              - name: guid
                in: path
                required: true
                type: string
                description: GUID of the site to retrieve
            responses:
                200:
                    description: Site deleted successfully
                404:
                    description: Request not found
                500:
                    description: Internal server error
        """
        try:
            response = self._site_service.delete_site(guid)

            if response == 1:
                return jsonify({
                    'status': 200,
                    'message': 'Site successfully deleted'
                }), 200
            elif response == 0:
                return jsonify({
                    'status': 404,
                    'message': 'Site not found'
                }), 404
            elif response == -1:
                return jsonify({
                    'status': 500,
                    'message': 'Internal server error'
                }), 500
        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500
