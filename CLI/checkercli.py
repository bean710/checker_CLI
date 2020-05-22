#!/usr/bin/python3
import sys
import os
import requests
import json
from time import sleep
from random import randint, uniform

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

def help():
    print("Help for Checker CLI:")
    print("")
    print("\033[1mCommands:\033[0m")
    print("\tstatus <project_id> [task_num]\t: Gets the status of a "+
          "certain project or task")
    print("\t\tproject_id\t: The ID of the project to get the " +
          "status of, \n\t\t\t\t  or contains the task to get the status of")
    print("\t\ttask_num\t: (Optional) The number of the task to " +
          "get the status of")
    print("\t\t\033[1mColor Code:\033[0m (When getting project status)")
    print("\t\t\t\033[0mWhite\t: Task has not been checked with CheckerCLI")
    print("\t\t\t\033[32mGreen\033[0m\t: Task has passed all checks")
    print("\t\t\t\033[31mRed\033[0m\t: Task has not passed all checks")
    print("")
    print("\tcheck <project_id> <task_num>\t: Checks a certain task")
    print("\t\tproject_id\t: The ID of the project that has the task to check")
    print("\t\ttask_num\t: The number of the task to check")
    print("")
    print("\trefresh\t: Prompts credential refresh")
    print("")
    #print("\trun\t: Pushes code and runs checker")
   # print("\t\t-d{n}\t: Dry mode. Runs checker for task `n` without " +
   #       "pushing new code. \n\t\t\t  Note: `n` should be the number next " +
   #       "to the task, not the file prefix.")
   # print("")
    print("\t -h, --help\t: Shows this help output")
    print("")

def set_check(projnum, tasknum, status, token):
    tasknum = int(tasknum)
    try:
        f = open(os.path.expanduser("~/.ccli/projects/{}".format(projnum)), "r")
        dat = json.load(f)

        dat["tasks"][tasknum]["cstatus"] = status

        f.close()

        f = open(os.path.expanduser("~/.ccli/projects/{}".format(projnum)), "w")
        json.dump(dat, f)
        f.close()

    except FileNotFoundError:
        if not os.path.exists(os.path.expanduser("~/.ccli/projects/")):
            os.mkdir(os.path.expanduser("~/.ccli/projects"))
        f = open(os.path.expanduser("~/.ccli/projects/{}".format(projnum)), "w")
        res = requests.get("https://intranet.hbtn.io/projects/{}.json"\
                           .format(projnum),
                           params={"auth_token" : token})
        if (not res or res.status_code != 200):
            print("Error with the request. Try refreshing credentials.")
            print(res)
            print(res.json())
            sys.exit(1)

        dat = res.json()
        print("\033[1m{}\033[0m".format(dat["name"]))
        for i in range(len(dat["tasks"])):
            task = dat["tasks"][i]
            task["cstatus"] = "not_checked"

        json.dump(dat, f)


def get_loc_status(projnum, token):
    try:
        f = open(os.path.expanduser("~/.ccli/projects/{}".format(projnum)), "r")
        dat = json.load(f)

        print("\033[1m{}\033[0m".format(dat["name"]))
        for i in range(len(dat["tasks"])):
            task = dat["tasks"][i]
            status = task["cstatus"]
            if (status == "not_checked"):
                color = "\033[0m"
            elif (status == "fail"):
                color = "\033[31m"
            elif (status == "pass"):
                color = "\033[32m"
            else:
                color = "\033[0m"
            print("{}: {}{}\033[0m".format(i, color, task["title"]))
    except FileNotFoundError:
        if not os.path.exists(os.path.expanduser("~/.ccli/projects/")):
            os.mkdir(os.path.expanduser("~/.ccli/projects"))
        f = open(os.path.expanduser("~/.ccli/projects/{}".format(projnum)), "w")
        res = requests.get("https://intranet.hbtn.io/projects/{}.json"\
                           .format(projnum),
                           params={"auth_token" : token})
        if (not res or res.status_code != 200):
            print("Error with the request. Try refreshing credentials.")
            print(res)
            print(res.json())
            sys.exit(1)

        dat = res.json()
        print("\033[1m{}\033[0m".format(dat["name"]))
        for i in range(len(dat["tasks"])):
            task = dat["tasks"][i]
            task["cstatus"] = "not_checked"
            print("{}: {}".format(i, task["title"]))

        json.dump(dat, f)


