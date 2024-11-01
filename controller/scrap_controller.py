from flask import jsonify, request, Response
from services.scrape_service import ScrapService

class ScrapController:
    def __init__(self, app):
        app.add_url_rule('/scrape/get_data', 'scrap_data', self.scrap_data, methods=['GET'])
        app.add_url_rule('/scrape/parse_html', 'parse_html', self.parse_html, methods=['GET'])
        app.add_url_rule('/scrape/export_excel', 'export_excel', self.export_excel, methods=['POST'])

    def scrap_data(self):
        """
        Scrape data from a given URL
        ---
        tags: ['Scrape']
        parameters:
          - name: url
            in: query
            type: string
            required: true
            description: The URL to scrape data from
        responses:
          200:
            description: Data exported successfully
          400:
            description: Failed to export data
          500:
            description: Internal server error
        """
        url = request.args.get('url')
        if not url:
            return jsonify({
                'status': 400,
                'message': 'URL parameter is required'
            }), 400

        try:
            scrap_service = ScrapService()
            result = scrap_service.scrap_data(url)

            return jsonify({
                'status': 200,
                'message': 'Successfully scraped data',
                'data': [{'name': data.name, 'image': data.image, 'price': data.price} for data in result]
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
        tags: ['Scrape']
        parameters:
          - name: url
            in: query
            type: string
            required: true
            description: The URL to scrape data from
        responses:
          200:
            description: Data exported successfully
          400:
            description: Failed to export data
          500:
            description: Internal server error
        """
        url = request.args.get('url')
        if not url:
            return jsonify({
                'status': 400,
                'message': 'URL parameter is required'
            }), 400

        try:
            scrap_service = ScrapService()
            result = scrap_service.parse_html(url)

            if result:
                return Response(result, mimetype='text/html')
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

    def export_excel(self):
        """
        Export scraped data to an Excel file
        ---
        tags: ['Scrape']
        responses:
          200:
            description: Data exported successfully
          400:
            description: Failed to export data
          500:
            description: Internal server error
        """
        try:
            scrap_service = ScrapService()
            result = scrap_service.export_excel()

            if result:
                return jsonify({
                    'status': 200,
                    'message': 'Data exported successfully'
                }), 200
            else:
                return jsonify({
                    'status': 400,
                    'message': 'Failed to export data'
                }), 400
        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500