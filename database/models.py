from gino import Gino
from sqlalchemy import BigInteger, Column, String, Boolean


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

    location: str = Column(String())
    terms: str = Column(String())
    requirements: str = Column(String())

    new_client: bool = Column(Boolean(), default=False)
    bad_credit_history: bool = Column(Boolean(), default=False)
    zero_percent: bool = Column(Boolean(), default=False)