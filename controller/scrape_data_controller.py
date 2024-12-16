from flask import Flask, request, jsonify, Response
from pymongo.database import Database

from dto.scrape_data.update_fav_dto import UpdateFavDto
from dto.scrape_data.update_name_dto import UpdateNameDto
from dto.scrape_data.update_note_dto import UpdateNoteDto
from middleware.auth_middleware import AuthMiddleware
from services.scrape_data_service import ScrapeDataService


class ScrapeDataController:
    def __init__(self, app: Flask, db: Database):
        self._auth_middleware = AuthMiddleware()
        self._scrape_service = ScrapeDataService(db)

        app.add_url_rule("/scrape/account", "get_by_account", self._auth_middleware.token_required(self.get_by_account),
                         methods=["GET"])
        app.add_url_rule("/scrape/web-data", "get_web_data", self._auth_middleware.token_required(self.get_web_data),
                         methods=["GET"])
        app.add_url_rule("/scrape/favorite", "get_fav_scrape",
                         self._auth_middleware.token_required(self.get_fav_scrape),
                         methods=["GET"])
        app.add_url_rule("/scrape/favorite-web-data", "get_fav_web_data",
                         self._auth_middleware.token_required(self.get_fav_web_data),
                         methods=["GET"])
        app.add_url_rule("/scrape/update-favorite", "update_web_data_fav",
                         self._auth_middleware.token_required(self.update_web_data_fav), methods=["PUT"])
        app.add_url_rule("/scrape/update-note", "update_web_data_note",
                         self._auth_middleware.token_required(self.update_web_data_note), methods=["PUT"])
        app.add_url_rule("/scrape/update-name", "update_scrape_name",
                         self._auth_middleware.token_required(self.update_scrape_name), methods=["PUT"])
        app.add_url_rule("/scrape/<string:guid>", "delete_scrape",
                         self._auth_middleware.token_required(self.delete_scrape), methods=["DELETE"])

    def get_by_account(self):
        """
            Get All Data
            ---
            tags: ['Scrape Data']
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
              - name: account_guid
                in: query
                type: string
                required: True
                description: Account GUID
              - name: site_guid
                in: query
                type: string
                description: Site GUID
            responses:
                200:
                    description: List of all data
                500:
                    description: Internal server error
        """
        try:
            search = request.args.get('search', "")
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 10))
            order_by = request.args.get('order_by', 0)
            column_name = request.args.get('column_name', None)
            account_guid = request.args.get('account_guid')
            site_guid = request.args.get('site_guid', '')

            response = self._scrape_service.get_by_account(account_guid, search, page, limit, order_by, column_name,
                                                           site_guid)

            return jsonify({
                'status': 200,
                'message': 'Scrape History get successfully',
                'data': response.data,
                'pagination': vars(response.pagination)
            }), 200

        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def get_web_data(self):
        """
            Get All Web Data
            ---
            tags: ['Scrape Data']
            parameters:
              - name: guid
                in: query
                type: string
                description: Scrape Guid
              - name: page
                in: query
                type: integer
                description: Page query
              - name: limit
                in: query
                type: integer
                description: Limit query
              - name: search
                in: query
                type: string
                description: Search query
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
            guid = request.args.get('guid')
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 10))
            search = request.args.get('search', '')
            order_by = request.args.get('order_by', 0)
            column_name = request.args.get('column_name', None)

            response = self._scrape_service.get_all_web_data(guid, search, page, limit, order_by, column_name)

            return jsonify({
                'status': 200,
                'message': 'Web Data get successfully',
                'data': response.data,
                'pagination': vars(response.pagination)
            }), 200

        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def get_fav_scrape(self):
        """
            Get All Fav Data
            ---
            tags: ['Scrape Data']
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
              - name: account_guid
                in: query
                type: string
                required: True
                description: Account GUID
              - name: site_guid
                in: query
                type: string
                description: Site GUID
            responses:
                200:
                    description: List of all data
                500:
                    description: Internal server error
        """
        try:
            search = request.args.get('search', "")
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 10))
            order_by = request.args.get('order_by', 0)
            column_name = request.args.get('column_name', None)
            account_guid = request.args.get('account_guid')
            site_guid = request.args.get('site_guid', '')

            response = self._scrape_service.get_fav_scrape_data(account_guid, search, page, limit, order_by,
                                                                column_name,
                                                                site_guid)

            return jsonify({
                'status': 200,
                'message': 'Scrape History get successfully',
                'data': response.data,
                'pagination': vars(response.pagination)
            }), 200

        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def get_fav_web_data(self):
        """
            Get All Fav Web Data
            ---
            tags: ['Scrape Data']
            parameters:
              - name: guid
                in: query
                type: string
                description: Scrape Guid
              - name: page
                in: query
                type: integer
                description: Page query
              - name: limit
                in: query
                type: integer
                description: Limit query
              - name: search
                in: query
                type: string
                description: Search query
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
            guid = request.args.get('guid')
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 10))
            search = request.args.get('search', '')
            order_by = request.args.get('order_by', 0)
            column_name = request.args.get('column_name', None)

            response = self._scrape_service.get_all_fav_web_data(guid, search, page, limit, order_by, column_name)

            return jsonify({
                'status': 200,
                'message': 'Web Data get successfully',
                'data': response.data,
                'pagination': vars(response.pagination)
            }), 200

        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def update_scrape_name(self):
        """
            Update Scrape Name
            ---
            tags: ['Scrape Data']
            parameters:
              - name: UpdateNameDto
                in: body
                required: true
                schema:
                  id: UpdateNameDto
                  properties:
                    guid:
                      type: string
                      description: Scrape Guid
                    scrape_name:
                      type: string
                      description: Scrape Name
            responses:
                200:
                    description: Data updated successfully
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

            request_dto = UpdateNameDto(**data)
            response = self._scrape_service.update_scrape(request_dto)

            if not response:
                return jsonify({
                    'status': 500,
                    'message': 'Failed to create data'
                }), 500

            return jsonify({
                'status': 200,
                'message': 'Data updated successfully'
            }), 200

        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def update_web_data_note(self):
        """
            Update Web Data Note
            ---
            tags: ['Scrape Data']
            parameters:
              - name: UpdateNoteDto
                in: body
                required: true
                schema:
                  id: UpdateNoteDto
                  properties:
                    guid:
                      type: string
                      description: Scrape Guid
                    index:
                      type: integer
                      description: Scrape Index
                    note:
                      type: string
                      description: Scrape Note
            responses:
                200:
                    description: Data updated successfully
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

            request_dto = UpdateNoteDto(**data)
            response = self._scrape_service.update_note(request_dto)

            if response == 0:
                return jsonify({
                    'status': 400,
                    'message': 'Failed to update data'
                }), 400

            return jsonify({
                'status': 200,
                'message': 'Note data updated successfully'
            }), 200
        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def update_web_data_fav(self):
        """
            Update Web Data Fav
            ---
            tags: ['Scrape Data']
            parameters:
              - name: UpdateFavDto
                in: body
                required: true
                schema:
                  id: UpdateFavDto
                  properties:
                    guid:
                      type: string
                      description: Scrape Guid
                    index:
                      type: integer
                      description: Scrape Index
                    is_favourite:
                      type: boolean
                      description: Favourite Status
            responses:
                200:
                    description: Data updated successfully
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

            request_dto = UpdateFavDto(**data)
            response = self._scrape_service.update_fav(request_dto)

            if response == 0:
                return jsonify({
                    'status': 400,
                    'message': 'Failed to update data'
                }), 400

            return jsonify({
                'status': 200,
                'message': 'Fav data updated successfully'
            }), 200
        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def delete_scrape(self, guid: str):
        """
            Delete Scrape
            ---
            tags: ['Scrape Data']
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
            response = self._scrape_service.delete_scrape(guid)

            if not response:
                return jsonify({
                    'status': 500,
                    'message': 'Data not found'
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
