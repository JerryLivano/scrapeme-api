from entities.account import Account
from entities.role import Role
from entities.user import User

class AccountResponseDto:
    def __init__(self, account: Account, user: User, role: Role):
        self.guid = account.guid
        self.user = user.to_dict() if user else None
        self.role = role.to_dict() if role else None
        self.password = account.password
        self.is_active = account.is_active
        self.created_by = account.created_by
        self.created_date = account.created_date