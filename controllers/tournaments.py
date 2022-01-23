from datetime import datetime

from controllers.abstract import AbstractController
from models.match import Match
from models.participant import Participant
from models.round import Round
from models.tournament import Tournament


class TournamentsController(AbstractController):
    """
    A class to represent the controller of the tournaments.
    In charge of communication between view class and model class for tournaments.

    """
    def display_tournament(self, tournament):
        '''Controls the display of tournament information.

        '''
        self.tournament_view.display_tournament(
                tournament.doc_id,
                tournament["name"],
                tournament["location"],
                tournament["start_date"],
                tournament["end_date"],
                tournament["time_control"],
                tournament["number_of_turn"],
                tournament["number_of_player"],
                tournament["description"])

    def index(self):
        '''Controls the display the list of tournaments in the database.

        '''
        if self.tournaments_db and len(self.tournaments_db.tournaments) != 0:
            self.tournament_view.display_tournament_header()
            for tournament in self.tournaments_db.tournaments:
                self.display_tournament(tournament)
            return self.tournaments_db.tournaments
        else:
            self.tournament_view.display_message_to_user(
                "\nAucun tournois n'a pu être trouvé dans la base de données !\n")
            return None

    def create(self):
        '''Controls the creation of a new tournament.

        '''
        tournois = Tournament()
        nbr_turn_default = tournois.number_of_turn
        nbr_player_default = tournois.number_of_player
        count = self.tournaments_db.count_tournament_in_db()
        name = self.tournament_view.get_string_value("le nom", "tournoi")
        location = self.tournament_view.get_string_value("la localisation", "tournoi")
        start_date = self.tournament_view.get_date_format(
            "la date du début", "tournoi", "start_tournoi")
        end_date = self.tournament_view.get_date_format("la date de fin", "tournoi", "end_tournoi", start_date)
        description = self.tournament_view.get_string_value("la description", "tournoi")
        time_control = self.tournament_view.display_time_control_possibilities()
        number_of_turn = self.tournament_view.get_number_of_turn(
            "le nombre", f"tours ou laisser vide ({nbr_turn_default} par défaut)", nbr_turn_default)
        number_of_player = self.tournament_view.get_number_of_player(
            "le nombre",
            f"joueur (nombre paire) ou laisser vide ({nbr_player_default} par défaut)", nbr_player_default)
        tournament_id = count + 1
        tournament = Tournament(
            name, location, start_date, end_date, description, time_control, number_of_turn,
            tournament_id, number_of_player)
        self.tournaments_db.save_tournament(tournament)
        self.tournament_view.display_message_to_user(f"Le tournoi {tournament.name} a été crée avec succès")
        return tournament

    def select_tournament(self):
        '''Controls the selection of a tournament if it exists.

        '''
        tournament_id = self.tournament_view.get_integer_value("l'id", "tournoi")
        existing_tournament = self.tournaments_db.search_tournament_by_id(tournament_id)
        if existing_tournament:
            return self.display_tournament_if_it_exists(existing_tournament)
        self.tournament_view.display_message_to_user(
            "\n"
            "Aucun tournoi n'a pu être trouvé !"
            "\n")
        return None

    def get_info_for_player_in_tournament(self, existing_tournament, tournament):
        '''Controls the extraction of information from a player in a tournament.

        '''
        if existing_tournament["players"]:
            for existing_player in existing_tournament["players"]:
                player = Participant(
                    existing_player["first_name"],
                    existing_player["last_name"],
                    existing_player["date_of_birth"],
                    existing_player["sex"],
                    existing_player["ranking"])
                player.player_id = self.players_db.get_player_id(
                    existing_player["first_name"],
                    existing_player["last_name"])
                player.score = existing_player["score"]
                player.ladder = existing_player["ladder"]
                for opponent in existing_player["opponents"]:
                    player.opponents.append(opponent)
                tournament.players.append(player)

    def get_info_for_round_in_tournament(self, existing_tournament, tournament):
        '''Controls the extraction of round information in a tournament.

        '''
        if existing_tournament["rounds"]:
            for existing_round in existing_tournament["rounds"]:
                game_round = Round(existing_round["name"], existing_round["created_at"])
                game_round.start = existing_round["round_in_progress"]
                game_round.finished_at = existing_round["finished_at"]
                tournament.rounds.append(game_round)
                for existing_match in existing_round["matchs"]:
                    match = Match(
                        existing_match["match"][0][0],
                        existing_match["match"][1][0],
                        existing_match["match"][0][1],
                        existing_match["match"][1][1])
                    game_round.matchs.append(match)

    def display_tournament_if_it_exists(self, existing_tournament):
        '''Controls the display of tournament information in the database.

        '''
        self.tournament_view.display_tournament_header()
        self.display_tournament(existing_tournament)
        tournament = Tournament(
            existing_tournament["name"],
            existing_tournament["location"],
            existing_tournament["start_date"],
            existing_tournament["end_date"],
            existing_tournament["description"],
            existing_tournament["time_control"],
            existing_tournament["number_of_turn"],
            existing_tournament["number_of_player"],
            existing_tournament["description"])
        tournament.tournament_id = existing_tournament.doc_id
        self.get_info_for_player_in_tournament(existing_tournament, tournament)
        self.get_info_for_round_in_tournament(existing_tournament, tournament)
        tournament.current_round = existing_tournament["current_round"]
        tournament.number_of_player = existing_tournament["number_of_player"]
        self.tournament_view.display_message_to_user(
            f"Le tournoi {tournament.name} a correctement été trouvé et importé !"
            "\n")
        return tournament

    def print_tournament_players_by_score(self, tournament: Tournament):
        '''Controls the display of tournament players by score.

        '''
        self.player_view.print_players_tournament(tournament.sort_players_by_score())

    def print_tournament_players_by_ranking(self, tournament: Tournament):
        '''Controls the display of tournament players by ranking.

        '''
        self.player_view.print_players_tournament(tournament.sort_players_by_ranking())

    def print_tournament_players_by_alphabetical(self, tournament: Tournament):
        '''Controls the display of tournament players by alphabetical order.

        '''
        self.player_view.print_players_tournament(tournament.sort_players_by_alphabetical())

    def launch_rounds_of_tournament(self, game_round, players_pairs, tournament):
        '''Controls the start of a round in a tournament.

        '''
        confirm = ""
        index = 1
        while confirm != "Y":
            self.round_view.display_players_pair_header()
            for first_player, second_player in players_pairs:
                self.round_view.display_players_pair(first_player, second_player)
            self.round_view.display_message_to_user(
                "\n"
                f"{game_round.name} est en cours,Patientez jusqu'à la fin des matchs pour inscrire les scores")
            self.round_view.display_message_to_user(
                "Si vous quittez celle-ci, la ronde sera supprimée\n")
            self.round_view.display_round_sub_menu()
            user_choice = self.round_view.get_user_choice(2)
            if user_choice == 0:
                self.round_view.display_message_to_user(
                    "Si vous quittez maintenant la ronde, celle-ci sera supprimée\n")
                confirm = self.round_view.request_confirmation()
                if confirm == "Y":
                    return
            else:
                self.start_round(game_round, players_pairs, tournament, index)
                return

    def start_tournament_rounds(self, tournament: Tournament):
        '''Control of the management of the rounds in the tournaments.

        '''
        if tournament.current_round <= tournament.number_of_turn:
            name = f"Round {tournament.current_round}"
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            game_round = Round(name, str(created_at))
            if tournament.current_round == 1:
                self.round_view.display_message_to_user("Première ronde")
                players_pairs = tournament.generate_first_round_pairs()
            else:
                self.round_view.display_message_to_user(f"{tournament.current_round}ème round")
                players_pairs = tournament.generate_pairs()
            if players_pairs:
                self.launch_rounds_of_tournament(game_round, players_pairs, tournament)
            else:
                self.round_view.display_message_to_user(
                    "Oups ! Il y a un problème, merci de recommencer !")
                return
        else:
            self.round_view.display_message_to_user("Ce tournoi est maintenant terminée")
            return

    def set_player_score(self, first_player):
        '''Control of players'scores during a match in a round.

        '''
        match = Match(
                "first_player",
                "second_player",
                "first_player_score",
                "second_player_score")
        score_match_lose = match.score_match_lose
        score_match_win = match.score_match_win
        score_match_equality = match.score_match_equality
        first_player_score = second_player_score = 0
        score = []
        match_nul = self.round_view.get_player_score(
            "Est-ce que le match s'est terminé par un match nul ?")
        if match_nul == "Y":
            first_player_score = second_player_score = score_match_equality
        else:
            first_player_if_win = self.round_view.get_player_score(
                f"Est-ce que le joueur {first_player} a gagné le match ?")
            if first_player_if_win == "Y":
                first_player_score = score_match_win
                second_player_score = score_match_lose
            else:
                second_player_score = score_match_win
                first_player_score = score_match_lose
        score = [first_player_score, second_player_score]
        return score

    def start_round(self, game_round, players_pairs, tournament, index):
        '''Control of the progress of the rounds in a tournament.

        '''
        for first_player, second_player in players_pairs:
            self.round_view.display_message_to_user(f"\nLe match {index} commence.")
            self.round_view.display_message_to_user(
                f"\nMatch : {first_player.first_name} {first_player.last_name}"
                "  VS  "
                f"{second_player.first_name} {second_player.last_name}\n")
            first_player_name = f"{first_player.first_name} {first_player.last_name}"
            score = self.set_player_score(first_player_name)
            first_player_score = score[0]
            first_player.score += first_player_score
            second_player_score = score[1]
            second_player.score += second_player_score
            match = Match(
                first_player.serialize_match_player,
                second_player.serialize_match_player,
                first_player_score,
                second_player_score,)
            game_round.matchs.append(match)
            index += 1
        tournament.rounds.append(game_round)
        tournament.current_round += 1
        game_round.finished_at = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        game_round.start = False
        if tournament.current_round == (tournament.number_of_turn + 1):
            for ladder, player in enumerate(tournament.sort_players_by_score(), start=1):
                player.ladder = ladder
            self.round_view.display_message_to_user(
                "Le tournoi est TERMINÉ! Vous pouvez désormais afficher les résultats")
        else:
            self.round_view.display_message_to_user(
                f"Le tour {tournament.current_round - 1} est terminé !")
        self.tournaments_db.update_tournament(tournament)

    def display_tournament_rounds(self, tournament: Tournament):
        '''Controls the display of tournament rounds.

        '''
        self.round_view.display_rounds_header()
        self.round_view.display_rounds_list(tournament)
        validation = self.round_view.request_user_validation_for_return()
        if validation == "Y":
            return

    def display_tournament_matchs(self, tournament: Tournament):
        '''Controls the display of tournament matchs.

        '''
        self.round_view.display_matchs_list(tournament)
        validation = self.round_view.request_user_validation_for_return()
        if validation == "Y":
            return
