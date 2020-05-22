#!/usr/bin/python3
import sys
import os

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if (command in set(["-h", "--help"])):
            print("Help for Checker CLI:")
            print("")
            print("\033[1mCommands:\033[0m")
            print("\trun\t: Pushes code and runs checker")
            print("")
            print("\033[1mOptions:\033[0m")
            print("\t-d{n}\t: Dry mode. Runs checker for task `n` without " +
                  "pushing new code. Note: `n` should be the number next " +
                  "to the task, not the file prefix.")
            print("")
        elif (command == "run"):
            dry = -1
            if len(sys.argv) > 2:
                flag = sys.argv[2]
                if len(flag) >= 2:
                    if flag[:2] == "-d":
                        if len(flag) > 2:
                            try:
                                dry = int(flag[2:])
                            except:
                                print("Not a valid value for `n`!")

            if dry == -1:
                os.system("echo 'Replace this with git push code'")
            os.system("echo 'Replace this with checker API code'")
