class Match:
    """
    A class to represent the model of a match.
    In charge of the underlying logical structure of match.

    """
    def __init__(
        self, first_player,
        second_player,
        first_player_score,
        second_player_score,
        score_match_lose: int = 0,
        score_match_win: int = 1,
        score_match_equality: int = 0.5
    ):
        self.first_player = first_player
        self.second_player = second_player
        self.first_player_score = first_player_score
        self.second_player_score = second_player_score
        self.matchs = (
            [first_player, first_player_score],
            [second_player, second_player_score],
        )
        self.score_match_lose = score_match_lose
        self.score_match_win = score_match_win
        self.score_match_equality = score_match_equality

    @property
    def serialize_match(self):
        '''Returns a dictionary containing the names
        of the participants of a match.

        '''
        return {"match": self.matchs}
