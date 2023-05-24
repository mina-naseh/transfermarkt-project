from sqlalchemy import URL, VARCHAR, Integer, create_engine, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

DB_NAME = "transfermarktdb"


url_object = URL.create(
    "mysql+mysqlconnector",
    username="root",
    password="XXXXXXXXXXX",
    host="localhost",
)
engine = create_engine(url_object)


with engine.connect() as conn:
    conn.execute(text(f"DROP DATABASE IF EXISTS {DB_NAME}"))
    conn.execute(text(f"CREATE DATABASE {DB_NAME}"))

url_object = URL.create(
    "mysql+mysqlconnector",
    username="root",
    password="XXXXXXXXXXX",
    host="localhost",
    database=DB_NAME,
)

engine = create_engine(url_object)


class Base(DeclarativeBase):
    pass


class Country(Base):
    __tablename__ = "country"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(7))


Base.metadata.create_all(bind=engine)


###########################################
# INSERT DATA
###########################################
