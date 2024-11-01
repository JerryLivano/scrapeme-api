class Category:
    def __init__(self, guid: str, category_name: str):
        self.guid = guid
        self.category_name = category_name

    def to_dict(self):
        return {
            'guid': self.guid,
            'category_name': self.category_name
        }