from interactions import *
import signal
import sys
import atexit


def user_logged(name=str, session_password=str) -> None:
    """
    This function is the interface with the user after he successfully logged in and allows to add, load, edit, delete his data in his wallet.\n
    Automatically encrypts his wallet in case of a logout, a Ctrl-C/Ctrl-Z/Ctrl-D or terminal window closure (SIGTSTP/SIGBREAK).
    """

    if sys.platform != "win32":
        def handle_ctrl_z_signal(signum, frame):
            """
            Function that allows to intercept the Linux Ctrl-Z and interpret it as an exit and not as a stop.
            """
            encrypt_wallet(name, session_password)
            sys.exit(0)
    
        signal.signal(signal.SIGTSTP, handle_ctrl_z_signal)

    else:
        atexit.register(encrypt_wallet, name, session_password)

    try:
        print(f"Welcome {name} ! Please select an option :")

        while True:

            print("------------------------------\n1 - Add a credential\n2 - List your stored credentials\n3 - Edit a credential\n4 - Delete a credential\n5 - Get a credential's data\n6 - Logout\n")
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
                
                if sys.platform != "win32":
                    signal.signal(signal.SIGTSTP, signal.SIG_DFL)
                else:
                    atexit.unregister(encrypt_wallet)
                
                encrypt_wallet(name, session_password)
                return
            else:
                print("Please choose an option between 1 and 6.\n")
    
    except (KeyboardInterrupt, EOFError):

        if sys.platform == "win32":
            atexit.unregister(encrypt_wallet)
        
        encrypt_wallet(name, session_password)
        return
    
def home():
    """
    This function is the interface that the user has after executing the main python file and allows the user to log in, register, check a password, and generate a password.
    """

    try:
        print("Welcome ! Please select an option :")

        while True:

            print("------------------------------\n1 - Log In\n2 - Register\n3 - Password Checker\n4 - Generate a password\n")
            cli = str(input(">>> "))

            if cli.lower() == "1":
                
                try:
                    name = str(input("Please enter your name : "))
                    password = str(input("Please enter your password : "))

                    output = decrypt_wallet(name, password)

                    if output == -1:
                        print("The password is incorrect.")
                    elif output == -2:
                        print("This user doesn't exist.")
                    else:
                        user_logged(name, password)

                except (KeyboardInterrupt, EOFError):
                    pass

            elif cli.lower() == "2":
                register_interaction()


    except (KeyboardInterrupt, EOFError):
        pass