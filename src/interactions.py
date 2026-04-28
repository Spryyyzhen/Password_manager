from password_functions import *
from wallet_functions import *
from wallet_data_functions import *


def password_gen_interaction() -> str:
    """
    This function allows the user via inputs to either generate a random password or type is own password, it also checks if the password is compromised.\n
    The function returns the str of the password (generated/typed)
    """

    while True:
        ask_randomized_pwd = str(input("Do you want to generate a randomized password (y/n)? : "))
        if ask_randomized_pwd.lower() == "y":
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
            break

        elif ask_randomized_pwd.lower() == "n":
            password_input = str(input("Password : "))
            break

        else:
            print("Please answer either by 'y'(yes) or 'n'(no).")
    
    data_breaches_count = password_checker(password_input)
    if data_breaches_count > 0:
        print(f"/!\\ CAREFUL This password has been detected in {data_breaches_count} existing data breaches, consider changing it later /!\\")
    elif data_breaches_count == -1:
        print("The password checker was unable to connect to the HaveIBeenPwned API, try checking the password later in case.")
    return password_input


def add_interaction(name=str) -> None:
    """
    This function allows the user to add a credential to his wallet via inputs.
    """

    app_input = str(input("Name of the application/website : "))
    app_exists = get_index_element(name, app_input)
    if app_exists != -1:
        print(f"The {app_input}'s credential already exists.")
        return
    
    username_input = str(input("Username or Email Address : "))
    password_input = password_gen_interaction()
    add_credential_to_wallet(name, app_input, username_input, password_input)
    print("Credential added successfully.\n")


def edit_interaction(name=str) -> None:
    """
    This function allows the user to edit via inputs an existing credential.
    """

    app_input = str(input("Name of the actual application/website : "))
    app_exists = get_index_element(name, app_input)
    if app_exists == -1:
        print(f"The {app_input}'s credential doesn't exist.\n")
        return
    
    new_app_input = str(input("New name of the application/website : "))
    username_input = str(input("New Username or Email Address : "))
    print("New Password : ")
    password_input = password_gen_interaction()
    
    edit_credential(name, app_input, new_app_input, username_input, password_input)
    print("Credentials changed successfully.\n")


def delete_interaction(name) -> None:
    """
    This function allows the user to delete a credential via inputs.
    """

    app_input = str(input("Name of the application/website to delete : "))
    output = del_credential_from_wallet(name, app_input)

    if output == -1:
        print(f"The {app_input}'s credential doesn't exist.\n")
    else:
        print("Credential deleted successfully.\n")


def get_data_interaction(name) -> None:
    """
    This function allows the user to load a credential's data via inputs.
    """

    app_input = str(input("Name of the application/website : "))
    print("")
    output = read_credential(name, app_input)

    if output == -1:
        print(f"The {app_input}'s credential doesn't exist.\n")