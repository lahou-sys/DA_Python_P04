from models.tournament import Tournament
from views.abstract import AbstractView


class RoundView(AbstractView):
    """
    A class to represent the view of rounds.
    In charge of the user interface for rounds.

    """
    @staticmethod
    def display_round_sub_menu():
        '''Display the sub-menu concerning the rounds
        for the registration of the results.

        '''
        print(f'{"=" * 119}')
        print(f'{"* MENU DES RONDES*"}'.center(119))
        print("1. Inscrire les résultats")
        print("0. Annuler et revenir au menu du tournoi")
        print(f'{"=" * 119}')

    @staticmethod
    def display_players_pair_header():
        '''Displays the players pair table header.

        '''
        print("")
        print(f'{"=" * 119}')
        print(
            f"{'Nom'.center(24)} | "
            f"{'Prénom'.center(24)}"
            f"{''.center(10)}"
            f"{'Nom'.center(24)} | "
            f"{'Prénom'.center(24)}"
            f"\n{'*' * 119}"
        )

    @staticmethod
    def display_players_pair(first_player, second_player):
        '''Displays players pair info in a table.

        '''
        print(
            f"{first_player.first_name.center(24)} | "
            f"{first_player.last_name.center(24)}"
            f"{'VS'.center(10)}"
            f"{second_player.first_name.center(24)} | "
            f"{second_player.last_name.center(24)}"
            f"\n{'-' * 119}"
        )

    def get_player_score(self, question):
        '''Asks the user for the match result to calculate
        the score of the players.

        '''
        validation = ""
        while validation != "Y":
            value = input(f"{question} (Y/N): ").upper()
            while value not in ["Y", "N"]:
                print("Je n'ai pas pu identifier votre réponse, veuillez la saisir à nouveau s'il vous plaît.")
            validation = self.request_confirmation()
            if validation == "Y":
                return value

    @staticmethod
    def display_rounds_header():
        '''Displays the rounds table header.

        '''
        print(f'{"=" * 119}')
        print(
            f"{'Nom'.center(25)} | "
            f"{'Début de ronde'.center(35)} | "
            f"{'Fin de ronde'.center(35)}"
            f"\n{'*' * 119}"
        )

    @staticmethod
    def display_rounds_list(tournament: Tournament):
        '''Displays the rounds info in a table.

        '''
        for game_round in tournament.rounds:
            print(
                f"{game_round.name.center(25)} | "
                f"{game_round.created_at.center(35)} | "
                f"{game_round.finished_at.center(35)}"
                f"\n{'-' * 119}"
            )

    @staticmethod
    def display_matchs_list(tournament: Tournament):
        '''Displays the list of matchs in a table.

        '''
        for game_round in tournament.rounds:
            print(f"\n{'=' * 119}")
            print(f"{'*' * 20}".center(119))
            print(f"{game_round.name.center(119)}")
            print(f"{'*' * 20}".center(119))
            print("")
            print(f"\n{'=' * 119}")
            print(
                f"{'Nom'.center(20)} | "
                f"{'Prénom'.center(20)} | "
                f"{'Score'.center(25)} | "
                f"{'Nom'.center(20)} | "
                f"{'Prénom'.center(20)}"
                f"\n{'*' * 119}"
            )
            for match in game_round.serialize_match:
                print(
                    f"{match['match'][0][0]['last_name'].center(20)} | "
                    f"{match['match'][0][0]['first_name'].center(20)} | "
                    f"{str(match['match'][0][1]).center(11)} | "
                    f"{str(match['match'][1][1]).center(11)} | "
                    f"{match['match'][1][0]['last_name'].center(20)} | "
                    f"{match['match'][1][0]['first_name'].center(20)}"
                    f"\n{'-' * 119}"
                )
