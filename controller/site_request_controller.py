from flask import Flask, request, jsonify
from pymongo.database import Database
from dto.site_request.site_request_decline_dto import SiteRequestDeclineDto
from dto.site_request.site_request_request_dto import SiteRequestRequestDto
from dto.site_request.site_request_update_request_dto import SiteRequestUpdateRequestDto
from middleware.auth_middleware import AuthMiddleware
from services.site_request_service import SiteRequestService

class SiteRequestController:
    def __init__(self, app: Flask, db: Database):
        self._site_request_service = SiteRequestService(db)
        self._auth_middleware = AuthMiddleware()

        app.add_url_rule("/request", "get_requests", self._auth_middleware.token_required(self.get_requests),
                         methods=["GET"])
        app.add_url_rule("/request/account/<string:account_guid>", "get_requests_by_account",
                         self._auth_middleware.token_required(self.get_requests_by_account), methods=["GET"])
        app.add_url_rule("/request/<string:guid>", "get_request_by_guid",
                         self._auth_middleware.token_required(self.get_request_by_guid), methods=["GET"])
        app.add_url_rule("/request", "create_request", self._auth_middleware.token_required(self.create_request),
                         methods=["POST"])
        app.add_url_rule("/request", "update_request", self._auth_middleware.token_required(self.update_request),
                         methods=["PUT"])
        app.add_url_rule("/request/<string:guid>", "delete_request",
                         self._auth_middleware.token_required(self.delete_request), methods=["DELETE"])
        app.add_url_rule("/request/accept/<string:guid>", "accept_request",
                         self._auth_middleware.token_required(self.accept_request), methods=["PUT"])
        app.add_url_rule("/request/decline", "decline_request",
                         self._auth_middleware.token_required(self.delete_request), methods=["PUT"])

    def get_requests(self):
        """
            Get All Data
            ---
            tags: ['Site Request']
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

            response = self._site_request_service.get_all(search, page, limit, order_by, column_name)

            return jsonify({
                'status': 200,
                'message': 'Site Requests get successfully',
                'data': response.data,
                'pagination': vars(response.pagination)
            })

        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def get_requests_by_account(self, account_guid: str):
        """
            Get Account Request Data
            ---
            tags: ['Site Request']
            parameters:
              - name: account_guid
                in: path
                required: true
                type: string
                description: GUID of the account to retrieve
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

            response = self._site_request_service.get_by_account(account_guid, search, page, limit, order_by,
                                                                 column_name)

            return jsonify({
                'status': 200,
                'message': 'Category retrieved successfully',
                'data': response.data,
                'pagination': vars(response.pagination)
            }), 200

        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def get_request_by_guid(self, guid: str):
        """
        Get Site Request by GUID
        ---
        tags: ['Site Request']
        parameters:
          - name: guid
            in: path
            required: true
            type: string
            description: GUID of the category to retrieve
        responses:
            200:
                description: Site Request retrieved successfully
            404:
                description: Site Request not found
            500:
                description: Internal server error
        """
        try:
            response = self._site_request_service.get_by_guid(guid)

            if response:
                return jsonify({
                    'status': 200,
                    'message': 'Site Request retrieved successfully',
                    'data': response.__dict__
                }), 200
            else:
                return jsonify({
                    'status': 404,
                    'message': 'Site Request not found'
                }), 404

        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def create_request(self):
        """
            Create a new Site Request
            ---
            tags: ['Site Request']
            parameters:
              - name: SiteRequestRequestDto
                in: body
                required: true
                schema:
                  id: SiteRequestRequestDto
                  properties:
                    account_guid:
                      type: string
                      description: Account Guid
                    subject:
                      type: string
                      description: Subject
                    site_url:
                      type: string
                      description: Site URL
                    description:
                      type: string
                      description: Description
            responses:
                200:
                    description: Site Request created successfully
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

            request_dto = SiteRequestRequestDto(**data)
            response = self._site_request_service.create_request(request_dto)

            if not response:
                return jsonify({
                    'status': 500,
                    'message': 'Failed to create data'
                }), 500

            return jsonify({
                'status': 200,
                'message': 'Site Request created successfully',
                'data': response.to_dict()
            }), 200

        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def update_request(self):
        """
        Update Site Request
        ---
        tags: ['Site Request']
        parameters:
          - name: SiteRequestUpdateRequestDto
            in: body
            required: true
            schema:
              id: SiteRequestUpdateRequestDto
              properties:
                guid:
                  type: string
                  required: true
                  description: Site request GUID
                subject:
                  type: string
                  description: Subject data
                site_url:
                  type: string
                  description: Site URL data
                description:
                  type: string
                  description: Description data
        responses:
            200:
                description: Site Request updated successfully
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

            request_dto = SiteRequestUpdateRequestDto(**data)

            response = self._site_request_service.update_request(request_dto)

            if response == -2:
                return jsonify({
                    'status': 404,
                    'message': 'Site Request not found'
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
                'message': 'Site Request successfully updated'
            }), 200
        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def delete_request(self, guid: str):
        """
            Delete Site Request
            ---
            tags: ['Site Request']
            parameters:
              - name: guid
                in: path
                required: true
                type: string
                description: GUID of the site request to retrieve
            responses:
                200:
                    description: Site Request deleted successfully
                404:
                    description: Request not found
                500:
                    description: Internal server error
        """
        try:
            response = self._site_request_service.delete_request(guid)

            if response == 1:
                return jsonify({
                    'status': 200,
                    'message': 'Site Request successfully deleted'
                }), 200
            elif response == 0:
                return jsonify({
                    'status': 404,
                    'message': 'Site Request not found'
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

    def accept_request(self, guid: str):
        """
        Accept Site Request by GUID
        ---
        tags: ['Site Request']
        parameters:
          - name: guid
            in: path
            required: true
            type: string
            description: GUID of the site request to retrieve
        responses:
            200:
                description: Site Request accepted
            404:
                description: Action failed
            404:
                description: Site Request not found
            500:
                description: Internal server error
        """
        try:
            response = self._site_request_service.accept(guid)

            if response == -2:
                return jsonify({
                    'status': 404,
                    'message': 'Site Request not found'
                }), 404
            elif response == 0:
                return jsonify({
                    'status': 400,
                    'message': 'Failed to accept'
                }), 400
            elif response == -1:
                return jsonify({
                    'status': 500,
                    'message': 'Internal Server Error'
                }), 500
            return jsonify({
                'status': 200,
                'message': 'Site Request successfully accepted'
            }), 200

        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def decline_request(self):
        """
        Decline Site Request
        ---
        tags: ['Site Request']
        parameters:
          - name: SiteRequestUpdateDeclineDto
            in: body
            required: true
            schema:
              id: SiteRequestUpdateDeclineDto
              properties:
                guid:
                  type: string
                  required: true
                  description: Site request GUID
                decline_reason:
                  type: string
                  description: Decline reason data
        responses:
            200:
                description: Site Request updated successfully
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

            request_dto = SiteRequestDeclineDto(**data)

            response = self._site_request_service.decline(request_dto)

            if response == -2:
                return jsonify({
                    'status': 404,
                    'message': 'Site Request not found'
                }), 404
            elif response == 0:
                return jsonify({
                    'status': 400,
                    'message': 'Failed to decline'
                }), 400
            elif response == -1:
                return jsonify({
                    'status': 500,
                    'message': 'Internal Server Error'
                }), 500
            return jsonify({
                'status': 200,
                'message': 'Site Request successfully declined'
            }), 200
        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500
