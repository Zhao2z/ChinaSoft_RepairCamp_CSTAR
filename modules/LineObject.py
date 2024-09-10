import re

class LineObject:
    # Five attributes: path_part, class_part, method_part, line_part, score_part
    def __init__(self, path_part, class_part, method_part, line_part, score_part):
        self.path_part = path_part
        self.class_part = class_part
        self.method_part = method_part
        self.line_part = line_part
        self.score_part = score_part

    def __str__(self) -> str:
        return "Path: " + self.path_part + ", Class: " + self.class_part + ", Method: " + self.method_part + ", Line: " + str(self.line_part) + ", Score: " + str(self.score_part)
    
    # Static method to parse a line and create a Line object
    @staticmethod
    def parseLine(line: str):
        parts = line.split("#")
        path_part = parts[0].replace(".", "/").split("$")[0]+"/"
        class_part = parts[0].split(".")[-1].split("$")[1]
        # <clinit>() remove the <> keep the clinit()
        # method_part = parts[1].split(":")[0]
        method_part = parts[1].split(":")[0].replace("<", "").replace(">", "")

        line_part = int(parts[1].split(":")[1].split(";")[0])
        score_part = float(parts[1].split(":")[1].split(";")[1].strip())
        return LineObject(path_part, class_part, method_part, line_part, score_part)
    