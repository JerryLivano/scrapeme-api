from flask import Flask, redirect
from flasgger import Swagger
from controller.account_controller import AccountController
from controller.category_controller import CategoryController
from controller.dashboard_controller import DashboardController
from controller.role_controller import RoleController
from controller.scrap_controller import ScrapController
from controller.site_controller import SiteController
from controller.site_request_controller import SiteRequestController
from controller.template_controller import TemplateController
from db_context.mongo_db_connection import MongoDBConnection
from middleware.cors_middleware import CorsMiddleware

SWAGGER_TEMPLATE = {
    "info": {
        "title": "API Documentation",
        "description": "API documentation with Bearer Token authentication",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ]
}

# Init app and swagger
app = Flask(__name__)
swagger = Swagger(app, template=SWAGGER_TEMPLATE)

# Middleware
cors = CorsMiddleware(app)

# Database init
mongo_connection = MongoDBConnection()
db = mongo_connection.get_database()

# Controller registered
with app.app_context():
    ScrapController(app)
    RoleController(app, db)
    AccountController(app, db)
    # CategoryController(app, db)
    SiteRequestController(app, db)
    SiteController(app, db)
    TemplateController(app, db)
    DashboardController(app, db)

@app.route('/')
def index():
    return redirect('/apidocs')

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
