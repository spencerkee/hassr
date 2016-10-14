import networkx as nx
import random
import pickle
from copy import deepcopy
import sys
import graphviz as gv

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

# def reset_pickle_file(file_path, num_pickled_items):
#     try:
#         open(file_path, 'w').close()
#     except FileNotFoundError:
#         open(file_path, 'a').close()
#     pickle.dump([[] for i in range(num_pickled_items)], open( filename, "wb" ))


