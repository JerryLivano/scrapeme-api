from flask_cors import CORS

class CorsMiddleware:
    def __init__(self, app):
        self.cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})