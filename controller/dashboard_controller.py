from flask import Flask, jsonify, request
from pymongo.database import Database
from middleware.auth_middleware import AuthMiddleware
from services.dashboard_service import DashboardService


class DashboardController:
    def __init__(self, app: Flask, db: Database):
        self._dashboard_service = DashboardService(db)
        self._auth_middleware = AuthMiddleware()

        app.add_url_rule("/dashboard/count", "get_count", self._auth_middleware.token_required(self.get_count),
                         methods=["GET"])
        app.add_url_rule("/dashboard/top-scraper", "get_top_scraper",
                         self._auth_middleware.token_required(self.get_top_scraper),
                         methods=["GET"])
        app.add_url_rule("/dashboard/statistic", "get_scrape_statistic", self.get_scrape_statistic, methods=["GET"])

    def get_count(self):
        """
            Get All Dashboard Count
            ---
            tags: ['Dashboard']
            responses:
                200:
                    description: List of all count
                500:
                    description: Internal server error
        """
        try:
            response = self._dashboard_service.get_dashboard_count()
            return jsonify({
                'status': 200,
                'message': 'Categories get successfully',
                'data': response.__dict__
            })

        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def get_top_scraper(self):
        """
            Get Top Scraper
            ---
            tags: ['Dashboard']
            responses:
                200:
                    description: List of all count
                500:
                    description: Internal server error
        """
        try:
            response = self._dashboard_service.get_top_scraper()
            return jsonify({
                'status': 200,
                'message': 'Data get successfully',
                'data': [data.__dict__ for data in response]
            }), 200

        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def get_scrape_statistic(self):
        """
        Get Scrape Statistic
        ---
        tags: ['Dashboard']
        parameters:
          - name: year
            in: query
            required: true
            type: integer
            description: Year Params
        responses:
            200:
                description: Data retrieved successfully
            404:
                description: Not found
            500:
                description: Internal server error
        """
        try:
            year = int(request.args.get('year'))
            if not year:
                return jsonify({
                    'status': 400,
                    'message': 'Year parameter is required'
                }), 400

            result = self._dashboard_service.get_scrape_statistic(year)
            if not result:
                return jsonify({
                    'status': 404,
                    'message': 'Data not found'
                }), 404

            return jsonify({
                'status': 200,
                'message': "Data get successfully",
                'data': [data.__dict__ for data in result]
            }), 200

        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500
