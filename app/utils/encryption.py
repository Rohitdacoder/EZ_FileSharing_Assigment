import jwt
import datetime
from jwt import ExpiredSignatureError, InvalidTokenError

# Secret key to sign tokens (keep it safe & secret in env variables in production)
SECRET_KEY = "your-very-secure-secret-key"

def generate_secure_token(user_id: str, file_id: str, expires_in_minutes=60) -> str:
    """
    Generate a JWT token containing user_id, file_id, and expiry time.
    This token will be used as an encrypted URL part.
    """
    payload = {
        "user_id": user_id,
        "file_id": file_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_in_minutes)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def verify_secure_token(token: str) -> dict:
    """
    Verify and decode the JWT token.
    Returns the decoded payload if valid.
    Raises Exception if invalid or expired.
    """
    try:
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_payload
    except ExpiredSignatureError:
        raise Exception("Token has expired")
    except InvalidTokenError:
        raise Exception("Invalid token")

