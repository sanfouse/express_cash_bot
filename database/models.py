from gino import Gino
from sqlalchemy import BigInteger, Column, String


db = Gino()


class User(db.Model):
    __tablename__ = "users"
    
    idx: int = Column(BigInteger, primary_key=True)
    username: str = Column(String(255), default='noname')


class Offer(db.Model):
    __tablename__ = "offers"

    idx: int = Column(BigInteger, primary_key=True)
    description: str = Column(String())
    media_path: str = Column(String())
    referral_url: str = Column(String())
