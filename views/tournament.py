from models.tournament import Tournament
from utils.utils import date_now
from views.abstract import AbstractView


class TournamentView(AbstractView):
    """
    A class to represent the view of a tounament.
    In charge of the user interface for tournaments.

    """
    @staticmethod
    def display_logo_ascii_art(logo_file):
        '''Displays the club's logo as a banner
        when the program is launched.

        '''
        with open(logo_file, 'r') as f:
            for line in f:
                print((line.center(119)).rstrip())
        print("")
        print("**".center(119))
        print("")
        print(" ** CLUB D'ECHECS ** ".center(119))
        print("")
        print(" ** GESTION DE TOURNOIS ** ".center(119))
        print("")
        print("**".center(119))
        print(f"Date: {date_now()}")
        print("")

    def display_time_control_possibilities(self):
        '''Shows the user the choice between
        the different time controls.

        '''
        print("Voici les différents choix possibles : ")
        print("1. Bullet")
        print("2. Blitz")
        print("3. Coup rapide")
        user_choice = 0
        while user_choice not in range(1, 4):
            try:
                user_choice = int(input("Quel time control souhaitez vous choisir ? :"))
                if user_choice not in range(1, 4):
                    print(
                        "Désolé mais votre choix ne correspond pas au possibilitées offertes"
                    )
                else:
                    user_confirmation = self.request_confirmation()
                    if user_confirmation == "Y":
                        return self.perform_user_time_control_choice(user_choice)
            except (ValueError, TypeError):
                print("Désolé mais je n'ai pas compris votre choix, veuillez réessayer")

    @staticmethod
    def perform_user_time_control_choice(user_choice: int):
        '''Returns the choice between the different time controls.

        '''
        switcher = {1: "Bullet", 2: "Blitz", 3: "Coup rapide"}
        return switcher.get(user_choice)

    def tournament_sub_menu(self, tournament: Tournament):
        '''Displays the tournament submenus.

        '''
        print("Quelle action souhaitez vous effectuer ?")
        if tournament.current_round < (tournament.number_of_turn + 1):
            if (
                not tournament.players
                or len(tournament.serialize_tournament_players) < tournament.number_of_player
            ):
                print("1. Ajouter des joueurs.")
                print("2. Afficher la liste des participants par classement.")
                print("3. Afficher la liste des participants par ordre alphabétique.")
                print("0. Quitter le tournoi.")
            else:
                print(f"1. Démarrer le tour : {tournament.current_round}.")
                print("2. Afficher la liste des participants par classement.")
                print("3. Afficher la liste des participants par ordre alphabétique.")
                print("4. Afficher la liste des rondes.")
                print("5. Afficher la liste des matches.")
                print("0. Quitter le tournoi.")
        else:
            print("1. Afficher la liste des participants par classement.")
            print("2. Afficher la liste des participants par ordre alphabétique.")
            print("3. Afficher la liste des participants par score.")
            print("4. Afficher la liste des rondes.")
            print("5. Afficher la liste des matches.")
            print("0. Quitter le tournoi.")

    @staticmethod
    def display_tournament_header():
        '''Displays the tournaments table header.

        '''
        print("")
        print(f'{"=" * 140}')
        print(
            f"{'Id'.center(4)} | "
            f"{'Nom'.center(15)} | "
            f"{'Lieu'.center(12)} | "
            f"{'Date de début'.center(13)} | "
            f"{'Date de fin'.center(13)} | "
            f"{'Time control'.center(13)} | "
            f"{'Nbre de tours'.center(10)} | "
            f"{'Nbre joueur max'.center(10)} | "
            f"{'Description'.center(20)}"
            f"\n{'*' * 140}")

    @staticmethod
    def display_tournament(
        tournament_id: int,
        name: str,
        location: str,
        start_date: str,
        end_date: str,
        time_control: str,
        number_of_turn: int,
        number_of_player: int,
        description: str
    ):
        '''Displays tournament info in a table.

        '''
        print(
            f"{str(tournament_id).center(4)} | "
            f"{name.center(15)} | "
            f"{location.center(12)} | "
            f"{start_date.center(13)} | "
            f"{end_date.center(13)} | "
            f"{time_control.center(13)} | "
            f"{str(number_of_turn).center(13)} | "
            f"{str(number_of_player).center(15)} | "
            f"{description.center(20)}"
            f"\n{'-' * 140}"
            f"\n{''}")

    @staticmethod
    def print_header_tournament_no_finished():
        '''Display the header of the table concerning
        an unfinished tournament in a table.

        '''
        print(
            f"{'Ronde en cours'.center(13)} | "
            f"{'Nom'.center(18)} | "
            f"{'Lieu'.center(15)} | "
            f"{'Date de début'.center(12)} | "
            f"{'Date de fin'.center(12)} | "
            f"{'Time control'.center(12)} | "
            f"{'Nombre de tours'.center(12)} | "
            f"{'Description'.center(20)}"
            f"\n{'*' * 140}")

    @staticmethod
    def print_header_tournament_finished():
        '''Display the table header for a completed
        tournament in a table.

        '''
        print(
            f"{'Nom'.center(18)} | "
            f"{'Lieu'.center(15)} | "
            f"{'Date de début'.center(12)} | "
            f"{'Date de fin'.center(12)} | "
            f"{'Time control'.center(12)} | "
            f"{'Nombre de tours'.center(12)} | "
            f"{'Description'.center(20)}"
            f"\n{'*' * 140}")

    def print_current_tournament(self, tournament: Tournament, end_of_tournament=False):
        '''Display information about a tournament in a table.

        '''
        print("")
        print(f'{"=" * 140}')
        if not end_of_tournament:
            self.print_header_tournament_no_finished()
            print(
                f"{(str(tournament.current_round)).center(14)} | "
                f"{tournament.name.center(18)} | "
                f"{tournament.location.center(15)} | "
                f"{tournament.start_date.center(12)} | "
                f"{tournament.end_date.center(12)} | "
                f"{tournament.time_control.center(12)} | "
                f"{(str(tournament.number_of_turn)).center(15)} | "
                f"{tournament.description.center(20)}"
                f"\n{'-' * 140}"
                f"\n{''}")
        else:
            self.print_header_tournament_finished()
            print(
                f"{tournament.name.center(18)} | "
                f"{tournament.location.center(15)} | "
                f"{tournament.start_date.center(12)} | "
                f"{tournament.end_date.center(12)} | "
                f"{tournament.time_control.center(12)} | "
                f"{(str(tournament.number_of_turn)).center(15)} | "
                f"{tournament.description.center(20)}"
                f"\n{'-' * 140}"
                f"\n{''}")
            print("Tournois terminé !\n")

    @staticmethod
    def display_menu_tournament():
        '''Display the menu to import a tournament.

        '''
        print(f'{"=" * 140}')
        print(f'{"* MENU TOURNAMENTS*"}'.center(119))
        print("1. Importez un tournoi.")
        print("0. Retour au menu principal.\n")
        print(f'{"=" * 140}')
