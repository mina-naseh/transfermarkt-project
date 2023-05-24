from typing import List

from sqlalchemy import URL, VARCHAR, Integer, create_engine, text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


MYSQL_DRIVER = "mysql+mysqlconnector"
MYSQL_USERNAME = "root"
MYSQL_PASSWORD = "XXXXXXXXXXX"
MYSQL_HOST_NAME = "localhost"
MYSQL_PORT = 3306
DB_NAME = "transfermarktdb"


url_object = URL.create(
    MYSQL_DRIVER ,
    username = MYSQL_USERNAME,
    password = MYSQL_PASSWORD,
    host = MYSQL_HOST_NAME,
    port = MYSQL_PORT
)
engine = create_engine(url_object)


with engine.connect() as conn:
    conn.execute(text(f"DROP DATABASE IF EXISTS {DB_NAME}"))
    conn.execute(text(f"CREATE DATABASE {DB_NAME}"))

url_object = URL.create(
    MYSQL_DRIVER ,
    username = MYSQL_USERNAME,
    password = MYSQL_PASSWORD,
    host = MYSQL_HOST_NAME,
    port = MYSQL_PORT,
    database=DB_NAME,
)

engine = create_engine(url_object)


class Base(DeclarativeBase):
    pass


class Country(Base):
    __tablename__ = "country"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(7))
    leagues: Mapped[List["League"]] = relationship(back_populates="country")


class League(Base):
    __tablename__ = "league"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(20))
    country_id: Mapped[int] = mapped_column(ForeignKey("country.id"))


Base.metadata.create_all(bind=engine)


###########################################
# INSERT DATA
###########################################
