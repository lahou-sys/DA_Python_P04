from abc import ABC

from utils.utils import (date_compare_if_previous, date_now, datetime_to_str,
                         is_date_format, valid_name)


class AbstractView(ABC):
    """
    Common class for views

    """
    @staticmethod
    def main_menu_who_display_possible_choice_to_user():
        '''Display of choices for the main menu.

        '''
        print(f'{"=" * 119}')
        print(f'{"* MENU PRINCIPAL*"}'.center(119))
        print("1. Ajouter un nouveau joueur")
        print("2. Créer un tournoi")
        print("3. Reprendre avec un tournoi existant")
        print("4. Afficher la liste des joueurs")
        print("5. Afficher la liste des tournois")
        print("0. Quitter le programme")
        print(f'{"=" * 119}')

    @staticmethod
    def get_user_choice(limit_choice):
        '''Returns the user's choice.

        '''
        user_choice = ""
        while user_choice not in range(limit_choice):
            try:
                user_choice = int(input("Choisissez ce que vous souhaitez faire :"))
            except (ValueError, TypeError):
                print("Désolé votre réponse n'est pas valide")
        return user_choice

    @staticmethod
    def exit_program():
        '''Displays the end of program message.

        '''
        print("Merci d'avoir utilisé ce programme, à bientôt !")

    @staticmethod
    def request_confirmation():
        '''Returns the user's confirmation.

        '''
        validation = ""
        while validation not in ["Y", "N"]:
            validation = input("Confirmez-vous cela ? (Y/N): ").upper()
            if validation not in ["Y", "N"]:
                print(
                    "Je n'ai pas pu identifier votre réponse, veuillez la saisir à nouveau s'il vous plaît."
                )
            return validation

    @staticmethod
    def request_user_validation_for_return():
        '''Returns user confirmation of return to menu.

        '''
        validation = ""
        while validation not in ["Y"]:
            validation = input("Pour retourner au menu veuillez saisir 'Y': ").upper()
            if validation not in ["Y"]:
                print(
                    "Je n'ai pas pu identifier votre réponse, veuillez la saisir à nouveau s'il vous plaît."
                )
            return validation

    @staticmethod
    def request_user_validation_to_continue():
        '''Returns the user's choice of whether to continue.

        '''
        validation = ""
        while validation not in ["Y", "N"]:
            validation = input("Pour continuer saisir 'Y' ou sinon 'N': ").upper()
            if validation not in ["Y", "N"]:
                print(
                    "Je n'ai pas pu identifier votre réponse, veuillez la saisir à nouveau s'il vous plaît."
                )
            return validation

    @staticmethod
    def display_message_to_user(message: str):
        '''Displays a message to the user.

        '''
        print(f"{message}")

    def get_string_value(self, first_argument: str, second_argument: str):
        '''Prompts the user to enter a character string with an input check.

        '''
        validate = ""
        while validate != "Y":
            value = input(f"Veuillez saisir {first_argument} du {second_argument}: ")
            if not value:
                print("Votre saisie n'a pas été comprise")
                print(
                    f"veuillez rééssayer d'indiquer {first_argument} du {second_argument}"
                )
            else:
                print(f"{first_argument} du {second_argument} est : {value}")
                validate = self.request_confirmation()
                if validate == "Y":
                    return value

    def get_valide_name(self, first_argument: str, second_argument: str):
        '''Prompts the user to enter a valid first or last name with input verification.

        '''
        validate = ""
        while validate != "Y":
            value = input(f"Veuillez saisir {first_argument} du {second_argument}: ")
            if not value or not valid_name(value):
                print("Votre saisie n'a pas été comprise, les chiffres et caractères spéciaux ne sont pas acceptés.")
                print(
                    f"veuillez rééssayer d'indiquer {first_argument} du {second_argument}"
                )
            else:
                print(f"{first_argument} du {second_argument} est : {value}")
                validate = self.request_confirmation()
                if validate == "Y":
                    return value

    def get_integer_value(self, first_argument: str, second_argument: str):
        '''Prompts the user to enter a valid first or last name with input verification.

        '''
        validate = ""
        while validate != "Y":
            value = input(f"Veuillez saisir {first_argument} du {second_argument}: ")
            if not value.isnumeric() or not value:
                print("Votre saisie n'a pas été comprise")
                print(
                    f"veuillez rééssayer d'indiquer {first_argument} du {second_argument}"
                )
            else:
                print(f"{first_argument} du {second_argument} est : {value}")
                validate = self.request_confirmation()
                if validate == "Y":
                    return value

    def get_number_of_turn(self, first_argument: str, second_argument: str, default_value=None):
        '''Prompt the user to enter an integer for the number
        of turns with an input check.

        '''
        validate = ""
        while validate != "Y":
            value = input(f"Veuillez saisir {first_argument} de {second_argument}: ")
            if value:
                if not value.isnumeric():
                    print("Votre saisie n'a pas été comprise")
                    print(
                        f"veuillez rééssayer d'indiquer {first_argument} de {second_argument}"
                    )
                else:
                    print(f"{first_argument} de tours est : {value}")
                    validate = self.request_confirmation()
                    if validate == "Y":
                        return int(value)
            else:
                print(f"Le nombre de tours est {default_value} (la valeur par défaut).")
                print(default_value)
                validate = self.request_confirmation()
                if validate == "Y":
                    return int(default_value)

    def get_number_of_player(self, first_argument: str, second_argument: str, default_value=None):
        '''Prompt the user to enter an integer and even number
        for the player number with input verification.

        '''
        validate = ""
        while validate != "Y":
            value = input(f"Veuillez saisir {first_argument} de {second_argument}: ")
            if value:
                if not value.isnumeric():
                    print("Votre saisie n'a pas été comprise")
                    print(f"veuillez rééssayer d'indiquer {first_argument} de {second_argument}")
                else:
                    if int(value) % 2 != 0:
                        print(f"Le nombre saisie '{value}' n'est pas paire")
                        print(f"veuillez rééssayer d'indiquer {first_argument} de {second_argument}")
                    else:
                        print(f"{first_argument} de joueur est : {value}")
                        validate = self.request_confirmation()
                        if validate == "Y":
                            return int(value)
            else:
                print(f"{first_argument} de joueur est {default_value} (la valeur par défaut).")
                print(default_value)
                validate = self.request_confirmation()
                if validate == "Y":
                    return int(default_value)

    def verify_date_birthday(self, date, first_argument: str, second_argument: str, key: str, format_date):
        '''Checks if the date corresponds to a date of birth.

        '''
        validate = ""
        while validate != "Y":
            if (date and is_date_format(date) and datetime_to_str(is_date_format(date))
                    and date_compare_if_previous(date_now(), date)
                    and key == "birthday"):
                print(f"{first_argument} du {second_argument} est : {date}")
                validate = self.request_confirmation()
                if validate == "Y":
                    return date
            else:
                print("Votre saisie n'est pas correct ou le joueur est trop jeune (ou pas encore né) ! ")
                print(
                    f"veuillez rééssayer d'indiquer {first_argument} du {second_argument} ({format_date})")
                date = input(f"Veuillez saisir {first_argument} du {second_argument} ({format_date}) : ")
                date = datetime_to_str(is_date_format(date))

    def verify_date_tournament(
                            self, date, first_argument: str, second_argument: str, key: str,
                            format_date,
                            option=None
                            ):
        '''Checks if the start and end dates of tournaments are correct.

        '''
        validate = ""
        while validate != "Y":
            if key == "start_tournoi":
                print(f"{first_argument} du {second_argument} est : {date}")
                validate = self.request_confirmation()
                if validate == "Y":
                    return date
            elif key == "end_tournoi":
                if (date and is_date_format(date) and datetime_to_str(is_date_format(date))
                        and not date_compare_if_previous(option, date)):
                    print(f"{first_argument} du {second_argument} est : {date}")
                    validate = self.request_confirmation()
                    if validate == "Y":
                        return date
                else:
                    print(
                        "Votre saisie n'est pas correct ou"
                        + f"la date de fin doit être identique ou postérieur au {option} ! ")
                    print(
                        f"veuillez rééssayer d'indiquer {first_argument} du {second_argument} ({format_date})")
                    date = input(f"Veuillez saisir {first_argument} du {second_argument} ({format_date}) : ")
                    date = datetime_to_str(is_date_format(date))

    def verify_date(self, value, first_argument: str, second_argument: str, key: str, format_date, option=None):
        '''Checks if the dates are in the correct format and correspond to valid dates.

        '''
        validate = ""
        while validate != "Y":
            if not value or not is_date_format(value):
                print("Votre saisie n'est pas au bon format")
                print(
                    f"veuillez rééssayer d'indiquer {first_argument} du {second_argument} ({format_date})")
                value = input(f"Veuillez saisir {first_argument} du {second_argument} ({format_date}) : ")
            else:
                if not value or not is_date_format(value) or not datetime_to_str(is_date_format(value)):
                    print("Votre saisie n'est pas correcte")
                    print(
                        f"veuillez rééssayer d'indiquer {first_argument} du {second_argument} ({format_date})")
                    value = input(f"Veuillez saisir {first_argument} du {second_argument} ({format_date}) : ")
                else:
                    date = datetime_to_str(is_date_format(value))
                    validate = "Y"
        if key == "birthday":
            result = self.verify_date_birthday(date, first_argument, second_argument, key, format_date)
            validate = "Y"
            return result
        elif key == "start_tournoi" or key == "end_tournoi":
            result = self.verify_date_tournament(date, first_argument, second_argument, key, format_date, option)
            validate = "Y"
            return result

    def get_date_format(self, first_argument: str, second_argument: str, key: str, option=None):
        '''Prompts the user to enter a date in the correct format.

        '''
        format_date = "JJ/MM/AAAA"
        validate = ""
        while validate != "Y":
            value = input(f"Veuillez saisir {first_argument} du {second_argument} ({format_date}) : ")
            if not value:
                print("Votre saisie n'a pas été comprise")
                print(
                    f"veuillez rééssayer d'indiquer {first_argument} du {second_argument} ({format_date})")
            else:
                result = self.verify_date(value, first_argument, second_argument, key, format_date, option)
                validate = "Y"
        return result
