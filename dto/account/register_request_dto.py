class RegisterRequestDto:
    def __init__(self, first_name: str, email: str, password: str, confirm_password: str, role_guid: str, last_name: str = None, created_by: str = "root"):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.confirm_password = confirm_password
        self.created_by = created_by
        self.role_guid = role_guid