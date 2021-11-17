from typing import List
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/servers",
    tags=["servers"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ServerOut)
def create_server(server: schemas.ServerIn, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    server_check = db.query(models.Server).filter(
        models.Server.name == server.name).first()

    if server_check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Server with name: {server.name} already exists")

    new_server = models.Server(owner_id=current_user.id, **server.dict())
    db.add(new_server)
    db.commit()
    db.refresh(new_server)

    member = models.Members(user_id=current_user.id, server_id=new_server.id)
    db.add(member)
    db.commit()

    return new_server


@router.get("/{id}", response_model=schemas.ServerOut)
def get_server(id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    server = db.query(models.Server).join(models.User, models.User.id ==
                                          models.Server.owner_id, isouter=True).filter(models.Server.id == id).first()

    if not server:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Server with id: {id} does not exist")

    members = db.query(models.User).join(models.Members, models.User.id ==
                                         models.Members.user_id, isouter=True).filter(models.Members.server_id == id).all()

    members_list = []

    for member in members:
        members_list.append(vars(member))

    server.members = members_list

    return server


@router.post("/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.Member)
def join_server(id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    member_check = db.query(models.Members).filter(
        models.Members.server_id == id, models.Members.user_id == current_user.id).first()

    if member_check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User with id: {current_user.id} already joined server with id: {id}")

    server = db.query(models.Server).filter(models.Server.id == id).first()

    if not server:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Server with id: {id} does not exist")

    new_member = models.Members(user_id=current_user.id, server_id=id)
    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return vars(new_member)


@router.get("/{id}/members", response_model=List[schemas.MemberOut])
def get_server_members(id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    members = db.query(models.Members).join(models.User, models.User.id == models.Members.user_id, isouter=True).filter(
        models.Members.server_id == id).all()

    return members
