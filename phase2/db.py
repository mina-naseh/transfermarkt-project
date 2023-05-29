import csv
from datetime import datetime

from sqlalchemy import (
    URL,
    VARCHAR,
    BigInteger,
    Date,
    Float,
    ForeignKey,
    Integer,
    create_engine,
    text,
    select,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from static_data import countries, leagues, playing_positions

MYSQL_DRIVER = "mysql+mysqlconnector"
MYSQL_USERNAME = "root"
MYSQL_PASSWORD = "XXXXXXXXXXX"
MYSQL_HOST_NAME = "localhost"
MYSQL_PORT = 3306
DB_NAME = "transfermarktdb"


url_object = URL.create(
    MYSQL_DRIVER,
    username=MYSQL_USERNAME,
    password=MYSQL_PASSWORD,
    host=MYSQL_HOST_NAME,
    port=MYSQL_PORT,
)
engine = create_engine(url_object)


with engine.connect() as conn:
    conn.execute(text(f"DROP DATABASE IF EXISTS {DB_NAME}"))
    conn.execute(text(f"CREATE DATABASE {DB_NAME}"))

url_object = URL.create(
    MYSQL_DRIVER,
    username=MYSQL_USERNAME,
    password=MYSQL_PASSWORD,
    host=MYSQL_HOST_NAME,
    port=MYSQL_PORT,
    database=DB_NAME,
)

engine = create_engine(url_object)


class Base(DeclarativeBase):
    pass


class Country(Base):
    __tablename__ = "country"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(7))


class League(Base):
    __tablename__ = "league"

    id: Mapped[int] = mapped_column(VARCHAR(3), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(20))
    country_id: Mapped[int] = mapped_column(ForeignKey("country.id"), nullable=True)


class Agent(Base):
    __tablename__ = "agent"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(20))


class Team(Base):
    __tablename__ = "team"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(20))


class TeamDetail(Base):
    __tablename__ = "team_detail"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    year: Mapped[int] = mapped_column(Integer())
    league_id: Mapped[int] = mapped_column(ForeignKey("league.id"))
    average_age: Mapped[float] = mapped_column(Float())
    match_played: Mapped[int] = mapped_column(Integer())
    won: Mapped[int] = mapped_column(Integer())
    draw: Mapped[int] = mapped_column(Integer())
    lost: Mapped[int] = mapped_column(Integer())
    goal_for: Mapped[int] = mapped_column(Integer())
    goal_against: Mapped[int] = mapped_column(Integer())
    goal_diff: Mapped[int] = mapped_column(Integer())
    points: Mapped[int] = mapped_column(Integer())
    group_position: Mapped[int] = mapped_column(Integer())
    total_market_value: Mapped[int] = mapped_column(BigInteger())


class PlayingPosition(Base):
    __tablename__ = "playing_position"

    id: Mapped[int] = mapped_column(VARCHAR(2), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(20))


class Player(Base):
    __tablename__ = "player"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(50))
    birthdate: Mapped[datetime.date] = mapped_column(Date(), nullable=True)
    height: Mapped[int] = mapped_column(Integer(), nullable=True)
    foot: Mapped[str] = mapped_column(VARCHAR(5), nullable=True)
    main_playing_position_id: Mapped[int] = mapped_column(
        ForeignKey("playing_position.id"), nullable=True
    )


class PlayerDetail(Base):
    __tablename__ = "player_detail"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"))
    season: Mapped[int] = mapped_column(Integer())
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    market_value: Mapped[int] = mapped_column(BigInteger())
    agent_id: Mapped[int] = mapped_column(ForeignKey("agent.id"), nullable=True)


class Match(Base):
    __tablename__ = "match"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    season: Mapped[int] = mapped_column(Integer())
    date: Mapped[datetime.date] = mapped_column(Date())
    league_id: Mapped[int] = mapped_column(ForeignKey("league.id"))
    home_team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    away_team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    result: Mapped[str] = mapped_column(VARCHAR(20))
    home_team_goals: Mapped[int] = mapped_column(Integer())
    away_team_goals: Mapped[int] = mapped_column(Integer())


class TeamAppearance(Base):
    __tablename__ = "team_appearance"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    match_id: Mapped[int] = mapped_column(ForeignKey("match.id"))
    hosting: Mapped[str] = mapped_column(VARCHAR(4))


class PlayerAppearance(Base):
    __tablename__ = "player_appearance"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"))
    match_id: Mapped[int] = mapped_column(ForeignKey("match.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    home_team: Mapped[int] = mapped_column(Integer())
    away_team: Mapped[int] = mapped_column(Integer())
    playing_position_id: Mapped[int] = mapped_column(ForeignKey("playing_position.id"))


class Goal(Base):
    __tablename__ = "goal"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    match_id: Mapped[int] = mapped_column(ForeignKey("match.id"))
    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    home_team: Mapped[int] = mapped_column(Integer())
    away_team: Mapped[int] = mapped_column(Integer())
    time_in_minutes: Mapped[int] = mapped_column(Integer())
    own_goal: Mapped[int] = mapped_column(Integer())
    penalty: Mapped[int] = mapped_column(Integer())


class Card(Base):
    __tablename__ = "card"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    match_id: Mapped[int] = mapped_column(ForeignKey("match.id"))
    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    home_team: Mapped[int] = mapped_column(Integer())
    away_team: Mapped[int] = mapped_column(Integer())
    time_in_minutes: Mapped[int] = mapped_column(Integer())
    type: Mapped[str] = mapped_column(VARCHAR(13))


Base.metadata.create_all(bind=engine)

###########################################
# INSERT DATA
###########################################
session = Session(engine)


###########################################
# INSERT COUNTRIES
###########################################
for country in countries:
    new_data = Country(
        id=country["id"],
        name=country["name"],
    )
    session.add(new_data)


###########################################
# INSERT LEAGUES
###########################################
for league in leagues:
    new_data = League(
        id=league["id"],
        name=league["name"],
        country_id=league["country_id"],
    )
    session.add(new_data)


###########################################
# INSERT PLAYING POSITIONS
###########################################
for position in playing_positions:
    new_data = PlayingPosition(
        id=position["id"],
        name=position["name"],
    )
    session.add(new_data)


###########################################
# INSERT PLAYERS
###########################################
with open("./unique_players.csv", "r") as file:
    file_contents = csv.DictReader(file)
    for player in file_contents:
        playing_position_name = (
            player["main_position"]
            .replace("midfield", "Central Midfield")
            .replace("Defender", "Defensive Midfield")
            .replace("Attack", "Attacking Midfield")
            if player["main_position"] in ["midfield", "Defender", "Attack"]
            else player["main_position"]
        )
        if playing_position_name:
            playing_position = (
                session.scalars(
                    select(PlayingPosition).where(
                        PlayingPosition.name == playing_position_name
                    )
                )
                .one()
                .id
            )
        else:
            playing_position = None
        new_data = Player(
            id=player["player_id"],
            name=player["player_name"],
            birthdate=datetime.strptime(player["birthdate"], "%m/%d/%Y").strftime(
                "%Y-%m-%d"
            )
            if player["birthdate"]
            else None,
            height=player["height"] if player["height"] not in ["N/A", ""] else None,
            foot=player["foot"] if player["foot"] not in ["N/A", ""] else None,
            main_playing_position_id=playing_position,
        )
        session.add(new_data)


session.commit()
