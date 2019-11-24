import traceback
from typing import Tuple

from sqlalchemy import (
    Column,
    String,
    BigInteger,
    ForeignKey,
    Integer,
    exc,
    sql,
    and_,
)

from .base import Base, Session, engine
from log import get_logger

logger = get_logger('user')


class Diaposon(Base):
    __tablename__ = 'numbers_diaposons'
    start = Column(BigInteger, nullable=False, unique=True, primary_key=True)
    end = Column(BigInteger, nullable=False)
    operator = Column(Integer, ForeignKey('numbers_operators.id'))
    location = Column(Integer, ForeignKey('numbers_locations.id'))

    @staticmethod
    def detect_number(number: int) -> Tuple[str, str]:
        """
        Detect number and return company name and location
        :param number: 10 digits phone number
        :return: (operator, location)
        """
        try:
            session = Session()
            result = session.query(Diaposon)\
                            .filter(and_(Diaposon.start <= number, Diaposon.end >= number))\
                            .first()
            return (result.operator, result.location)
        except Exception:
            return None
        finally:
            session.close()

    @staticmethod
    def truncate() -> None:
        """
        Truncate database
        """
        engine.execute(sql.text("TRUNCATE TABLE numbers_diaposons CASCADE").execution_options(autocommit=True))
        engine.execute(sql.text("TRUNCATE TABLE numbers_operators CASCADE").execution_options(autocommit=True))
        engine.execute(sql.text("TRUNCATE TABLE numbers_locations CASCADE").execution_options(autocommit=True))


class Operator(Base):
    __tablename__ = 'numbers_operators'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, unique=True)


class Location(Base):
    __tablename__ = 'numbers_locations'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False, unique=True)
