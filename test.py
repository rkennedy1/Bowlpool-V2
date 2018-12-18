import json
import argparse
import logging
import requests
from flask import Flask, escape, Markup, render_template
from flask_table import Table, Col
import openpyxl
from flask import Flask
app = Flask(__name__)

gamesList = []

@app.route('/')
def hello_world():
    bowlList = load_games_for_day('401035253')
    bowlListHTML = Markup(bowlList.__html__())
    return render_template('layout.html', bowlListHTML=bowlListHTML)

class GameTable(Table):

    teams = Col('teams')
    conference = Col('conference')
    homeAway = Col('homeAway')
    points = Col('points')
    school = Col('school')



def load_games_for_day(gameID):
    # Execute the espn api to get all the games for a day and load them into the
    # internal game object that in turn is stored in the games dictionary
    r = requests.get('https://api.collegefootballdata.com/games/teams?year=2018&seasonType=regular&gameId=' + gameID)
    logging.info('Teams loaded for game ID: ' + gameID)
    gamesjson = json.loads(r.text)
    for gamejson in gamesjson[0]["teams"]:
        tempConference = gamejson["conference"]
        tempHomeAway = gamejson["homeAway"]
        tempPoints = int(gamejson["points"])
        tempSchool = gamejson["school"]
        print(tempSchool)

        if (tempHomeAway == 'away'):
            awayTeam = dict(conference = tempConference,
                        homeAway = tempHomeAway,
                        points = tempPoints,
                        school = tempSchool)
        else:
            homeTeam = dict(conference = tempConference,
                        homeAway = tempHomeAway,
                        points = tempPoints,
                        school = tempSchool)

    #gamesjson = bowlpool_from_dict(json.loads(r.text))
    gamesList.append(homeTeam)
    gamesList.append(awayTeam)

    gameTable = GameTable(gamesList)

    return gamesList

    if __name__ == '__main__':
        logging.basicConfig(level=logging.INFO)

        # Only accepts on parm that contains the location of the configuration file
        # If none it provided a default is used.
        parser = argparse.ArgumentParser(description='Bowl Pool')
        parser.add_argument(
            '-playerfile',
            nargs='?',
            default='data/players.json',
            metavar='PLAYERFILE',
            help='Name of the player file (Default: data/players.json)'
        )

        args = parser.parse_args()
        logging.info('Player File - {0}'.format(args.playerfile))

        # Load the configuraiton based on the configuration file
        playerfilename = args.playerfile
        #load_players()
        hello_world()
        #print_team_ids()
        #load_games_for_day("20171216")

        startTime = datetime.datetime.now()

        endTime = datetime.datetime.now()

        delta = endTime - startTime
        logging.info('Start Time: {0}'.format(startTime))
        logging.info('End Time: {0}'.format(endTime))
        logging.info('Total time elapsed (seconds): {0}'.format(delta.total_seconds()) )


# # To use this code, make sure you
# #
# #     import json
# #
# # and then, to convert JSON from a string, do
# #
# #     result = bowlpool_from_dict(json.loads(json_string))
#
# from typing import Any, List, TypeVar, Callable, Type, cast
#
#
# T = TypeVar("T")
#
#
# def from_str(x: Any) -> str:
#     assert isinstance(x, str)
#     return x
#
#
# def from_int(x: Any) -> int:
#     assert isinstance(x, int) and not isinstance(x, bool)
#     return x
#
#
# def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
#     assert isinstance(x, list)
#     return [f(y) for y in x]
#
#
# def to_class(c: Type[T], x: Any) -> dict:
#     assert isinstance(x, c)
#     return cast(Any, x).to_dict()
#
#
# class Stat:
#     category: str
#     stat: str
#
#     def __init__(self, category: str, stat: str) -> None:
#         self.category = category
#         self.stat = stat
#
#     @staticmethod
#     def from_dict(obj: Any) -> 'Stat':
#         assert isinstance(obj, dict)
#         category = from_str(obj.get("category"))
#         stat = from_str(obj.get("stat"))
#         return Stat(category, stat)
#
#     def to_dict(self) -> dict:
#         result: dict = {}
#         result["category"] = from_str(self.category)
#         result["stat"] = from_str(self.stat)
#         return result
#
#
# class Team:
#     school: str
#     conference: str
#     home_away: str
#     points: int
#     stats: List[Stat]
#
#     def __init__(self, school: str, conference: str, home_away: str, points: int, stats: List[Stat]) -> None:
#         self.school = school
#         self.conference = conference
#         self.home_away = home_away
#         self.points = points
#         self.stats = stats
#
#     @staticmethod
#     def from_dict(obj: Any) -> 'Team':
#         assert isinstance(obj, dict)
#         school = from_str(obj.get("school"))
#         conference = from_str(obj.get("conference"))
#         home_away = from_str(obj.get("homeAway"))
#         points = from_int(obj.get("points"))
#         stats = from_list(Stat.from_dict, obj.get("stats"))
#         return Team(school, conference, home_away, points, stats)
#
#     def to_dict(self) -> dict:
#         result: dict = {}
#         result["school"] = from_str(self.school)
#         result["conference"] = from_str(self.conference)
#         result["homeAway"] = from_str(self.home_away)
#         result["points"] = from_int(self.points)
#         result["stats"] = from_list(lambda x: to_class(Stat, x), self.stats)
#         return result
#
#
# class BowlpoolElement:
#     id: int
#     teams: List[Team]
#
#     def __init__(self, id: int, teams: List[Team]) -> None:
#         self.id = id
#         self.teams = teams
#
#     @staticmethod
#     def from_dict(obj: Any) -> 'BowlpoolElement':
#         assert isinstance(obj, dict)
#         id = from_int(obj.get("id"))
#         teams = from_list(Team.from_dict, obj.get("teams"))
#         return BowlpoolElement(id, teams)
#
#     def to_dict(self) -> dict:
#         result: dict = {}
#         result["id"] = from_int(self.id)
#         result["teams"] = from_list(lambda x: to_class(Team, x), self.teams)
#         return result
#
#
# def bowlpool_from_dict(s: Any) -> List[BowlpoolElement]:
#     return from_list(BowlpoolElement.from_dict, s)
#
#
# def bowlpool_to_dict(x: List[BowlpoolElement]) -> Any:
#     return from_list(lambda x: to_class(BowlpoolElement, x), x)
