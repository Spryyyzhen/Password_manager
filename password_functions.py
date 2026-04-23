import random
import string
import hashlib
import requests

def password_gen(letters=bool, numbers=bool, specials=bool, length=int) -> str:
    # Function that generate random passwords
    
    characterlist = ""
    password = ""
    
    if letters:
        characterlist += string.ascii_letters
    if numbers:
        characterlist += string.digits
    if specials:
        characterlist += string.punctuation
    
    for i in range(length):
        password += random.choice(characterlist)
    
    return password

def password_checker(password=str) -> int:
    # Function that checks via the HaveIBeenPwned API if the given password was already compromised
    # Returns the number of data breaches where this password appears

    sha_pwd = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix = sha_pwd[:5]
    suffix = sha_pwd[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)

    if response.status_code != 200:
        print("Error connecting to the API")
        return -1
    
    for line in response.text.splitlines():
        returned_suffix, count = line.split(':')
        if returned_suffix == suffix:
            return int(count)
    return 0
        

print(password_checker("password"))
print(password_gen(True, True, True, 20))