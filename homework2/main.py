from importlib.metadata import requires
import re

def build_dep(depends, all_libs):
    for lib in all_libs:
        try:
            req = requires(lib)
            req = req if req else []
        except:
            req = []
        if lib not in depends:
            depends[lib] = set()
        for addicted_lib in req:
            add_lib = re.findall(r"[\d\w\-_\.]+", addicted_lib.split(";")[0])[0]
            if add_lib not in depends[lib]:
                depends[lib].add(add_lib)
                build_dep(depends, [add_lib])


def do_bfs(res, libname, dep):
    visited = {i:False for i in dep.keys()}
    def bfs(curr_lib):
        visited[curr_lib] = True
        for add_lib in dep[curr_lib]:
            res.append(f'"{curr_lib}" -> "{add_lib}"')
            if not visited[add_lib]:
                bfs(add_lib)

    bfs(libname)

def get_graph(name, deps):
    res = []
    do_bfs(res, name, deps)
    return "digraph G {\n\n"+"\n".join(res)+"\n\n}"


if __name__ == "__main__":

    with open("requirements.txt") as fin:
        lines = fin.readlines()
        libs = [lib.strip().split("==")[0] for lib in lines]

    dependencies = {}
    build_dep(dependencies, libs)
    for i in dependencies:
        dependencies[i] = list(dependencies[i])


    print(sorted(dependencies.keys()))
    print(get_graph(input(), dependencies))