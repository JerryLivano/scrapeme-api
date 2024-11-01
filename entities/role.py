from bson import ObjectId

class Role:
    def __init__(self, guid: str, role_name: str):
        self.guid = guid
        self.role_name = role_name

    def to_dict(self):
        return {
            "guid": self.guid,
            "role_name": self.role_name
        }