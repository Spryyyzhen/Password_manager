from password_functions import *
from wallet_functions import *
from wallet_data_functions import *


def password_gen_default_interaction() -> str:
    try:
        while True:
            ask_letters = str(input("Do you want to use normal characters (y/n)? : "))
            if ask_letters.lower() in ["y","n"]:       
                letters_bool = (ask_letters.lower() == "y")
                break
            print("Please answer either by 'y'(yes) or 'n'(no).")

        while True:
            ask_digits = str(input("Do you want to use digits (y/n)? : "))
            if ask_digits.lower() in ["y","n"]:       
                digits_bool = (ask_digits.lower() == "y")
                break
            print("Please answer either by 'y'(yes) or 'n'(no).")

        while True:
            ask_special_char = str(input("Do you want to use special characters (y/n)? : "))
            if ask_special_char.lower() in ["y","n"]:
                special_char_bool = (ask_special_char.lower() == "y")
                break
            print("Please answer either by 'y'(yes) or 'n'(no).")

        while True:
            try:
                password_length = int(input("What is the length of the password? : "))
                break
            except ValueError:
                print("Please enter an int.")
        
        password_input = password_gen(letters_bool, digits_bool, special_char_bool, password_length)
    
    except (KeyboardInterrupt, EOFError):
        pass

    return password_input


def password_gen_logged_interaction() -> str:
    """
    This function allows the user via inputs to either generate a random password or type is own password.\n 
    If the password is entered manually by the user, the password is checked if it is compromised.\n
    The function returns the str of the password (generated/typed).
    """
    try:

        while True:
            ask_randomized_pwd = str(input("Do you want to generate a randomized password (y/n)? : "))
            if ask_randomized_pwd.lower() == "y":
                password_input = password_gen_default_interaction()
                break

            elif ask_randomized_pwd.lower() == "n":
                password_input = str(input("Please enter the password : "))

                data_breaches_count = password_checker(password_input)
                if data_breaches_count > 0:
                    print(f"/!\\ CAREFUL This password has been detected in {data_breaches_count} existing data breaches, consider changing it later /!\\")
                elif data_breaches_count == -1:
                    print("The password checker was unable to connect to the HaveIBeenPwned API, consider checking the password later in case.")
                break

            else:
                print("Please answer either by 'y'(yes) or 'n'(no).")
    
    except (KeyboardInterrupt, EOFError):
        pass

    return password_input


def add_interaction(name=str) -> None:
    """
    This function allows the user to add a credential to his wallet via inputs.
    """
    try:
        app_input = str(input("Name of the application/website : "))
        app_exists = get_index_element(name, app_input)
        if app_exists != -1:
            print(f"The {app_input}'s credential already exists.")
            return
        
        username_input = str(input("Username or Email Address : "))
        password_input = password_gen_logged_interaction()
        add_credential_to_wallet(name, app_input, username_input, password_input)
        print("Credential added successfully.\n")

    except (KeyboardInterrupt, EOFError):
        pass


def edit_interaction(name=str) -> None:
    """
    This function allows the user to edit via inputs an existing credential.
    """
    try:

        app_input = str(input("Name of the actual application/website : "))
        app_exists = get_index_element(name, app_input)
        if app_exists == -1:
            print(f"The {app_input}'s credential doesn't exist.\n")
            return
        
        new_app_input = str(input("New name of the application/website : "))
        username_input = str(input("New Username or Email Address : "))
        print("New Password : ")
        password_input = password_gen_logged_interaction()
        
        edit_credential(name, app_input, new_app_input, username_input, password_input)
        print("Credentials changed successfully.\n")

    except (KeyboardInterrupt, EOFError):
        pass


def delete_interaction(name=str) -> None:
    """
    This function allows the user to delete a credential via inputs.
    """
    try:

        app_input = str(input("Name of the application/website to delete : "))
        output = del_credential_from_wallet(name, app_input)

        if output == -1:
            print(f"The {app_input}'s credential doesn't exist.\n")
        else:
            print("Credential deleted successfully.\n")

    except (KeyboardInterrupt, EOFError):
        pass

def get_data_interaction(name=str, ) -> None:
    """
    This function allows the user to load a credential's data via inputs.
    """
    try:

        app_input = str(input("Name of the application/website : "))
        print("")
        output = read_credential(name, app_input)

        if output == -1:
            print(f"The {app_input}'s credential doesn't exist.\n")

    except (KeyboardInterrupt, EOFError):
        pass


def register_interaction() -> None:
    """
    Function that allows interaction with the user via inputs to register (create a new wallet) in the password manager CLI.\n
    Checks if the password entered is compromised, if it's the case, the function asks the user if he wants to use it anyway.
    """
    try:
        while True:

            name = str(input("Please enter your name : "))
            password = str(input("Please enter a main password (/!\\ REMEMBER IT /!\\) : "))
            output = password_checker(password)

            if output > 0:
                while True:
                    ask_final_pwd = str(input("The entered password has been detected in data breaches ! Do you want to use it anyway (y/n)? : "))

                    if ask_final_pwd.lower() == "y":
                        break

                    elif ask_final_pwd.lower() == "n":
                            while True:
                                password = str(input("Please enter the main password again (/!\\ REMEMBER IT /!\\) : "))
                                output = password_checker(password)

                                if output > 0:
                                    print("This password has also been detected in data breaches.")
                                elif output == -1:
                                    print("The password checker was unable to connect to the HaveIBeenPwned API, consider checking the password later in case.")
                                else:
                                    break                            
                    else:
                        print("Please enter either 'y' or 'n'.")
                    break

            elif output == -1:
                print("The password checker was unable to connect to the HaveIBeenPwned API, consider checking the password later in case.")
            
            try_create = create_wallet(name, password)
            if try_create == -1:
                print("This user already exists.")
            elif try_create == 0:
                print("New user added successfully !")
                break

    except (KeyboardInterrupt, EOFError):
        pass