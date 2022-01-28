from controllers.abstract import AbstractController
from models.participant import Participant
from models.player import Player
from models.tournament import Tournament


class PlayersController(AbstractController):
    """
    A class to represent the controller of the players.
    In charge of communication between view class and model class for players.

    """
    def display_player(self, player):
        '''Controls the display of player information.

        '''
        self.player_view.display_player(
            player.doc_id,
            player["first_name"],
            player["last_name"],
            player["date_of_birth"],
            player["sex"],
            player["ranking"])

    def index(self):
        '''Controls the display the list of players in the database.

        '''
        if self.players_db.players:
            self.player_view.display_players_header()
            for player in self.players_db.players:
                self.display_player(player)
            self.player_view.display_players_sub_menu()
            return self.players_db.players
        self.player_view.display_message_to_user(
            "\n"
            "Aucun joueur n'a pu être trouvé dans la base de données !"
            "\n")
        return None

    def create(self, first_name=None, last_name=None):
        '''Controls the creation of a new player.

        '''
        if (first_name and last_name) is None:
            first_name = self.player_view.get_valide_name("le prénom", "joueur")
            last_name = self.player_view.get_valide_name("le nom", "joueur")
        if not self.players_db.search_in_players_table(first_name, last_name):
            self.create_if_player_does_not_exist(first_name, last_name)
        else:
            self.player_view.display_message_to_user(
                "\n** ATTENTION ! **\n"
                f"\nLe joueur {first_name} {last_name} existe déjà !")

    def create_if_player_does_not_exist(self, first_name, last_name):
        '''Controls the creation of a new player if it does not exist in the database.

        '''
        date_of_birth = self.player_view.get_date_format(
            "la date de naissance", "joueur", "birthday")
        sex = self.player_view.get_player_sex()
        ranking = self.player_view.get_integer_value("le rang", "joueur")
        player = Player(first_name, last_name, date_of_birth, sex, ranking)
        self.players_db.save_player(player)
        self.player_view.display_message_to_user(
            f"{first_name} {last_name} a bien été ajouté à la base de données")

    def prepare_add_player_to_tournament(self, player_to_add):
        '''Controls the preparation of a player's info to add him to a tournament.

        '''
        player = Participant(
            player_to_add["first_name"],
            player_to_add["last_name"],
            player_to_add["date_of_birth"],
            player_to_add["sex"],
            player_to_add["ranking"])
        return player

    def ask_to_contnue(self):
        '''Controls asking the user if they want to continue.

        '''
        reponse = self.player_view.request_user_validation_to_continue()
        if reponse != "Y":
            return False
        else:
            return True

    def check_number_player_is_ok(self, nbr_of_player_expected, nbr_of_player_in_base):
        '''Check if the expected number of players is reached.

        '''
        if nbr_of_player_expected == nbr_of_player_in_base:
            self.player_view.display_message_to_user(
                "Tous les joueurs nécessaires ont été créés, le tournoi peut commencer")

    def set_players_list(self, tournament: Tournament):
        '''Controls adding players to an existing tournament.

        '''
        actual_players_number_for_tournament = len(tournament.serialize_tournament_players)
        while actual_players_number_for_tournament < tournament.number_of_player:
            if actual_players_number_for_tournament == 0:
                self.player_view.display_message_to_user("Creez le 1er joueur")
            else:
                self.player_view.display_message_to_user(
                    f"Creez le {actual_players_number_for_tournament + 1} joueur")
            first_name = self.player_view.get_valide_name("le prénom", "joueur")
            last_name = self.player_view.get_valide_name("le nom", "joueur")
            first_name = first_name.capitalize()
            last_name = last_name.upper()
            if not any(d['first_name'] == first_name and
                       d['last_name'] == last_name for d in tournament.serialize_tournament_players):
                existing_player = self.players_db.search_in_players_table(first_name, last_name)
                if not existing_player:
                    self.create(first_name, last_name)
                    just_add_player = self.players_db.search_in_players_table(first_name, last_name)
                    player = self.prepare_add_player_to_tournament(just_add_player)
                    player.player_id = just_add_player.doc_id
                    tournament.players.append(player)
                    self.player_view.display_message_to_user(
                        f"Le joueur {first_name} {last_name} a bien été ajouté au tournoi")
                else:
                    player = self.prepare_add_player_to_tournament(existing_player)
                    player.player_id = existing_player.doc_id
                    tournament.players.append(player)
                    self.player_view.display_message_to_user(
                        f"Le joueur {first_name} {last_name} a bien été ajouté au tournoi")
            else:
                self.player_view.display_message_to_user(
                    f"Le joueur {first_name} {last_name} est déjà présent dans le tournoi")
            self.tournaments_db.update_tournament_wiht_id(tournament, tournament.tournament_id)
            actual_players_number_for_tournament = len(tournament.serialize_tournament_players)
            if not self.ask_to_contnue():
                break
        self.check_number_player_is_ok(tournament.number_of_player, actual_players_number_for_tournament)

    def update_players_ranking(self):
        '''Controls the change of a player's rating manually.

        '''
        self.player_view.display_message_to_user("Modifiez le classement d'un joueur")
        self.player_view.display_players_header()
        for player in self.players_db.players:
            self.display_player(player)
        player_id = self.player_view.get_integer_value("l'id", "joueur")
        player_found = self.players_db.search_player_by_id(player_id)
        if player_found:
            self.update_existing_players_ranking(player_found, player_id)
        else:
            self.player_view.display_message_to_user(
                "Ancun joueur n'a pu être trouvé avec cet id...")

    def update_existing_players_ranking(self, player_found, player_id):
        '''Controls the update of a player's ranking.

        '''
        player = Player(
            player_found["first_name"],
            player_found["last_name"],
            player_found["date_of_birth"],
            player_found["sex"],
            player_found["ranking"])
        self.player_view.display_players_header()
        self.display_player(player_found)
        ranking = self.player_view.get_integer_value("le nouveau classement", "joueur")
        player.ranking = ranking
        self.players_db.update_player(player, player_id)
        self.player_view.display_message_to_user(
            f"Le joueur {player.first_name} {player.last_name} a bien été modifié")

    def display_players_by_ranking(self):
        '''Controls player display by ranking.

        '''
        self.player_view.display_message_to_user("Liste des joueurs triés par classement")
        if self.players_db.players:
            self.player_view.display_players_header()
            for player in self.players_db.sort_players_by_ranking:
                self.display_player(player)
            validation = self.player_view.request_user_validation_for_return()
            if validation == "Y":
                return self.players_db.players
        self.player_view.display_message_to_user(
            "\n"
            "Aucun joueur n'a pu être trouvé dans la base de données !"
            "\n")
        return None

    def display_players_by_alphabetical_order(self):
        '''Controls the display of players in alphabetical order.

        '''
        self.player_view.display_message_to_user(
            "\n"
            "Liste des joueurs triés par ordre alphabétique")
        if self.players_db.players:
            self.player_view.display_players_header()
            for player in self.players_db.sort_players_alphabetically:
                self.display_player(player)
            validation = self.player_view.request_user_validation_for_return()
            if validation == "Y":
                return self.players_db.players
        self.player_view.display_message_to_user(
            "\n"
            "Aucun joueur n'a pu être trouvé dans la base de données !"
            "\n")
        return None
