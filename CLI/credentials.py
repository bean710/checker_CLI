import requests
import os
import sys

def getToken(refresh=False):
    tfile = os.path.expanduser("~/.ccli/token")
    tok = ""
    try:
        f = open(tfile, "r")
        tok = f.read()
        if tok == "" or refresh:
            raise FileNotFoundError
        return (tok)
    except FileNotFoundError:
        if not os.path.exists(os.path.expanduser("~/.ccli/")):
            os.mkdir(os.path.expanduser("~/.ccli/"))
        api_key = input("Please enter API key: ")
        email = input("Please enter your holberton email: ")
        password = input("Please enter your holberton password: ")
        res = ""
        try:
            res = requests.post("https://intranet.hbtn.io/users/auth_token.json",
                                  json={
                                    "api_key": api_key,
                                    "email": email,
                                    "password": password,
                                    "scope": "checker"
                                  });
        except TypeError:
            print("CheckerCLI requires `requests` version 2.4.2 or later to run.")
            print("Use `sudo pip3 install --upgrade requests` to get it.")
        if not res or res.status_code != 200:
            print("Error authenticating. Please make sure your information is correct.")
            sys.exit(1)
        f = open(tfile, "w")
        tok = res.json()["auth_token"]
        f.write(tok)
        f.close()
        print (tok)
        return tok

