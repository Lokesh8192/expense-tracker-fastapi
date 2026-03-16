from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from sqlalchemy.orm import Session

from app.core.config import SECRET_KEY, ALGORITHM
from app.database.database import get_db
from app.models.user_model import User

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = (
            db.query(User)
            .filter(User.username == username, User.deleted == False)
            .first()
        )

        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")

        return user

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
