from gino import Gino
from sqlalchemy import BigInteger, Column, String, Boolean, ForeignKey


db = Gino()


class User(db.Model):
    __tablename__ = "users"
    
    idx: int = Column(BigInteger, primary_key=True)
    username: str = Column(String(255), default='noname')


class Offer(db.Model):
    __tablename__ = "offers"

    idx: int = Column(BigInteger, primary_key=True)
    media_path: str = Column(String())
    referral_url: str = Column(String())

    description: str = Column(String())

    country: str = Column(ForeignKey('countries.idx'))

    new_client: bool = Column(Boolean(), default=False)
    bad_credit_history: bool = Column(Boolean(), default=False)
    zero_percent: bool = Column(Boolean(), default=False)


class Country(db.Model):
    __tablename__ = "countries"

    idx: int = Column(BigInteger, primary_key=True)
    name: str = Column(String(255))
