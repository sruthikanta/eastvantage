from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from uuid import UUID
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
    


class Address(BaseModel):
    address_id : int = Field()
    address : str = Field(min_length=1)
    city : str = Field(min_length=1, max_length=100)
    state : str = Field(min_length=1, max_length=100)
    zipcode : int = Field()
    phone_number : int = Field()
    latitude : float = Field()
    longitude : float = Field()


@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Addresses).all()

  

@app.post("/")
def create_address(address: Address, db: Session = Depends(get_db)):
    address_model = models.Addresses()
    address_model.address = address.address
    address_model.city = address.city
    address_model.state = address.state
    address_model.zipcode = address.zipcode
    address_model.phone_number = address.phone_number
    address_model.latitude = address.latitude
    address_model.longitude = address.longitude

    db.add(address_model)
    db.commit()
    print(f"{address.address} created successfully")
    return address


@app.put("/{address_id}")
def update_address(address_id: int, address: Address, db: Session = Depends(get_db)):
    counter = 0
    ADDRESSES=db.query(models.Addresses).all()

    for x in ADDRESSES:
        counter += 1
        if x.address_id == address_id:
            ADDRESSES[counter - 1] = address
            db.commit()
            print(f"{address} updated for {address_id} successfully")
    raise HTTPException(
        status_code=404,
        detail=f"ID {address_id} : Does not exist"
        )


@app.delete("/{address_id}")
def delete_address(address_id: int, db: Session = Depends(get_db)):
    counter = 0
    ADDRESSES=db.query(models.Addresses).all()
    
    for x in ADDRESSES:
        counter +=1
        if x.address_id == address_id:
            del ADDRESSES[counter - 1]
            db.commit()
            return f"ID: {address_id} deleted "
        raise HTTPException(
            status_code=404,
            detail=f"ID {address_id} : Does not exist"
            )
