import os
from ChinaSoft_RepairCamp_CSTAR.modules.Repo import Repo

EXPORT = "export PATH=$PATH:\"/home/zhao2z/Documents/GrowingBugs/GrowingBugRepository/framework/bin\""
DEFECTS4J = "/home/zhao2z/Documents/GrowingBugs/GrowingBugRepository/framework/bin/defects4j"
FILE_NAME = "pid_without_sub_with_sloc_info.csv"

repos = []

def main():
    # read from "pid_without_sub_with_sloc_info.csv"
    with open(FILE_NAME, "r") as f:
        # ignore the first line
        # index|ProjectID|Projectname|Numberofbugs|BugIDs
        f.readline()
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            # split by "|"
            parts = line.split("|")
            # convert the parts to the correct types
            # str to int
            parts[0] = int(parts[0])
            parts[3] = int(parts[3])
            # str to int list
            parts[4] = list(map(int,parts[4][1:-1].split(",")))
            # create a Repo object
            repo = Repo(parts[0], parts[1], parts[2], None, parts[3], parts[4])
            # add the Repo object to the list
            repos.append(repo)
    
    # run export command
    # os.system(EXPORT)
    
    for repo in repos:
        for bug_id in repo.bug_ids:
            checkout_command = DEFECTS4J + " checkout -p {} -v {}b -w /tmp/{}_{}_buggy".format(repo.project_id, bug_id, repo.project_id, bug_id)
            # write command to "checkoutAll.sh"
            with open("checkoutAll.sh", "a") as f:
                f.write(checkout_command + "\n")
            
            




if __name__ == '__main__':
    main()