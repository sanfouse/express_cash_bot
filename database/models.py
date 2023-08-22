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
    name: str = Column(String())

    media_path: str = Column(String())
    referral_url: str = Column(String())

    description: str = Column(String())

    country: str = Column(ForeignKey('countries.idx'))

    new_client: bool = Column(Boolean(), default=False)
    bad_credit_history: bool = Column(Boolean(), default=False)
    zero_percent: bool = Column(Boolean(), default=False)

    country_emoji = {
        1: 'Россия🇷🇺',
        2: 'Украина🇺🇦',
        3: 'Казахстан🇰🇿'
    }

    def __repr__(self) -> str:
        return f"""
<b>{self.name}</b>

{self.description}

<i>Выгодные условия для новых клиентов:</i> {'✅' if self.new_client else '❌'}
<i>Одобрение с плохой кредитной историей:</i> {'✅' if self.bad_credit_history else '❌'}
<i>Беспроцентный займ</i>: {'✅' if self.zero_percent else '❌'}

<i>Страна: <b>{self.country_emoji[self.country]}</b></i>
"""


class Country(db.Model):
    __tablename__ = "countries"

    idx: int = Column(BigInteger, primary_key=True)
    name: str = Column(String(255), primary_key=True)
