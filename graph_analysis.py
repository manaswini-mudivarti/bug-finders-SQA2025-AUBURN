#!/usr/bin/env python3
import ast, os
from collections import defaultdict
import networkx as nx

def find_py_files(root="."):
    for dp, dn, fn in os.walk(root):
        for f in fn:
            if f.endswith(".py"):
                yield os.path.join(dp, f)

def build_call_graph():
    G = nx.DiGraph()
    defs = {}  # fn_name → filepath

    # 1) collect all function definitions
    for path in find_py_files():
        src = open(path, encoding="utf-8").read()
        tree = ast.parse(src, path)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                fq = f"{os.path.basename(path).replace('.py','')}." + node.name
                defs[fq] = path
                G.add_node(fq)

    # 2) collect calls
    for path in find_py_files():
        src = open(path, encoding="utf-8").read()
        tree = ast.parse(src, path)
        # find calls in each function
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # resolve name
                if isinstance(node.func, ast.Attribute):
                    fn = node.func.attr
                elif isinstance(node.func, ast.Name):
                    fn = node.func.id
                else:
                    continue
                # link caller→callee if both known
                # (we approximate caller as the module name)
                caller = os.path.basename(path).replace(".py","")
                for fq, fpath in defs.items():
                    if fq.endswith(f".{fn}"):
                        G.add_edge(caller + "." + caller, fq)
    return G

def top_n_by_betweenness(G, n=5):
    bc = nx.betweenness_centrality(G)
    # only functions, not modules
    funcs = {k: v for k, v in bc.items() if "." in k}
    return sorted(funcs.items(), key=lambda x: x[1], reverse=True)[:n]

if __name__ == "__main__":
    G = build_call_graph()
    top5 = top_n_by_betweenness(G, 5)
    print("🏆 Top 5 functions to fuzz:")
    for fn, score in top5:
        print(f"  • {fn:<30}  score={score:.4f}")
    # write targets to a file
    with open("fuzz_targets.txt", "w") as o:
        for fn, _ in top5:
            o.write(fn + "\n")
