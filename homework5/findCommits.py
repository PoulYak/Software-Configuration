import os

def preprocess_commit(commit_name, filename,tree):
    with open(f"{filename}.txt") as fin:
        was_committer = False
        message = []
        for line in fin.readlines():
            if was_committer and line.strip():
                message.append(line.strip())
            if line.startswith("committer"):
                was_committer = True
            if line.startswith("parent"):
                parent = line.split()[1]
                tree[parent] = tree.get(parent, []) + [commit_name.strip()]

    return "\n".join(message)



def get_important_commits(all_commits, dir=".git/"):
    for branch_name in os.listdir(dir+"logs/refs/heads"):
        file_name = dir+"logs/refs/heads/"+branch_name
        with open (file_name) as fin:
            for line in fin.readlines():
                two_commits = line.split()[:2]
                all_commits.add(two_commits[1])



def get_commit_files(tree, dot, all_commits):
    for i in list(all_commits):
        os.system(f"git cat-file -p  {i} > tempfile.txt")
        dot.append(f'"{i}" [label = "{preprocess_commit(i,"tempfile", tree)}"]')

def add_relationships(tree, dot):
    for parent in tree.keys():
        for child in tree[parent]:
            dot.append(f'"{parent}"->"{child}"')


def main():

    tree = {}
    dot = []
    all_commits = set()
    dot.append("digraph G {")

    get_important_commits(all_commits, "../.git/")
    get_commit_files(tree, dot, all_commits)
    add_relationships(tree, dot)
    dot.append("}")
    print('\n'.join(dot))


if __name__ == "__main__":
    main()



