from entities.role import Role

class TokenRequestDto:
    def __init__(self, guid: str, sub_guid: str, fullname: str, email: str, role: Role):
        self.guid = guid
        self.sub_guid = sub_guid
        self.fullname = fullname,
        self.email = email,
        self.role = role.to_dict()