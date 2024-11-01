class CategoryUpdateRequestDto:
    def __init__(self, guid: str, category_name: str):
        self.guid = guid
        self.category_name = category_name
