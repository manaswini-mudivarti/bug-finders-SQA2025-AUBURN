#!/usr/bin/env python3
import ast, os
import networkx as nx

# Directories to skip entirely
SKIP_DIRS = {'env', '.venv', 'venv', '__pycache__', '.git'}

def find_py_files(root="."):
    for dirpath, dirnames, filenames in os.walk(root):
        # prune unwanted dirs
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fname in filenames:
            if fname.endswith(".py"):
                yield os.path.join(dirpath, fname)

def build_call_graph(root="."):
    G = nx.DiGraph()
    defs = {}  # fullname → filepath

    # 1) Collect function definitions
    for path in find_py_files(root):
        try:
            src = open(path, encoding="utf-8").read()
            tree = ast.parse(src, path)
        except (SyntaxError, UnicodeDecodeError):
            continue

        module = os.path.relpath(path, root).replace(os.sep, ".")[:-3]  # strip .py
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                fq = f"{module}.{node.name}"
                defs[fq] = path
                G.add_node(fq)

    # 2) Collect calls (caller→callee)
    for path in find_py_files(root):
        try:
            src = open(path, encoding="utf-8").read()
            tree = ast.parse(src, path)
        except (SyntaxError, UnicodeDecodeError):
            continue

        caller_mod = os.path.relpath(path, root).replace(os.sep, ".")[:-3]
        caller_node = f"{caller_mod}.{caller_mod}"
        G.add_node(caller_node)

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # extract simple name
                if isinstance(node.func, ast.Attribute):
                    fn = node.func.attr
                elif isinstance(node.func, ast.Name):
                    fn = node.func.id
                else:
                    continue

                # link to any matching def
                for fq in defs:
                    if fq.endswith(f".{fn}"):
                        G.add_edge(caller_node, fq)

    return G

def top_n_by_betweenness(G, n=5):
    bc = nx.betweenness_centrality(G)
    # filter just the functions (i.e. nodes with a dot)
    funcs = {k: v for k, v in bc.items() if "." in k}
    return sorted(funcs.items(), key=lambda x: x[1], reverse=True)[:n]

if __name__ == "__main__":
    G = build_call_graph()
    top5 = top_n_by_betweenness(G, 5)
    print("🏆 Top 5 functions to fuzz:")
    for fn, score in top5:
        print(f"  • {fn:<30}  score={score:.4f}")
    with open("fuzz_targets.txt", "w") as o:
        for fn, _ in top5:
            o.write(fn + "\n")
