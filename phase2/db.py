import csv
import json
from datetime import datetime

import pandas as pd
from sqlalchemy import (URL, VARCHAR, BigInteger, Date, Float, ForeignKey,
                        Integer, create_engine, select, text)
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
    name: Mapped[str] = mapped_column(VARCHAR(30))


class Team(Base):
    __tablename__ = "team"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(30))


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
    market_value: Mapped[int] = mapped_column(BigInteger(), nullable=True)
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
    # home_team: Mapped[int] = mapped_column(Integer())
    # away_team: Mapped[int] = mapped_column(Integer())
    playing_position_id: Mapped[int] = mapped_column(
        ForeignKey("playing_position.id"), nullable=True
    )


class Goal(Base):
    __tablename__ = "goal"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    match_id: Mapped[int] = mapped_column(ForeignKey("match.id"))
    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    # home_team: Mapped[int] = mapped_column(Integer())
    # away_team: Mapped[int] = mapped_column(Integer())
    number_of_goals: Mapped[int] = mapped_column(Integer())
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
# INSERT TEAMS
###########################################
with open("./teams_initial_data.csv", "r") as file:
    file_contents = csv.DictReader(file)
    for team in file_contents:
        team_record = session.get(Team, team["club_id"])
        if not team_record:
            new_data = Team(
                id=team["club_id"],
                name=team["club_name"],
            )
            session.add(new_data)


###########################################
# INSERT TEAM DETAILS
###########################################
initial_team_data = pd.read_csv("./teams_initial_data.csv")
more_team_data = pd.read_csv("./team_details.csv")
team_details_data = pd.merge(
    initial_team_data,
    more_team_data,
    left_on=["club_formatted_name", "season"],
    right_on=["team_name", "year"],
)
for _, row in team_details_data.iterrows():
    team_league = (
        session.scalars(select(League).where(League.name == row["league"])).one().id
    )
    new_data = TeamDetail(
        team_id=row["club_id"],
        year=row["season"],
        league_id=team_league,
        average_age=row["club_age"],
        match_played=row["num_match"],
        won=row["num_win"],
        draw=row["num_draw"],
        lost=row["num_lose"],
        goal_for=row["goal_zade"],
        goal_against=row["goal_khorde"],
        goal_diff=row["goal_difference"],
        points=row["points"],
        group_position=row["rank"],
        total_market_value=row["club_tmv"],
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
# INSERT AGENTS
###########################################
with open("./agents.csv", "r") as file:
    file_contents = csv.DictReader(file)
    for agent in file_contents:
        agent_record = session.get(Agent, agent["agent_id"])
        if not agent_record:
            new_data = Agent(
                id=agent["agent_id"],
                name=agent["agent_name"],
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


###########################################
# INSERT PLAYER DETAIL DATA
###########################################
agents_data = pd.read_csv("agents.csv")
with open("player_details.json") as file:
    file_contents = file.read()
    parsed_json = json.loads(file_contents)
    for player_detail in parsed_json:
        player_record = session.get(Player, player_detail["player_id"])
        if player_record:
            agent_record = agents_data.query(
                f'player_id == {player_detail["player_id"]} and season == {player_detail["season"]}'
            )
            agent = (
                None if agent_record.empty else int(agent_record["agent_id"].values[0])
            )
            new_data = PlayerDetail(
                player_id=player_detail["player_id"],
                season=player_detail["season"],
                team_id=player_detail["team_id"],
                market_value=player_detail["market_value"],
                agent_id=agent,
            )
            session.add(new_data)


###########################################
# INSERT MATCHES
###########################################
with open("./games.csv", "r") as file:
    file_contents = csv.DictReader(file)
    for game in file_contents:
        home_team = session.scalars(
            select(Team).where(Team.name == game["home_team"])
        ).first()
        away_team = session.scalars(
            select(Team).where(Team.name == game["away_team"])
        ).first()
        league = session.scalars(
            select(League).where(League.name == game["league_name"])
        ).first()
        if home_team and away_team and league:
            home_team_goals = (
                game["result"]
                .strip()
                .replace("'", "")
                .replace("[", "")
                .replace("]", "")
                .split(",")[0]
            )
            away_team_goals = (
                game["result"]
                .strip()
                .replace("'", "")
                .replace("[", "")
                .replace("]", "")
                .split(",")[1]
            )
            if int(home_team_goals) == int(away_team_goals):
                game_result = "draw"
            elif int(home_team_goals) > int(away_team_goals):
                game_result = "home team win"
            else:
                game_result = "away team win"
            new_data = Match(
                id=game["game_id"],
                season=datetime.strptime(game["date"], "%d-%b-%y").strftime("%Y"),
                date=datetime.strptime(game["date"], "%d-%b-%y").strftime("%Y-%m-%d"),
                league_id=league.id,
                home_team_id=home_team.id,
                away_team_id=away_team.id,
                result=game_result,
                home_team_goals=home_team_goals,
                away_team_goals=away_team_goals,
            )
            session.add(new_data)


###########################################
# INSERT PLAYER APPEARANCE
###########################################
with open("./player_games.csv", "r") as file:
    file_contents = csv.DictReader(file)
    for player_game in file_contents:
        player_record = session.get(Player, player_game["player_id"])
        match_record = session.get(Match, player_game["game_id"])
        team_record = session.get(Team, player_game["team_id"])
        if (
            player_record
            and match_record
            and team_record
            and player_game["played_minutes"]
        ):
            playing_position_name = (
                player_game["player_position"]
                .replace("midfield", "Central Midfield")
                .replace("Defender", "Defensive Midfield")
                .replace("Attack", "Attacking Midfield")
                if player_game["player_position"] in ["midfield", "Defender", "Attack"]
                else player_game["player_position"]
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
            new_data = PlayerAppearance(
                player_id=player_game["player_id"],
                match_id=player_game["game_id"],
                team_id=player_game["team_id"],
                playing_position_id=playing_position,
            )
            session.add(new_data)


###########################################
# INSERT PLAYER GOALS
###########################################
with open("./player_goals.csv", "r") as file:
    file_contents = csv.DictReader(file)
    for goal in file_contents:
        player_record = session.get(Player, goal["player_id"])
        match_record = session.get(Match, goal["game_id"])
        team_record = session.get(Team, goal["team_id"])
        if player_record and match_record and team_record:
            new_data = Goal(
                match_id=goal["game_id"],
                player_id=goal["player_id"],
                team_id=goal["team_id"],
                number_of_goals=goal["goals"],
                own_goal=0,
                penalty=0,
            )
            session.add(new_data)

with open("./player_own_goals.csv", "r") as file:
    file_contents = csv.DictReader(file)
    for own_goal in file_contents:
        player_record = session.get(Player, own_goal["player_id"])
        match_record = session.get(Match, own_goal["game_id"])
        team_record = session.get(Team, own_goal["team_id"])
        if player_record and match_record and team_record:
            new_data = Goal(
                match_id=own_goal["game_id"],
                player_id=own_goal["player_id"],
                team_id=own_goal["team_id"],
                number_of_goals=own_goal["own_goals"],
                own_goal=1,
                penalty=0,
            )
            session.add(new_data)

session.commit()
