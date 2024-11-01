class PaginationInfo:
    def __init__(self, total_records: int, current_page: int, total_pages: int, next_page: bool, prev_page: bool):
        self.total_records = total_records
        self.current_page = current_page
        self.total_pages = total_pages
        self.next_page = next_page
        self.prev_page = prev_page
