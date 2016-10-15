import networkx as nx
import random
import pickle
from copy import deepcopy
import sys
import graphviz as gv
import itertools

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

def reset_pickle_file(file_path, num_pickled_items):
    try:
        open(file_path, 'w').close()
    except FileNotFoundError:
        open(file_path, 'a').close()
    pickle.dump([[] for i in range(num_pickled_items)], open(file_path, "wb" ))

def current_comparisons_minus_skipped(current_item, total_possible_comparisons, skipped_comparisons, verbose=False):
    """
    Given a list of possible comparisons and the current item, return a list of the comparisons with the item
    besides those also in the skipped_comparisons list
    """
    return_list = []
    for node_pair in [i for i in total_possible_comparisons if current_item in i]:
        if not ((node_pair in skipped_comparisons) or [node_pair[1],node_pair[0]] in skipped_comparisons):
            return_list.append(node_pair)
        else:
            if verbose:
                print ('skipping' + str(node_pair))
    return return_list

def remove_relatives(graph, total_possible_comparisons, verbose=False):
    """
    Removes a comparison from total_possible_comparisons if there exists a path between each node
    """

    total_comparisons_copy = list(total_possible_comparisons)
    for pair in total_possible_comparisons:
        if nx.has_path(graph,pair[0],pair[1]):
            total_comparisons_copy.remove(pair)
            if verbose: print ('removing',pair)
            continue
        if nx.has_path(graph,pair[1],pair[0]):
            total_comparisons_copy.remove(pair)
            if verbose: print ('removing',pair)
            continue
    return total_comparisons_copy

def progressive_hassing(all_items, graph_name, load, reset, save, num_items_shown=5):
    assert num_items_shown <= 10

    getch = _Getch()

    if reset:
        print ('===RESETING===')
        load = False
        reset_pickle_file("pickles/" + graph_name + ".p", num_pickled_items=5)
    if load:
        print ('===LOADING===')
        pass
    else:
        print ('===STARING NEW===')
        DG=nx.DiGraph()
        [DG.add_node(i) for i in all_items]
        total_possible_comparisons = [list(pair) for pair in itertools.combinations(all_items, 2)] 
        moves = 0
        skipped_comparisons = []

    remaining_items = list(all_items)
    while len(total_possible_comparisons) > 0:
        print (str(len(total_possible_comparisons)) + ' comparisons left')
        # current_item = random.choice(remaining_items)
        current_item = remaining_items[0]
        current_comparisons = current_comparisons_minus_skipped(current_item,total_possible_comparisons, skipped_comparisons, verbose=True)
        print ("(g)reater than, (l)ess than, (s)kip, (q)uit?")
        mode = 'g'
        while len(current_comparisons) > 0:
            print ("Mode = " + mode)
            for i, j in enumerate(current_comparisons[:num_items_shown]):
                print (i, j)
            user_input = getch()
            if user_input == 'q':
                sys.exit('quit command')
            if user_input in ['g','l','s']:
                mode = user_input
                continue
            try:
                input_index = int(user_input)
                if input_index >= len(current_comparisons) or input_index >= num_items_shown:
                    print ("invalid input: value too high")
                    continue
            except ValueError:
                print ("invalid input: not [g] [l] [s] or convertable to int")
                continue
            if mode == 'g':
                DG.add_edge(current_comparisons[input_index][0],current_comparisons[input_index][1])
            elif mode == 'l':
                DG.add_edge(current_comparisons[input_index][1],current_comparisons[input_index][0])
            elif mode == 's':
                skipped_comparisons.append(current_comparisons[input_index])
            total_possible_comparisons.remove(current_comparisons[input_index])
            total_possible_comparisons = remove_relatives(DG,total_possible_comparisons,verbose=True)
            current_comparisons = current_comparisons_minus_skipped(current_item,total_possible_comparisons, skipped_comparisons, verbose=True)
        remaining_items.remove(current_item)

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