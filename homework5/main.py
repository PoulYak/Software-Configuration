import os
import graphviz


path_commits = "../.git/logs/refs/heads"
print(os.listdir())

def createGraph(graph, path):
    file = open(path, 'r')
    current_branch = os.path.basename(file.name)
    print(file.read())


dot = graphviz.Digraph('Graph')
for filename in os.listdir(path_commits):
    f = os.path.join(path_commits, filename)

    if os.path.isfile(f):
        f = str(f).replace("\\", '/')
        createGraph(dot, f)
        print(f)
    # dot.render(view=True)


# for i in os.listdir("../.git/objects/61"):
#     with open(os.path.join("../.git/objects/61", i), "rb") as f:
#         print(f.readline().decode("utf-8"))
