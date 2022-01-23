from tinydb import TinyDB

from models.tournament import Tournament

DATABASE = TinyDB("db/db.json")
TOURNAMENTS = DATABASE.table("TOURNAMENTS")


class TournamentsDatabaseController:
    """
    Class which aims to control the database operations for the tournament table.

    """
    def __init__(self):
        self.tournaments = TOURNAMENTS

    def save_tournament(self, tournament: Tournament):
        '''Controls the insertion of data into the database concerning the tournament.

        '''
        self.tournaments.insert(tournament.serialize_tournament)

    def count_tournament_in_db(self):
        '''Checks the count of tournaments present in the database.

        '''
        return len(self.tournaments)

    def update_tournament(self, tournament: Tournament):
        '''Controls the update of the tournament table.

        '''
        self.tournaments.update(
            tournament.serialize_tournament, doc_ids=[tournament.tournament_id])

    def update_tournament_wiht_id(self, tournament: Tournament, tournament_id: int):
        '''Control the update of the tournament table using the id.

        '''
        self.tournaments.update(
            tournament.serialize_tournament, doc_ids=[int(tournament_id)])

    def search_tournament_by_id(self, tournament_id: int):
        '''Controls the search for an item in the tournament table using the id.

        '''
        tournament = self.tournaments.get(doc_id=int(tournament_id))
        if tournament:
            return tournament
        return None
