import re

def isValidEmail(email):
    regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(regex, email) is not None

def isValidPassword(password):
    regex = r"^(?=.*[A-ZÑÁÉÍÓÚÜ])(?=.*\d)[A-Za-z\dñáéíóúüÑÁÉÍÓÚÜ]{8,}$"
    return re.match(regex, password) is not None

def isValidUserName(username):
    regex = r"^[a-zA-Z0-9]+$"
    return re.match(regex, username) is not None

