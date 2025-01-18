from flask import jsonify, request, Response, Flask
from pymongo.synchronous.database import Database
from dto.scrape_data.create_site_url_dto import CreateSiteUrlDto
from dto.scrape_data.scrape_data_dto import ScrapeDataDto
from middleware.auth_middleware import AuthMiddleware
from services.parse_html_service import ParseHTMLService


class ParseHTMLController:
    def __init__(self, app: Flask, db: Database):
        self._parse_service = ParseHTMLService(db)
        self._auth_middleware = AuthMiddleware()

        app.add_url_rule('/scrape/parse-html', 'parse_html', self.parse_html,
                         methods=['POST'])
        app.add_url_rule("/scrape/create-url", "create_site_url", self.create_site_url, methods=["POST"])
        app.add_url_rule("/scrape/scrape-data", "scrape_data", self.scrape_data, methods=["POST"])

    def create_site_url(self):
        """
            Create Site URL
            ---
            tags: ['Parse HTML']
            parameters:
              - name: CreateSiteUrlDto
                in: body
                required: true
                schema:
                  id: CreateSiteUrlDto
                  properties:
                    site_url:
                      type: string
                      description: Site URL
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
                          is_increment:
                            type: boolean
                            nullable: True
                            description: increment page
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
                    space_rule:
                      type: string
                      description: Space Rule
            responses:
                200:
                    description: Successfully created
                400:
                    description: Failed to create
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

            request_dto = CreateSiteUrlDto(**data)
            response = self._parse_service.create_site_url(request_dto)

            if not response:
                return jsonify({
                    'status': 500,
                    'message': 'Failed to create URL'
                }), 500

            return jsonify({
                'status': 200,
                'message': 'Data created successfully',
                'data': response
            }), 200

        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def parse_html(self):
        """
        Parse HTML from given URL
        ---
        tags: ['Parse HTML']
        parameters:
          - name: url
            in: body
            required: true
            schema:
              id: URLRequest
              properties:
                url:
                  type: string
                  description: Site URL
        responses:
          200:
            description: Data exported successfully
          400:
            description: Failed to export data
          500:
            description: Internal server error
        """
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 400,
                'message': 'URL parameter is required'
            }), 400
        try:
            result = self._parse_service.get_html_source(data["url"])
            if result:
                return jsonify({
                    'status': 200,
                    'message': 'Source successfully scraped',
                    'data': str(result.prettify())
                }), 200
            else:
                return jsonify({
                    'status': 400,
                    'message': 'Failed to scrape URL data'
                }), 400

        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def scrape_data(self):
        """
            Create Site URL
            ---
            tags: ['Parse HTML']
            parameters:
              - name: ScrapeDataDto
                in: body
                required: true
                schema:
                  id: ScrapeDataDto
                  properties:
                    site_guid:
                      type: string
                      description: Site GUID
                    account_guid:
                      type: string
                      description: Account GUID
                    limit_data:
                      type: integer
                      description: Limit Data
                    scrape_name:
                      type: string
                      description: Scrape Name
                    site_url:
                      type: string
                      description: Site URL
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
                          is_increment:
                            type: boolean
                            nullable: True
                            description: increment page
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
                    space_rule:
                      type: string
                      description: Space Rule
            responses:
                200:
                    description: Successfully created
                400:
                    description: Failed to create
                404:
                    description: template not found
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

            request_dto = ScrapeDataDto(**data)
            response = self._parse_service.scrape_data(request_dto)

            if response == -1:
                return jsonify({
                    'status': 404,
                    'message': 'Template not found',
                }), 404
            if response == 0:
                return jsonify({
                    'status': 400,
                    'message': 'Failed to create data',
                }), 400

            return jsonify({
                'status': 200,
                'message': 'Data created successfully',
                'data': response.__dict__
            }), 200

        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    # def export_excel(self):
    #     """
    #     Export scraped data to an Excel file
    #     ---
    #     tags: ['Scrape']
    #     responses:
    #       200:
    #         description: Data exported successfully
    #       400:
    #         description: Failed to export data
    #       500:
    #         description: Internal server error
    #     """
    #     try:
    #         scrap_service = ScrapService()
    #         result = scrap_service.export_excel()
    #
    #         if result:
    #             return jsonify({
    #                 'status': 200,
    #                 'message': 'Data exported successfully'
    #             }), 200
    #         else:
    #             return jsonify({
    #                 'status': 400,
    #                 'message': 'Failed to export data'
    #             }), 400
    #     except Exception as e:
    #         return jsonify({
    #             'status': 500,
    #             'message': f'Error occurred: {str(e)}'
    #         }), 500
