import os

import datetime

path_commits = "../.git/logs/refs/heads"

print(os.listdir(path_commits))


def preprocessString(s):
    s = s.split("\t")
    result = []
    for i in range(len(s)):
        result.extend(s[i].split())
    # result[5] = datetime.datetime.fromtimestamp(int(result[5])).__str__()
    result[5] = int(result[5])
    return result

def findCommitMergeWith(branch, t, hist):
    comm_name = ""
    curr_time = 0
    for key in hist:
        for item in hist[key]:
            comm_time = item[1]
            if item[0].startswith(branch) and comm_time<t and comm_time>curr_time:
                comm_name = item[0]
                curr_time = comm_time

    return comm_name
def preprocessMerges(dot, d):
    for key in d:
        for item in d[key]:
            if item[2] == "merge":
                to_merge = findCommitMergeWith(item[3], item[1], d)
                dot.append(f"{to_merge} -> {item[0]};")



def createGraph(graph, hist, path):
    with open(path, "r") as file:
        current_branch = os.path.basename(file.name)
        print(current_branch)
        for line in file.readlines():
            line = preprocessString(line)

            line[0] = current_branch+"_"+line[0][:7]
            line[1] = current_branch+"_"+line[1][:7]
            print(line)
            if line[7].startswith("commit"):
                line[7] = "commit"
                hist[line[0]] = hist.get(line[0], []) + [(line[1], line[5], line[7])]
            elif line[7].startswith("merge"):
                line[7] = "merge"
                hist[line[0]] = hist.get(line[0], [])+[(line[1], line[5], line[7], line[8].replace(":", ""))]
            else:
                hist[line[0]] = hist.get(line[0], []) + [(line[1], line[5], line[7])]
            # hist[line[0]] = hist.get(line[0], [])+[(line[1], line[2], line[3], line[5], " ".join(line[7:]))]




if __name__ == "__main__":

    dot = []
    dot.append("digraph G {")

    tree = {}
    for filename in os.listdir(path_commits):
        f = os.path.join(path_commits, filename)

        if os.path.isfile(f):
            createGraph(dot, tree, f)
    for k, v in tree.items():
        for child in v:
            dot.append(f"{k} -> {child[0]};")
        print(k, v)
    print("++++++++++++++")
    preprocessMerges(dot, tree)

    dot.append("}")
    print("\n".join(dot))
    # dot.render(view=True)

# for i in os.listdir("../.git/objects/61"):
#     with open(os.path.join("../.git/objects/61", i), "rb") as f:
#         print(f.readline().decode("utf-8"))
