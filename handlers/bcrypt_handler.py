import bcrypt

class BCryptHandler:
    def generate_salt(self):
        return bcrypt.gensalt(rounds=12)

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), self.generate_salt())

    def verify_password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))