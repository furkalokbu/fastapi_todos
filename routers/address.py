import sys
sys.path.append('..')

from typing import Optional, Annotated
from pydantic import BaseModel
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from .auth import get_current_user
import models
from database import engine, SessionLocal


router = APIRouter(
    prefix='/address',
    tags=['address'],
    responses={'404': {'description': 'Not found'}}
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


class Address(BaseModel):
    address1: str
    address2: Optional[str]
    city: str
    state: str
    country: str
    postalcode: str


@router.post("/")
async def create_address(address: Address,
                         user: dict = Depends(get_current_user),
                         db: Session = Depends(get_db)
                        ):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    address_model = models.Address()
    address_model.address1 = address.address1
    address_model.address2 = address.address2
    address_model.city = address.city
    address_model.state = address.state
    address_model.country = address.country
    address_model.postalcode = address.postalcode

    db.add(address_model)
    db.flush()

    user_model = db.query(models.Users).filter(models.Users.id == user.get('id')).first()
    user_model.address_id = address_model.id
    db.add(user_model)

    db.commit()
