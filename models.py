from sqlalchemy import Column, Integer, String, Float
from database import Base


class Addresses(Base):
    __tablename__ = "addresses"

    address_id = Column(Integer, primary_key=True)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zipcode = Column(Integer)
    phone_number = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)