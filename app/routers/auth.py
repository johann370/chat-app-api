from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.exceptions import HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import false
from starlette.responses import JSONResponse
from .. import schemas, models, utils, oauth2
from ..database import get_db

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    content = {"access_token": access_token,
               "token_type": "bearer", "user_id": user.id}
    response = JSONResponse(content=content)
    response.set_cookie(key="access_token", value=access_token, httponly=False)

    return response
