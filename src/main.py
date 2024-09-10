import sys
import os
import re
# sys.path.append("../")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from modules.generateInput import gen_input_file
from modules.Repo import Repo
from modules.LineObject import LineObject

def getByMethod(ProjectID, BugID, Path):
    FL_METHOD_NAME = Path+"sfl/txt/ochiai.ranking.csv"
    LineObjects = []

    # check if file exist
    if not os.path.exists(FL_METHOD_NAME):
        print(FL_METHOD_NAME + " does not exist")
        return None
    # open file
    
    with open(FL_METHOD_NAME, "r") as f:
        # ignore the first line
        f.readline()

        line = f.readline()

        while "<clinit>" in line:
            line = f.readline()

        # parse the line
        line0 = LineObject.parseLine(line)
        LineObjects.append(line0)
        # print(line0)
        for line in f.readlines():
            # if method = method_part the read and score != 0.0
            line_object = LineObject.parseLine(line)
            if line_object.class_part == line0.class_part and line_object.method_part == line0.method_part and line_object.score_part != 0.0:
                # print(line_object)
                LineObjects.append(line_object)
                # return the line
    
    # Sort the lines by line_part
    # Lines.sort(key=lambda x: x.line_part)

    for lineObject in LineObjects:
        print(lineObject)
    return LineObjects

def get_Method_Start_End( project_id, bug_id, lineObject):
    tmp_path = "/tmp/{}_{}_buggy".format(project_id, bug_id)
    class_path = tmp_path + "/src/main/java/" + lineObject.path_part + lineObject.class_part + ".java"
    # check if file exist
    if not os.path.exists(class_path):
        print(class_path + " does not exist")
        return None
    # open file
    print(class_path+ " exist")
    with open(class_path, "r") as f:
        lines = f.readlines()
        
    # method name
    method_name = lineObject.method_part.split("(")[0]
    print(method_name)

    # Combine lines into a single string
    code = ''.join(lines)

    # print(code)
    start_idx = None
    end_idx = None


    # 从指定行开始向上搜索方法的起始行
    for i in range(lineObject.line_part - 1, -1, -1):
        if method_name in lines[i]:
            # check if lines[i] is the method declaration regular expression
            pattern = '(public|protected|private|static) +[\w\<\>\[\]\,\s]*\s*(\w+) *\([^\)]*'
            print(lines[i])
            if re.match(pattern, lines[i].strip()):
                start_idx = i
                print("start_idx", start_idx)
                break
    
    if start_idx is not None:
        print(start_idx)
    
            
    # 从方法声明开始向下搜索方法的结束行
    if start_idx is not None:
        brace_count = 0

        # from start_idx to the INT MAX
        for i in range(start_idx-1, start_idx + 2000):
            # print(brace_count)
            brace_count += lines[i].count('{')
            if brace_count == 0:
                # print(brace_count)
                continue
            brace_count -= lines[i].count('}')
            if brace_count == 0:
                end_idx = i + 1
                break

    return start_idx, end_idx



FILE_NAME = "src/pid_without_sub_with_sloc_info.csv"
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

    # for repo in repos:
    #     for bug_id in repo.bug_ids:
    #         # check folder exist
    #         # folder path = "sflresults/ProjectID/BugID"
    #         # if not exist, print
    #         # path = "./sflresults/" + str(repo.project_id) + "/" + str(bug_id)
    #         # /home/zhao2z/Documents/ChinaSoft_RepairCamp_CSTAR/sflresults/AaltoXml/1/sfl/txt/ochiai.ranking.csv
    #         path = "/home/zhao2z/Documents/ChinaSoft_RepairCamp_CSTAR/sflresults/" + str(repo.project_id) + "/" + str(bug_id) + "/sfl/txt/ochiai.ranking.csv"
    #         # print(path)
    #         if not os.path.exists(path):
    #             # print id
    #             print("Index: " + str(repo.index) + ", BugID: " + str(bug_id) + " does not exist" + path)
    #             continue
        
    # repo = repos[10]
    # print(repo.project_id, repo.bug_ids[34])
    # LineObjects = getByMethod(repo.project_id, repo.bug_ids[34], "../sflresults/" + str(repo.project_id) + "/" + str(repo.bug_ids[34]) + "/")

    # start, end = get_Method_Start_End(repo.project_id, repo.bug_ids[34], LineObjects[0])
    # code_file_path = "/tmp/{}_{}_buggy/src/main/java/".format(repo.project_id, repo.bug_ids[34]) + LineObjects[0].path_part + LineObjects[0].class_part + ".java"
    # print(start, end)
    
    # line_list = []
    # for lineObject in LineObjects:
    #     line_list.append(lineObject.line_part)
    # # def gen_input_file(project_name, bug_id, package_dir, src_test_txt, info_file,  package_name , java_file_name, line_numbers, function_start_line, function_end_line):

    # gen_input_file(repo.project_id, repo.bug_ids[34], code_file_path, "source.txt", "./info.txt", LineObjects[0].path_part, LineObjects[0].class_part, line_list, start, end)

    for repo in repos:
        for bug_id in repo.bug_ids:
            try:
                print("-----------",repo.project_id, bug_id, "-----------")
                LineObjects = getByMethod(repo.project_id, bug_id, "./sflresults/" + str(repo.project_id) + "/" + str(bug_id) + "/")
                start, end = get_Method_Start_End(repo.project_id, bug_id, LineObjects[0])
                print("start", start, "end", end)
                # quit()
                code_file_path = "/tmp/{}_{}_buggy/src/main/java/".format(repo.project_id, bug_id) + LineObjects[0].path_part + LineObjects[0].class_part + ".java"
                print(code_file_path)
                line_list = []
                for lineObject in LineObjects:
                    line_list.append(lineObject.line_part)
                # print('--------')
                gen_input_file(repo.project_id, bug_id, code_file_path, "./input.txt", "./info.txt", LineObjects[0].path_part, LineObjects[0].class_part, line_list, start, end)
            # catch the error
            except Exception as e:
                print("Error: ", repo.project_id, bug_id)
                continue
            

if __name__ == '__main__':
    main()