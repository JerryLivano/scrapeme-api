from flask import Flask, jsonify, request
from pymongo.database import Database
from dto.template.template_request_dto import TemplateRequestDto
from dto.template.template_update_request_dto import TemplateUpdateRequestDto
from middleware.auth_middleware import AuthMiddleware
from services.template_service import TemplateService


class TemplateController:
    def __init__(self, app: Flask, db: Database):
        self._template_service = TemplateService(db)
        self._auth_middleware = AuthMiddleware()

        app.add_url_rule("/template/<string:site_guid>", "get_template",
                         self._auth_middleware.token_required(self.get_template), methods=['GET'])
        app.add_url_rule("/template", "create_template", self._auth_middleware.token_required(self.create_template),
                         methods=['POST'])
        app.add_url_rule("/template", "update_template", self._auth_middleware.token_required(self.update_template),
                         methods=['PUT'])
        app.add_url_rule("/template", "delete_template", self._auth_middleware.token_required(self.delete_template),
                         methods=['DELETE'])

    def get_template(self, site_guid: str):
        """
        Get Template by Site GUID
        ---
        tags: ['Template']
        parameters:
          - name: guid
            in: path
            required: true
            type: string
            description: GUID of the template to retrieve
        responses:
            200:
                description: Template retrieved successfully
            404:
                description: Template not found
            500:
                description: Internal server error
        """
        try:
            template = self._template_service.get_by_site_guid(site_guid)

            if template:
                return jsonify({
                    'status': 200,
                    'message': 'Template retrieved successfully',
                    'data': template.__dict__
                }), 200
            else:
                return jsonify({
                    'status': 404,
                    'message': 'Template not found'
                }), 404

        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def create_template(self):
        """
            Create a new Template
            ---
            tags: ['Template']
            parameters:
              - name: TemplateRequestDto
                in: body
                required: true
                schema:
                  id: TemplateRequestDto
                  properties:
                    site_guid:
                      type: string
                      description: Site Guid
                    container:
                      type: string
                      description: Container
                    is_class:
                      type: boolean
                      description: Container type
                    is_id:
                      type: boolean
                      description: Container type
                    is_tag:
                      type: boolean
                      description: Container type
                    tag_data:
                      type: array
                      description: List of Tag Data
                      items:
                        type: object
                        properties:
                          identifier:
                            type: string
                            description: Tag Identifier
                          is_class:
                            type: boolean
                            nullable: True
                            description: Class tag
                          is_id:
                            type: boolean
                            nullable: True
                            description: Tag id
                          is_tag:
                            type: boolean
                            nullable: True
                            description: Tag name
                          image:
                            type: array
                            description: Image list
                            nullable: True
                            items:
                              type: string
                              description: Image source
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

            request_dto = TemplateRequestDto(**data)
            response = self._template_service.create_template(request_dto)

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

    def update_template(self):
        """
            Update Template
            ---
            tags: ['Template']
            parameters:
              - name: TemplateUpdateRequestDto
                in: body
                required: true
                schema:
                  id: TemplateUpdateRequestDto
                  properties:
                    guid:
                      type: string
                      description: Template Guid
                    container:
                      type: string
                      description: Container
                    is_class:
                      type: boolean
                      description: Container type
                    is_id:
                      type: boolean
                      description: Container type
                    is_tag:
                      type: boolean
                      description: Container type
                    tag_data:
                      type: array
                      description: List of Tag Data
                      items:
                        type: object
                        properties:
                          identifier:
                            type: string
                            description: Tag Identifier
                          is_class:
                            type: boolean
                            nullable: True
                            description: Class tag
                          is_id:
                            type: boolean
                            nullable: True
                            description: Tag id
                          is_tag:
                            type: boolean
                            nullable: True
                            description: Tag name
                          image:
                            type: array
                            description: Image list
                            nullable: True
                            items:
                              type: string
                              description: Image source
            responses:
                200:
                    description: Data updated successfully
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

            request_dto = TemplateUpdateRequestDto(**data)
            response = self._template_service.update_template(request_dto)

            if response == -2:
                return jsonify({
                    'status': 404,
                    'message': 'Data not found'
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
                'message': 'Data successfully updated'
            }), 200
        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def delete_template(self, guid: str):
        """
            Delete Template
            ---
            tags: ['Template']
            parameters:
              - name: guid
                in: path
                required: true
                type: string
                description: GUID of the data to retrieve
            responses:
                200:
                    description: Data deleted successfully
                404:
                    description: Request not found
                500:
                    description: Internal server error
        """
        try:
            response = self._template_service.delete_template(guid)
            if response == 1:
                return jsonify({
                    'status': 200,
                    'message': 'Data successfully deleted'
                }), 200
            elif response == 0:
                return jsonify({
                    'status': 404,
                    'message': 'Data not found'
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
