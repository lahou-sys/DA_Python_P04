class Round:
    """
    A class to represent the model of a round.
    In charge of the underlying logical structure of round.

    """
    def __init__(
        self, name: str, created_at: str, finished_at: str = None, start: bool = True
    ):
        self.matchs = []
        self.name = name
        self.created_at = created_at
        self.finished_at = finished_at
        self.start = start

    @property
    def serialize_round(self):
        '''Returns the dictionary of class attributes.

        '''
        return {
            "name": self.name,
            "created_at": self.created_at,
            "finished_at": self.finished_at,
            "round_in_progress": self.start,
            "matchs": self.serialize_match,
        }

    @property
    def serialize_match(self):
        '''Returns the list of match for a round.

        '''
        return [match.serialize_match for match in self.matchs]
