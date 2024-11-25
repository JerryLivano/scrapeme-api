from flask import Flask, jsonify
from pymongo.database import Database
from middleware.auth_middleware import AuthMiddleware
from services.dashboard_service import DashboardService


class DashboardController:
    def __init__(self, app: Flask, db: Database):
        self._dashboard_service = DashboardService(db)
        self._auth_middleware = AuthMiddleware()

        app.add_url_rule("/dashboard/count", "get_count", self._auth_middleware.token_required(self.get_count),
                         methods=["GET"])

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
