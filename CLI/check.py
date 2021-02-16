import sys
import os
import requests
import json
from time import sleep
from random import randint, uniform

def get_loc_status(projnum, token):
    """ Get the status of a certain project """
    try:
        # Try getting the project data from cache
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
        # If the project doesn't exist in the cache, get it from the API
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


def set_check(projnum, tasknum, status, token):
    """ Update the status of a task in the cache """
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
        # Task isn't found in the cache, get it from API
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
        for i in range(len(dat["tasks"])):
            task = dat["tasks"][i]
            task["cstatus"] = "not_checked"

        json.dump(dat, f)

def check(projnum, tasknum, token):
    """ Main checking function """
    pass_phrase = ["Dynomite!", "You’re Winner", "Achievement Obtained: Passed Checker", "Looks like a win-win-win situation", "Let’s hope the next task won’t be a trainwreck", "if you're not first, you're last - Ricky Bobby", "The checker has been defeated. Obtained: 98xp", "If Julien gave you a dollar for every check you got, how quickly on the road to bankruptcy would Julien be?", "Start practicing your happy dance; the checker approves of your code!", "Winning may not be everything, but as far as the checker is concerned it’s all that matters.", "forty-two"]

    fail_phrase = ["Should have tested it before you pushed", "You miss all of the shots you don’t take - Wayne Gretzky. - Michael Scott.", "Fission Mailed", "Abe Lincoln had a brighter future when he picked up his tickets at the box office", "It is possible to commit no mistakes and still lose", "Nice job failing it, hero", "Throw me a frickin' bone here!", "It’s okay to be imperfect. After all, I AM perfect", "Son of a nutcracker!", "Trying is the first step toward failure", "You're killing me, Smalls!", "You are Error"]

    load_phrase = [" checking...", " testing...", " loading...", " running...", " failing...", " breaking...", " waiting..."]

    # Run the checker via API call
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
    # Loop until check is finished on Holberton's side by pinging API
    while (not done):
        sleep(1)
        res = requests.get("https://intranet.hbtn.io/correction_requests/{}.json"\
                           .format(check_id),
                           params={"auth_token" : token})
        dat = res.json()

        # API returned that check is done, load results
        if (dat["status"] == "Done"):
            done = True
            checks = dat["result_display"]["checks"]
            gotOneWrong = False
            for check in checks:
                label = check["check_label"]
                if (label == "requirement"):
                    if (check["passed"]):
                        print("\033[0m\u2713\033[0m", end='')
                    else:
                        gotOneWrong = True
                        print("\033[0m\u2717\033[0m", end="")
                elif (label == "code"):
                    if (check["passed"]):
                        print("\033[32;1m\u2713\033[0m", end="")
                    else:
                        gotOneWrong = True
                        print("\033[31;1m\u2717\033[0m", end="")
                elif (label == "answer"):
                    if (check["passed"]):
                        print("\033[34;1m\u2713\033[0m", end="")
                    else:
                        gotOneWrong = True
                        print("\033[33;1m\u2717\033[0m", end="")
                elif (label == "efficienct"):
                    if (check["passed"]):
                        print("\033[95;1m\u2713\033[0m", end="")
                    else:
                        gotOneWrong = True
                        print("\033[93;1m\u2717\033[0m", end="")
            print("")
            if gotOneWrong:
                # Save fail into cache
                set_check(projnum, tasknum, "fail", token)
                sentence_num = randint(0, len(fail_phrase) - 1)
                print("{}".format(fail_phrase[sentence_num])) # checker fail
            else:
                # Save pass into cache
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
