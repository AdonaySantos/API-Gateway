from fastapi import HTTPException, Request
from core.dotenv_config import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError, ExpiredSignatureError

async def auth_token(request: Request):
    auth_header: str | None = request.headers.get('Authorization')
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authentication token is missing")

    try:
        token = auth_header.split()[1]
        _ = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication token.")
    except Exception:
        raise HTTPException(status_code=401, detail="Error while verifying authentication token.")
