class ChangePasswordRequestDto:
    def __init__(self, guid: str, password: str, confirm_password: str):
        self.guid = guid
        self.password = password
        self.confirm_password = confirm_password