import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance
import sys
import os
import random
import numpy as np

def solve(G):
    G.remove_edges_from(nx.selfloop_edges(G))
    node = the_node(G)
    if node != G:
        print(node)
        return node
    spt = spt_solution(G)
    mst = mst_solution(G)
    if average_pairwise_distance(spt) < average_pairwise_distance(mst):
        print("spt")
        return spt
    else:
        print("mst")
        return mst

def the_node(G):
    numberOfNodes = G.number_of_nodes()
    nodes = G.nodes()
    for node in nodes:
        if G.degree(node) == numberOfNodes - 1:
            new = nx.Graph()
            new.add_node(node)
            return new
    return G

def spt_solution(G):
    # resultDict = {}
    smallest = [float('inf'), None]
    for starting in G.nodes():
        T = getSPT(G, starting)
        aveDis = average_pairwise_distance(T)
        if smallest[0] > aveDis:
            smallest = [aveDis, T]
    before_pruning = smallest[1]
    no_ramdom = prune_leaf(G, before_pruning)
    random = random_prune(G, before_pruning)
    if average_pairwise_distance(no_ramdom) < average_pairwise_distance(random):
        print("No random spt")
        return no_ramdom
    else:
        print("random spt")
        return random

def getSPT(G, source):
    spt = nx.Graph()
    spt.add_nodes_from(G.nodes())
    paths = nx.single_source_shortest_path(G, source)
    for dest in paths:
        path = paths[dest]
        pathList = convertList(path)
        for edge in pathList:
            if not spt.has_edge(edge[0], edge[1]):
                spt.add_edge(edge[0], edge[1],
                             weight=G[edge[0]][edge[1]]['weight'])
    return spt

def getAvePairwiseDistance(tree):
    vertices = tree.nodes()
    edges = tree.edges()
    tree_cp = nx.Graph()
    tree_cp.add_nodes_from(vertices)
    tree_cp.add_edges_from(edges)

    for vertex in vertices:
        if tree.degree(vertex) == 0:
            tree_cp.remove_node(vertex)
    return average_pairwise_distance(tree_cp)

def convertList(list):
    length = len(list)
    counter = 0
    output = []
    while(counter < length - 1):
        output.append([list[counter], list[counter+1]])
        counter += 1
    return output

def prune_leaf(G, T):
    for _ in range(25):
        leaves = [x for x in T.nodes() if T.degree(x) == 1]
        for i in leaves:
            temp = T.copy()
            temp.remove_node(i)
            try:
                if is_valid_network(G, temp) and average_pairwise_distance(temp) < average_pairwise_distance(T):
                    T = temp
            except:
                continue
    deg_two = [x for x in T.nodes() if T.degree(x) == 2]
    for i in deg_two:
        temp = T.copy()
        temp.remove_node(i)
        try:
            if is_valid_network(G, temp) and average_pairwise_distance(temp) < average_pairwise_distance(T):
                T = temp
        except:
            continue
    return T

def mst_solution(G):
    # check complete graph
    # Minimum Spanning Tree T, our output
    T = nx.Graph()
    T.add_nodes_from(G.nodes(data = True))
    T.add_edges_from(nx.minimum_spanning_edges(G))
    T2 = T.copy()
    # deleting leaves from T
    T = prune_leaf(G, T)
    T2 = random_prune(G, T2)
    # return the min of T and T2
    if average_pairwise_distance(T) < average_pairwise_distance(T2):
        print("no random mst")
        return T
    else:
        print("random mst")
        return T2
"""def random_prune(G, tree):
    min_tree = tree.copy()
    print("random prune", tree.edges())
    result = {}
    for k in range(7000):
        T = tree.copy()

        for j in range(random.randint(1, 1/5*G.number_of_nodes())):
            temp = T.copy()
            tempp = T.copy()
            leaves = [x for x in T.nodes() if T.degree(x) ==
                      1 or T.degree(x) == 2]
            for i in range(random.randint(1, len(leaves))):
                leaves = [x for x in tempp.nodes() if tempp.degree(x) ==
                          1]
                if len(leaves) == 0:
                    break
                select = random.choice(leaves)
                temp = tempp.copy()
                temp.remove_node(select)
                if is_valid_network(G, temp):
                    tempp = temp
            if is_valid_network(G, temp) and average_pairwise_distance(tempp) < average_pairwise_distance(min_tree):
                T = tempp

        if average_pairwise_distance(T) < average_pairwise_distance(min_tree):
            min_tree = T
            print(average_pairwise_distance(min_tree))
    return min_tree"""

def random_prune(G, tree):
    min_tree = tree
    for k in range(1000):
        T = tree.copy()
        """list = range(25)
        random_range = random.choice(list)
        for j in range(70): #ramdom select leaves. if delete and valid, delete it
            temp = T.copy()
            leaves = [x for x in T.nodes() if T.degree(x) == 1 or T.degree(x) == 2]
            if len(leaves) == 0:
                break
            select = random.choice(leaves)
            temp.remove_node(select)
            if is_valid_network(G, temp):
                T = temp"""

        for j in range(30):
            temp = T.copy()
            for i in range(5):
                leaves = [x for x in T.nodes() if T.degree(x) == 1 or T.degree(x) == 2]
                if len(leaves) == 0:
                    break
                select = random.choice(leaves)
                temp = T.copy()
                temp.remove_node(select)
                if is_valid_network(G, temp):
                    T = temp
            if is_valid_network(G, temp) and average_pairwise_distance(temp) < average_pairwise_distance(T):
                T = temp

        if average_pairwise_distance(T) < average_pairwise_distance(min_tree):
            min_tree = T
            print(average_pairwise_distance(min_tree))
    return min_tree

# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
     assert len(sys.argv) == 2
     path = sys.argv[1]
     print(path)
     G = read_input_file(path)
     T = solve(G)
     print(T.nodes())
     assert is_valid_network(G, T)
     print("Average  pairwise distance: {}".format(average_pairwise_distance(T)))
     write_output_file(T, './submission/medium-206.out')

# if __name__ == "__main__":
#     output_dir = "submission"
#     input_dir = "inputs"
#     for input_path in os.listdir(input_dir):
#         graph_name = input_path.split(".")[0]
#         print(graph_name)
#         G = read_input_file(f"{input_dir}/{input_path}")
#         T = solve(G)
#         write_output_file(T, f"{output_dir}/{graph_name}.out")