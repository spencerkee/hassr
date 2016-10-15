import networkx as nx
import random
import pickle
from copy import deepcopy
import sys
import graphviz as gv

class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()
    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

def has_cycle(graph):
    """Given a networkx graph, return True if it has a cycle and False otherwise"""
    a = len(list(nx.simple_cycles(graph)))
    if a > 0:
        print (nx.simple_cycles(graph))
    return a > 0

def unique_parents(graph,node_list):
    """
    Given a networkx graph and a list of node strings return a list of all unique parents
    of the node strings in node_list
    """
    return_list = []
    for node in node_list:
        return_list = return_list + graph.predecessors(node)
    return list(set(return_list))

def all_successors(graph,node):
    """
    Given a networkx graph and a node string return a list of all successors of the node
    i.e. every node J such that there is a path from the input node to J
    """
    d = nx.dfs_successors(graph,node)
    return_list = []
    for key in d:
        return_list = return_list + d[key]
    return list(set(return_list))

def all_predecessors(graph, node):
    """
    Given a networkx graph and a node string return a list of all predecessors of the node
    i.e. every node J such that there is a path from J to the input node
    """
    lst = graph.predecessors(node)
    return_list = lst
    while len(lst) > 0:
        for node in lst:
            return_list = return_list + graph.predecessors(node)
        lst = unique_parents(graph,lst)
    return list(set(return_list))

def draw(graph,file_path):
    """Converts a networkx graph into a graphviz graph and then creates an svg rendering of the graph"""
    nodes = graph.nodes()
    edges = graph.edges()

    g = gv.Digraph(format='svg')
    for i in nodes:
        g.node(i)
    for i in edges:
        g.edge(i[0],i[1])
    g.render(file_path)

"""ANSI escape sequences"""
class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# def reset_pickle_file(file_path, num_pickled_items):
#     try:
#         open(file_path, 'w').close()
#     except FileNotFoundError:
#         open(file_path, 'a').close()
#     pickle.dump([[] for i in range(num_pickled_items)], open( filename, "wb" ))

def progressive_hassing(all_items, graph_name, load, reset, save, num_items_shown=5,):
    getch = _Getch()
    user_input = getch()
    print (user_input)

def main():
    if len(sys.argv) != 4:
        sys.exit('Usage: ' + sys.argv[0] + ' incorrect number of arguments [load] [reset] [save]')
    for i in range(1,4):
        if sys.argv[i] == 'True':
            sys.argv[i] = True
        elif sys.argv[i] == 'False':
            sys.argv[i] = False
        else:
            sys.exit('Usage: ' + sys.argv[0] + ' improper input [load] [reset] [save]')

    with open('item_list') as f:
        item_content = f.readlines()
        item_content = [x.strip('\n') for x in item_content] 

    progressive_hassing(all_items=item_content,graph_name='movies',
        load=sys.argv[1], reset=sys.argv[2], save=sys.argv[3],
        num_items_shown=5)

if __name__ == '__main__':
    main()