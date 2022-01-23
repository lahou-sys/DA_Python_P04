from abc import ABC

from controllers.database.players import PlayersDatabaseController
from controllers.database.tournaments import TournamentsDatabaseController
from views.player import PlayerView
from views.round import RoundView
from views.tournament import TournamentView


class AbstractController(ABC):
    """
    Common class for controller.
    Makes it easier to call other classes.
    Acts as an abstraction layer.

    """
    def __init__(self):
        self.player_view = PlayerView()
        self.tournament_view = TournamentView()
        self.round_view = RoundView()
        self.players_db = PlayersDatabaseController()
        self.tournaments_db = TournamentsDatabaseController()
