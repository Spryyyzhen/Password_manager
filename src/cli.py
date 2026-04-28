from interactions import *

def user_logged(name=str, session_password=str) -> None:
    """
    The interface with the user after he successfully logged in and allows to add, load, edit, delete his data in his wallet.\n
    Automatically encrypts his wallet in case of a logout or a Ctrl-C/Ctrl-Z.
    """
    try:
        print(f"Welcome {name} ! Please select an option :")

        while True:
            print("------------------------------\n1 - Add a credential\n2 - List your stored credentials\n3 - Edit a credential\n4 - Delete a credential\n5 - Get a credential's data\n6 - Logout")
            cli = input(">>> ")

            if cli.lower() == "1":
                add_interaction(name)

            elif cli.lower() == "2":
                print("All your credentials :")
                list_all_applications(name)
                print("")

            elif cli.lower() == "3":
                edit_interaction(name)

            elif cli.lower() == "4":
                delete_interaction(name)

            elif cli.lower() == "5":
                get_data_interaction(name)
            
            elif cli.lower() == "6":
                encrypt_wallet(name, session_password)
                return
            else:
                print("Please choose an option between 1 and 6.\n")
    
    except KeyboardInterrupt:
        encrypt_wallet(name, session_password)
        return