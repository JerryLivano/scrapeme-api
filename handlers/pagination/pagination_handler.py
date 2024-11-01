from handlers.pagination.pagination_info import PaginationInfo
from handlers.pagination.response_pagination_handler import ResponsePaginationHandler

class PaginationHandler:
    @staticmethod
    def paginate(queryable, transform_function, page, limit):
        total_records = len(queryable)
        total_pages = (total_records + limit - 1) // limit
        items_to_skip = (page - 1) * limit

        if items_to_skip >= total_records:
            return ResponsePaginationHandler(
                data=[],
                pagination=PaginationInfo(total_records, page, total_pages, None, None)
            )

        paginated_data = queryable[items_to_skip: items_to_skip + limit]
        transformed_data = [transform_function(item, i + items_to_skip + 1) for i, item in enumerate(paginated_data)]

        next_page = page + 1 if page < total_pages else None
        prev_page = page - 1 if page > 1 else None

        pagination_info = PaginationInfo(
            total_records=total_records,
            current_page=page,
            total_pages=total_pages,
            next_page=next_page,
            prev_page=prev_page
        )

        return ResponsePaginationHandler(
            data=transformed_data,
            pagination=pagination_info
        )
