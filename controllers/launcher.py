import sys

from controllers.players import PlayersController
from controllers.tournaments import TournamentsController
from models.tournament import Tournament


class LauncherController:
    """
    Class which has an orchestrator role for the launch of the program.
    Entry point for the main menu.

    """
    def __init__(self):
        self.player_controller = PlayersController()
        self.tournament_controller = TournamentsController()

    def banner(self):
        '''Contrôle l'affichage de la bannière avec le logo du club.

        '''
        self.tournament_controller.tournament_view.display_logo_ascii_art("logo/ascii-art.txt")

    def perform(self):
        '''Controle l'affichage du menu principal.

        '''
        user_choice = ""
        while user_choice != 0:
            self.tournament_controller.tournament_view.main_menu_who_display_possible_choice_to_user()
            user_choice = self.tournament_controller.tournament_view.get_user_choice(6)
            self.execute_user_choice(user_choice)

    def create_new_player(self):
        '''Controls the launch of a new player creation.

        '''
        self.player_controller.create()
        self.perform()

    def create_new_tournament(self):
        '''Controls the launch of a creation of a new tournament.

        '''
        tournament = self.tournament_controller.create()
        if tournament:
            self.get_tournament_user_choice(tournament)
        self.perform()

    def exit_program(self):
        '''Controls the launch of the program shutdown.

        '''
        self.tournament_controller.tournament_view.exit_program()
        sys.exit()

    def execute_user_choice(self, user_choice: int):
        '''Controls the launch of the command according to the user's choice.

        '''
        commands = {
            1: self.create_new_player,
            2: self.create_new_tournament,
            3: self.use_existing_tournament,
            4: self.display_players,
            5: self.display_tournaments,
            0: self.exit_program,
        }
        getattr(commands[user_choice]())

    def display_players(self):
        '''Controls the launch of the players display.

        '''
        players = self.player_controller.index()
        if players:
            user_choice = self.player_controller.player_view.get_user_choice(5)
            self.execute_user_choice_about_players(user_choice)
        self.perform()

    def display_tournaments(self):
        '''Controls the launch of the tournaments display.

        '''
        tournaments = self.tournament_controller.index()
        if tournaments:
            self.tournament_controller.tournament_view.display_menu_tournament()
            user_choice = self.tournament_controller.tournament_view.get_user_choice(2)
            self.execute_user_choice_about_tournaments(user_choice)
        self.perform()

    def execute_user_choice_about_tournaments(self, user_choice: int):
        '''Controls the execution of the user's choice regarding tournaments.

        '''
        if user_choice == 1:
            self.use_existing_tournament()
        elif user_choice == 2:
            self.perform()

    def execute_user_choice_about_players(self, user_choice: int):
        '''Controls the execution of the user's choice regarding players.

        '''
        if user_choice == 1:
            self.player_controller.create()
            self.display_players()
        elif user_choice == 2:
            self.player_controller.update_players_ranking()
            self.display_players()
        elif user_choice == 3:
            self.player_controller.display_players_by_ranking()
            self.display_players()
        elif user_choice == 4:
            self.player_controller.display_players_by_alphabetical_order()
            self.display_players()
        elif user_choice == 0:
            self.perform()

    def use_existing_tournament(self):
        '''Controls the user's choice of choosing an existing tournament.

        '''
        if not self.tournament_controller.index() is None:
            self.tournament_controller.tournament_view.display_message_to_user(
                "Utiliser un tournoi déjà existant")
            tournament = self.tournament_controller.select_tournament()
            if tournament:
                self.get_tournament_user_choice(tournament)
        self.perform()

    def get_tournament_user_choice(self, tournament: Tournament):
        '''Controls the launch of the display of the tournament submenus.

        '''
        user_choice = ""
        while user_choice != 0:
            self.tournament_controller.tournament_view.tournament_sub_menu(tournament)
            user_choice = self.tournament_controller.tournament_view.get_user_choice(6)
            self.tournament_perform(user_choice, tournament)

    def display_players_list_by_ranking(self, tournament: Tournament, end_of_tournament=False):
        '''Controls the launch of the player display of a tournament by ranking.

        '''
        self.tournament_controller.tournament_view.print_current_tournament(tournament, end_of_tournament)
        self.tournament_controller.tournament_view.display_message_to_user("Liste des participants.")
        self.tournament_controller.print_tournament_players_by_ranking(tournament)

    def display_rounds_list(self, tournament: Tournament, end_of_tournament=False):
        '''Controls the launch of the rounds display of a tournament.

        '''
        self.tournament_controller.tournament_view.print_current_tournament(tournament, end_of_tournament)
        self.tournament_controller.tournament_view.display_message_to_user("Liste des rondes.")
        self.tournament_controller.display_tournament_rounds(tournament)

    def display_matchs_list(self, tournament: Tournament, end_of_tournament=False):
        '''Controls the launch of the match display of a tournament.

        '''
        self.tournament_controller.tournament_view.print_current_tournament(tournament, end_of_tournament)
        self.tournament_controller.tournament_view.display_message_to_user("Liste des matches.")
        self.tournament_controller.display_tournament_matchs(tournament)

    def players_list_by_alphabetical(self, tournament: Tournament, end_of_tournament=False):
        '''Controls the launch of the player display of a tournament by alphabetical.

        '''
        self.tournament_controller.tournament_view.print_current_tournament(tournament, end_of_tournament)
        self.tournament_controller.tournament_view.display_message_to_user("Résultat du tournoi")
        self.tournament_controller.print_tournament_players_by_alphabetical(tournament)

    def display_players_list_by_score(self, tournament: Tournament, end_of_tournament=False):
        '''Controls the launch of the player display of a tournament by score.

        '''
        self.tournament_controller.tournament_view.print_current_tournament(tournament, end_of_tournament)
        self.tournament_controller.tournament_view.display_message_to_user("Liste des participants.")
        self.tournament_controller.print_tournament_players_by_score(tournament)

    def tournament_perform(self, user_choice, tournament: Tournament):
        '''Controls the launch of tournament submenus.

        '''
        if tournament.current_round <= tournament.number_of_turn:
            if (not tournament.players or len(tournament.serialize_tournament_players) < tournament.number_of_player):
                if user_choice == 1:
                    self.tournament_controller.tournament_view.display_message_to_user("\n## Créez les joueurs ##\n")
                    self.player_controller.set_players_list(tournament)
                elif user_choice == 2:
                    self.display_players_list_by_ranking(tournament)
                elif user_choice == 3:
                    self.players_list_by_alphabetical(tournament)
                elif user_choice == 0:
                    self.perform()
            else:
                if user_choice == 1:
                    self.tournament_controller.tournament_view.display_message_to_user("\nTournoi en cours.\n")
                    self.tournament_controller.start_tournament_rounds(tournament)
                elif user_choice == 2:
                    self.display_players_list_by_ranking(tournament)
                elif user_choice == 3:
                    self.players_list_by_alphabetical(tournament)
                elif user_choice == 4:
                    self.display_rounds_list(tournament)
                elif user_choice == 5:
                    self.display_matchs_list(tournament)
                elif user_choice == 0:
                    self.perform()
            user_choice = ""
        else:
            if user_choice == 1:
                self.display_players_list_by_ranking(tournament, True)
            elif user_choice == 2:
                self.players_list_by_alphabetical(tournament, True)
            elif user_choice == 3:
                self.display_players_list_by_score(tournament, True)
            elif user_choice == 4:
                self.display_rounds_list(tournament, True)
            elif user_choice == 5:
                self.display_matchs_list(tournament, True)
            elif user_choice == 0:
                self.perform()
