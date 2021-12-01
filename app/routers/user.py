from typing import List
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserIn, db: Session = Depends(get_db)):

    user_check = db.query(models.User).filter(
        models.User.email == user.email).first()

    if user_check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User with email: {user.email} already exists")

    hashed_password = utils.get_password_hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user


@router.get("/{id}/servers", response_model=List[schemas.UserServer])
def get_joined_servers(id: int, db: Session = Depends(get_db)):
    joined_servers = db.query(models.Members).join(models.Server, models.Server.id == models.Members.server_id, isouter=True).filter(
        models.Members.user_id == id).all()

    if not joined_servers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not have any joined_servers")

    return joined_servers
