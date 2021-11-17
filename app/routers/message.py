from typing import List
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/messages",
    tags=["messages"]
)


@router.post("/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.MessageOut)
def create_message(id: int, message: schemas.MessageIn, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    server = db.query(models.Server).filter(models.Server.id == id).first()

    if not server:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Server with id: {id} does not exist")

    new_message = models.Message(
        server_id=id, author_id=current_user.id, **message.dict())

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return new_message


@router.get("/{id}", response_model=List[schemas.MessageOut])
def get_messages(id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user), limit: int = 50):
    server = db.query(models.Server).filter(models.Server.id == id).first()

    if not server:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Server with id: {id} does not exist")

    messages = db.query(models.Message).filter(
        models.Message.server_id == id).limit(limit).all()

    return messages
