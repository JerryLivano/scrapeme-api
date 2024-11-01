from datetime import datetime

class Account:
    def __init__(self, guid: str, user_guid: str, role_guid: str | None, password: str, is_active: bool, created_by: str, created_date: datetime):
        self.guid = guid
        self.user_guid = user_guid
        self.role_guid = role_guid
        self.password = password
        self.is_active = is_active
        self.created_by = created_by
        self.created_date = created_date

    def to_dict(self):
        return {
            'guid': self.guid,
            'user_guid': self.user_guid,
            'role_guid': self.role_guid,
            'password': self.password,
            'is_active': self.is_active,
            'created_by': self.created_by,
            'created_date': self.created_date
        }