import os

import datetime

path_commits = "../.git/logs/refs/heads"


def preprocessString(s):
    s = s.split("\t")
    result = []
    for i in range(len(s)):
        result.extend(s[i].split())
    result[5] = datetime.datetime.fromtimestamp(int(result[5])).__str__()
    return result


def createGraph(graph, hist, path):
    with open(path, "r") as file:
        current_branch = os.path.basename(file.name)
        for line in file.readlines():
            line = preprocessString(line)
            if line[7].startswith('commit'):
                hist[line[0]] = hist.get(line[0], [])+[(line[1], line[2], line[3], line[5])]



if __name__ == "__main__":
    dot = []
    tree = {}
    for filename in os.listdir(path_commits):
        f = os.path.join(path_commits, filename)

        if os.path.isfile(f):
            createGraph(dot, tree, f)

    for k, v in tree.items():
        print(k, v)
    # dot.render(view=True)

# for i in os.listdir("../.git/objects/61"):
#     with open(os.path.join("../.git/objects/61", i), "rb") as f:
#         print(f.readline().decode("utf-8"))
