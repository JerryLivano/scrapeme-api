from flask import jsonify, request, Flask
from pymongo.database import Database
from dto.category.category_add_request_dto import CategoryAddRequestDto
from dto.category.category_update_request_dto import CategoryUpdateRequestDto
from middleware.auth_middleware import AuthMiddleware
from services.category_service import CategoryService

class CategoryController:
    def __init__(self, app: Flask, db: Database):
        self._category_service = CategoryService(db)
        self._auth_middleware = AuthMiddleware()

        app.add_url_rule('/category', 'get_categories', self._auth_middleware.token_required(self.get_categories), methods=['GET'])
        app.add_url_rule('/category/<string:guid>', 'get_category_by_guid', self._auth_middleware.token_required(self.get_category_by_guid), methods=['GET'])
        app.add_url_rule('/category', 'create_category', self._auth_middleware.token_required(self.create_category), methods=['POST'])
        app.add_url_rule('/category', 'update_category', self._auth_middleware.token_required(self.update_category), methods=['PUT'])
        app.add_url_rule('/category/<string:guid>', 'delete_category', self._auth_middleware.token_required(self.delete_category), methods=['DELETE'])

    def get_categories(self):
        """
            Get All Categories Data
            ---
            tags: ['Category']
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
                    description: List of all categories
                500:
                    description: Internal server error
        """
        try:
            page = int(request.args.get('page'))
            limit = int(request.args.get('limit'))
            search = request.args.get('search', "")
            order_by = request.args.get('order_by', 0)
            column_name = request.args.get('column_name', None)

            response = self._category_service.get_all(search, page, limit, order_by, column_name)

            return jsonify({
                'status': 200,
                'message': 'Categories get successfully',
                'data': response.data,
                'pagination': vars(response.pagination)
            })

        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def get_category_by_guid(self, guid: str):
        """
        Get Category by GUID
        ---
        tags: ['Category']
        parameters:
          - name: guid
            in: path
            required: true
            type: string
            description: GUID of the category to retrieve
        responses:
            200:
                description: Category retrieved successfully
            404:
                description: Category not found
            500:
                description: Internal server error
        """
        try:
            category = self._category_service.get_by_guid(guid)

            if category:
                return jsonify({
                    'status': 200,
                    'message': 'Category retrieved successfully',
                    'data': category.__dict__
                }), 200
            else:
                return jsonify({
                    'status': 404,
                    'message': 'Category not found'
                }), 404

        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def create_category(self):
        """
            Create a new Category
            ---
            tags: ['Category']
            parameters:
              - name: CategoryAddRequestDto
                in: body
                required: true
                schema:
                  id: CategoryAddRequestDto
                  properties:
                    category_name:
                      type: string
                      description: Name of the category to create
            responses:
                200:
                    description: Category created successfully
                400:
                    description: Bad request (invalid JSON or missing fields)
                500:
                    description: Internal server error
        """
        try:
            data = request.get_json()

            if not data or 'category_name' not in data:
                return jsonify({
                    'status': 400,
                    'message': 'Invalid request payload or missing category_name'
                }), 400

            category_request_dto = CategoryAddRequestDto(**data)

            new_category = self._category_service.create_category(category_request_dto)

            if new_category:
                return jsonify({
                    'status': 200,
                    'message': 'Category created successfully',
                    'data': new_category.to_dict()
                }), 200
            else:
                return jsonify({
                    'status': 500,
                    'message': 'Failed to create category'
                }), 500

        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def update_category(self):
        """
            Update Category
            ---
            tags: ['Category']
            parameters:
              - name: CategoryUpdateRequestDto
                in: body
                required: true
                schema:
                  id: CategoryUpdateRequestDto
                  properties:
                    guid:
                      type: string
                      required: true
                      description: category GUID
                    category_name:
                      type: string
                      description: Name of the category to create
            responses:
                200:
                    description: Category updated successfully
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

            category_request_dto = CategoryUpdateRequestDto(**data)

            result = self._category_service.update_category(category_request_dto)

            if result == -2:
                return jsonify({
                    'status': 404,
                    'message': 'Category not found'
                }), 404
            elif result == 0:
                return jsonify({
                    'status': 400,
                    'message': 'Failed to update category'
                }), 400
            elif result == -1:
                return jsonify({
                    'status': 500,
                    'message': 'Internal Server Error'
                }), 500
            return jsonify({
                'status': 200,
                'message': 'Category successfully updated'
            }), 200
        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500

    def delete_category(self, guid: str):
        """
            Delete Category
            ---
            tags: ['Category']
            parameters:
              - name: guid
                in: path
                required: true
                type: string
                description: GUID of the category to retrieve
            responses:
                200:
                    description: Category deleted successfully
                404:
                    description: Request not found
                500:
                    description: Internal server error
        """
        try:
            result = self._category_service.delete_category(guid)

            if result == 1:
                return jsonify({
                    'status': 200,
                    'message': 'Category successfully deleted'
                }), 200
            elif result == 0:
                return jsonify({
                    'status': 404,
                    'message': 'Category not found'
                }), 404
            elif result == -1:
                return jsonify({
                    'status': 500,
                    'message': 'Internal server error'
                }), 500
        except Exception as e:
            return jsonify({
                'status': 500,
                'message': f'Error occurred: {str(e)}'
            }), 500
