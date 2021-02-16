#!/usr/bin/python3
import sys
import os
import requests
import json
from time import sleep
from random import randint, uniform
from credentials import getToken
from help import help
from check import check, set_check, get_loc_status

if __name__ == "__main__":
    token = getToken()
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if (command in set(["-h", "--help"])):
            help()
        elif (command == "run"):
            # Command used mostly for debugging
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
            # Get the results from the last time the task was checked, or check it if a task was specified
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
            # Check a project's task
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

