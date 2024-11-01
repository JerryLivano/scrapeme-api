from datetime import datetime, timedelta
import jwt
from dto.account.token_request_dto import TokenRequestDto

class JWTHandler:
    def __init__(self):
        self.key = "secret"

    def generate_token(self, user_data: TokenRequestDto) -> str | None:
        if not user_data:
            return None

        try:
            claims = {
                "guid": user_data.guid,
                "name": user_data.fullname[0],
                "email": user_data.email[0],
                "role": user_data.role,
                "sub": user_data.sub_guid,
                "iss": "https://localhost:5000",
                "iat": datetime.utcnow(),
                "exp": datetime.utcnow() + timedelta(hours=48)
            }

            token = jwt.encode(claims, self.key, algorithm="HS256")
            return token
        except Exception as e:
            print(f"Token generation error: {str(e)}")
            return None

    def decode_token(self, token: str) -> dict | None:
        try:
            decoded_token = jwt.decode(token, self.key, algorithms=["HS256"], issuer="https://localhost:5000")
            return decoded_token
        except jwt.ExpiredSignatureError:
            print("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            print(f"Invalid token: {str(e)}")
            return None