def check(projnum, tasknum, token):
    pass_phrase = ["Dynomite!", "You’re Winner", "Achievement Obtained: Passed Checker", "Looks like a win-win-win situation", "Let’s hope the next task won’t be a trainwreck", "if you're not first, you're last - Ricky Bobby", "The checker has been defeated. Obtained: 98xp", "If Julien gave you a dollar for every check you got, how quickly on the road to bankruptcy would Julien be?", "Start practicing your happy dance; the checker approves of your code!", "Winning may not be everything, but as far as the checker is concerned it’s all that matters.", "forty-two"]

    fail_phrase = ["Should have tested it before you pushed", "You miss all of the shots you don\’t take - Wayne Gretzky. - Michael Scott.", "Fission Mailed", "Abe Lincoln had a brighter future when he picked up his tickets at the box office", "It is possible to commit no mistakes and still lose", "Nice job failing it, hero", "Throw me a frickin' bone here!", "It’s okay to be imperfect. After all, I AM perfect", "Son of a nutcracker!", "Trying is the first step toward failure", "You're killing me, Smalls!", "You are Error"]

    load_phrase = [" checking...", " testing...", " loading...", " running...", " failing...", " breaking...", " waiting..."]

    res = requests.get("https://intranet.hbtn.io/projects/{}.json"\
                       .format(projnum),
                       params={"auth_token" : token})
    if (not res or res.status_code != 200):
        print("Error with the request. Try refreshing credentials.")
        print(res)
        print(res.json())
        sys.exit(1)

    dat = res.json()
    task_id = dat["tasks"][int(tasknum)]["id"]
    print("Checking task {} of project {}".format(tasknum,
                                                  dat["name"]))
    res = requests.post("https://intranet.hbtn.io/tasks/{}/start_correction.json"\
                        .format(task_id),
                        params={"auth_token" : token})
    dat = res.json()
    check_id = dat["id"]
    done = False
    while (not done):
        sleep(1)
        res = requests.get("https://intranet.hbtn.io/correction_requests/{}.json"\
                           .format(check_id),
                           params={"auth_token" : token})
        dat = res.json()
        if (dat["status"] == "Done"):
            done = True
            checks = dat["result_display"]["checks"]
            gotOneWrong = False
            for check in checks:
                if (check["passed"]):
                    print("\033[32my\033[0m", end="")
                else:
                    gotOneWrong = True
                    print("\033[31mn\033[0m", end="")
            print("")
            if gotOneWrong:
                set_check(projnum, tasknum, "fail", token)
                sentence_num = randint(0, len(fail_phrase) - 1)
                print("{}".format(fail_phrase[sentence_num])) # checker fail
            else:
                set_check(projnum, tasknum, "pass", token)
                sentence_num = randint(0, len(pass_phrase) - 1)
                print("{}".format(pass_phrase[sentence_num])) # checker pass
        else:
            # Randomly prints out a message that the checker is still running
            # one letter at a time, in random float delay in between
            num = randint(0, len(load_phrase) - 1)
            string = "Now" + load_phrase[num]

            for i in string:
                print(i, end='')
                sys.stdout.flush()
                sleep(uniform(0.01, 0.5))

            print("")
            sys.stdout.flush()
            sleep(uniform(0.01, 0.5))

if __name__ == "__main__":
    token = getToken()
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if (command in set(["-h", "--help"])):
            help()
        elif (command == "run"):
            dry = -1
            if len(sys.argv) > 2:
                flag = sys.argv[2]
                if len(flag) > 2 and flag[:2] == "-d":
                    try:
                        dry = int(flag[2:])
                    except:
                        print("Not a valid value for `n`!")

            if dry == -1:
                os.system("echo 'Replace this with git push code'")
            os.system("echo 'Replace this with checker API code'")
        elif (command == "status"):
            if len(sys.argv) > 2:
                if len(sys.argv) == 3:
                    projnum = sys.argv[2]
                    get_loc_status(projnum, token)
                else:
                    projnum = sys.argv[2]
                    tasknum = sys.argv[3]
                    res = requests.get("https://intranet.hbtn.io/projects/{}.json"\
                                       .format(projnum),
                                       params={"auth_token" : token})
                    if (not res or res.status_code != 200):
                        print("Error with the request. Your token may have expired.  Try refreshing credentials.")
                        print(res)
                        print(res.json())
                        sys.exit(1)

                    dat = res.json()
                    task = dat["tasks"][int(tasknum)]
                    print("Task {}: \033[1m{}\033[0m".format(int(tasknum), task["title"]))
                    if task["checker_available"]:
                        print("Checker is available for this task")
                    else:
                        print("Checker is not available for this task")

            else:
                print("Not enough arguments. Run `checkercli --help`")
        elif (command == "check"):
            if len(sys.argv) >= 4:
                projnum = sys.argv[2]
                tasknum = sys.argv[3]
                check(projnum, tasknum, token)
            else:
                print("Not enough arguments. Run `checkercli --help`")
        elif (command == "refresh"):
            getToken(refresh=True)
        else:
            print("Run `checkercli --help` for help")
    else:
        help()

