import json
from pathlib import Path

file_src = Path(__file__).resolve().parent


def get_index_element(name=str, app=str) -> int:
    """
    Function that gets the index in the user's .json file of the given application.\n
    Returns the index of the application in the file if found, if not, the function returns -1.
    """

    file = file_src.parent / "wallets" / f"{name}_wallet.json"

    with open(file, "r") as f:
        file_data = json.load(f)

    for i in range (len(file_data[f"Wallet of {name}"])):

        if file_data[f"Wallet of {name}"][i]["application"] == app:
            return i
    
    return -1


def add_credential_to_wallet(name=str, app=str, username=str, password=str) -> None:
    """
    Function that adds credentials to the user's wallet.\n
    Takes the user's local name, the application name, the username used and the password that he wants to store.
    """

    data_to_append = { "application" : app,
                      "username/email" : username,
                      "password" : password}
    
    file = file_src.parent / "wallets" / f"{name}_wallet.json"
    
    with open(file, "r") as f:
        file_data = json.load(f)
    
    file_data[f"Wallet of {name}"].append(data_to_append)

    with open(file, "w") as f:
        json.dump(file_data, f, indent=4)


def del_credential_from_wallet(name=str, app=str) -> int:
    """
    Function that deletes credential information of the application given from the user's .json file.\n
    Returns 0 if the information was deleted successfully and -1 if the application is not in the user's wallet.
    """

    file = file_src.parent / "wallets" / f"{name}_wallet.json"

    with open(file, "r") as f:
        file_data = json.load(f)
    
    index_app = get_index_element(name, app)

    if index_app != -1:
        del file_data[f"Wallet of {name}"][index_app]

        with open(file, "w") as f:
            json.dump(file_data, f, indent=4)
            
            return 0
        
    return -1


def list_all_applications(name=str) -> None:
    """
    Function that lists all the different credentials for every application stored in the user's wallet.
    """

    file = file_src.parent / "wallets" / f"{name}_wallet.json"

    with open(file, "r") as f:
        file_data = json.load(f)
    
    if len(file_data[f"Wallet of {name}"]) == 0:
        print("Your password wallet is empty")
    else:
        for e in file_data[f"Wallet of {name}"]:
            print(e["application"])


def edit_credential(name=str, app=str, new_app_name=str, new_username=str, new_password=str) -> int:
    """
    Function that allows the user to edit an existing credential stored in his wallet.\n
    Returns 0 if the changes have been applied and returns -1 if the given application is not in the wallet.
    """

    file = file_src.parent / "wallets" / f"{name}_wallet.json"

    with open(file, "r") as f:
        file_data = json.load(f)
    
    index_app = get_index_element(name, app)

    if index_app != -1:
        credential = file_data[f"Wallet of {name}"][index_app]

        credential["application"] = new_app_name
        credential["username/email"] = new_username
        credential["password"] = new_password

        with open(file, "w") as f:
            json.dump(file_data, f, indent=4)
        
        return 0
    
    return -1

def read_credential(name=str, app=str) -> int:
    """
    Prints all the information about a stored credential from the given user's .json file.\n
    Returns 0 if the credential was found, if not, returns -1.
    """
    file = file_src.parent / "wallets" / f"{name}_wallet.json"

    with open(file, "r") as f:
        file_data = json.load(f)
    
    index_app = get_index_element(name, app)

    credential = file_data[f"Wallet of {name}"][index_app]

    if index_app != -1:
        print(f"Application/Website Name : {credential["application"]}\nUsername/Email Address : {credential["username/email"]}\nPassword : {credential["password"]}")
        return 0
    
    return -1