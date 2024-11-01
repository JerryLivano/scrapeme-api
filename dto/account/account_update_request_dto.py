class AccountUpdateRequestDto:
    def __init__(self, guid: str, first_name: str, last_name: str, email: str, is_active: bool, role_guid: str | None = None):
        self.guid = guid
        self.first_name = first_name,
        self.last_name = last_name,
        self.email = email,
        self.is_active = is_active,
        self.role_guid = role_guid