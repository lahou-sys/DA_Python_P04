class Tournament:
    """
    A class to represent the model of a tounament.
    In charge of the underlying logical structure of tournaments.

    """
    def __init__(
        self,
        name: str = "",
        location: str = "",
        start_date: str = "",
        end_date: str = "",
        description: str = "",
        time_control: str = "",
        number_of_turn: int = 4,
        tournament_id: int = 0,
        number_of_player: int = 8,
        current_round: int = 1,
    ):
        self.name = name.upper()
        self.location = location.capitalize()
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.time_control = time_control
        self.number_of_turn = number_of_turn
        self.current_round = current_round
        self.tournament_id = tournament_id
        self.number_of_player = number_of_player
        self.players = []
        self.rounds = []

    @property
    def serialize_tournament(self):
        '''Returns the dictionary of class attributes.

        '''
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "time_control": self.time_control,
            "number_of_turn": self.number_of_turn,
            "current_round": self.current_round,
            "tournament_id": self.tournament_id,
            "players": self.serialize_tournament_players,
            "rounds": self.serialize_tournament_rounds,
            "number_of_player": self.number_of_player
        }

    @property
    def serialize_tournament_players(self):
        '''Returns the list of players for a tournament.

        '''
        return [player.serialize_player for player in self.players]

    @property
    def serialize_tournament_rounds(self):
        '''Returns the list of rounds of a tournament.

        '''
        return [round.serialize_round for round in self.rounds]

    def sort_players_by_score(self):
        '''Returns the list of players in a tournament sorted by score
        and by classement.

        '''
        return sorted(
            self.players,
            key=lambda player: (player.score, player.ranking),
            reverse=True
        )

    def sort_players_by_alphabetical(self):
        '''Returns the list of players in a tournament sorted in alphabetical order.

        '''
        return sorted(
            self.players,
            key=lambda player: (player.last_name, player.first_name),
            reverse=False
        )

    def sort_players_by_ranking(self):
        '''Returns the list of players in a tournament sorted by ranking order
        and by name.

        '''
        return sorted(
            self.players,
            key=lambda player: (player.ranking, player.last_name, player.first_name),
            reverse=False
        )

    def sort_players_by_rank(self):
        '''Returns the list of players in a tournament sorted by ranking.

        '''
        return sorted(
            self.players, key=lambda player: player.ranking, reverse=True
        )

    def generate_first_round_pairs(self):
        '''Returns the list of players in a paired tournament for the first round.

        '''
        players = self.sort_players_by_rank()
        tournament_number_of_players = self.number_of_player
        first_players_part = players[0: int(tournament_number_of_players / 2)]
        second_players_part = players[int(tournament_number_of_players / 2):]
        players_pairs = []
        for index in range(int(tournament_number_of_players / 2)):
            players_pair = [first_players_part[index], second_players_part[index]]
            players_pairs.append(players_pair)
            first_players_part[index].opponents.append(
                second_players_part[index].player_id)
            second_players_part[index].opponents.append(
                first_players_part[index].player_id)
        return players_pairs

    def generate_pairs(self):
        '''Returns the list of players in a paired tournament for subsequent rounds.

        '''
        players = self.sort_players_by_score()
        players_pairs = []
        while players:
            index = 1
            while (
                    index <= len(players)
                    and len(players) > 2
                    and players[index].player_id in players[0].opponents):
                index += 1
            players_pair = [players[0], players[index]]
            players[0].opponents.append(players[index].player_id)
            players[index].opponents.append(players[0].player_id)
            del players[index]
            del players[0]
            players_pairs.append(players_pair)
        return players_pairs
