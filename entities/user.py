class User:
    def __init__(self, guid: str, first_name: str, last_name: str, email: str):
        self.guid = guid
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def full_name(self) -> str:
        return f"{self.first_name.strip()}{(" " + self.last_name.strip()) if self.last_name else ""}"

    def to_dict(self):
        return {
            'guid': self.guid,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }
