class Player:
    """
    A class to represent the model of a player.
    In charge of the underlying logical structure of player.

    """
    def __init__(
        self, first_name: str, last_name: str, date_of_birth: str, sex: str, ranking
    ):
        self.first_name = first_name.capitalize()
        self.last_name = last_name.upper()
        self.date_of_birth = date_of_birth
        self.sex = sex
        self.ranking = ranking

    @property
    def serialize_player(self):
        '''Returns the dictionary of class attributes.

        '''
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "sex": self.sex,
            "ranking": self.ranking,
        }

    @property
    def serialize_match_player(self):
        '''Returns a dictionary with the following info:
        last name, first name and player ID for a match.

        '''
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "id": self.player_id,
        }
