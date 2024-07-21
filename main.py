import itertools
import networkx as nx
import matplotlib.pyplot as plt
from tabulate import tabulate as tb


def parser(a_list):
    flat_list = []
    for subset in a_list:
        for item in subset:
            if item not in flat_list:
                flat_list.append(item)

    if not not flat_list:
        flat_list.pop(0)
    return flat_list


def node_is_not_functioning(neighbors_list, network_A, network_B):
    belongs_to_A = 0
    belongs_to_B = 0

    if not neighbors_list:
        return True

    for node in neighbors_list:
        if node in network_A:
            belongs_to_A += 1
        elif node in network_B:
            belongs_to_B += 1

    if belongs_to_A > 0 and belongs_to_B > 0:
        return False

    return True


def remove_from_networks(node, network_A, network_B):
    if node in network_A:
        network_A.remove(node)
    else:
        network_B.remove(node)


def subgraph_is_functioning(G, a_set, network_A, network_B):
    belongs_to_A = 0
    belongs_to_B = 0
    H = G.copy()
    difference = list(set(H.nodes) - set(a_set))
    H.remove_nodes_from(nodes=difference)

    for node in a_set:
        new_list = parser(H.edges(node))
        if node_is_not_functioning(new_list, network_A, network_B):
            return False
        else:
            if node in network_A:
                belongs_to_A += 1
            elif node in network_B:
                belongs_to_B += 1

    if belongs_to_A > 0 and belongs_to_B > 0:
        return True

    return False


def number_of_subgraph(G, node_numbers):
    counter = 0
    for sub_node in itertools.combinations(G.nodes(), node_numbers):
        subgraph = G.subgraph(sub_node)
        if nx.is_connected(subgraph):
            counter += 1

    return counter


def create_table(subgraph_list):
    temp_list = ["k"]
    new_list = []

    for i in range(1, len(subgraph_list[0]) + 1):
        temp_list.append(i)
    new_list.append(temp_list)

    i = 1
    for subgraph in subgraph_list:
        subgraph.insert(0, "G" + str(i))
        i += 1

    for i in subgraph_list:
        new_list.append(i)

    print(tb(new_list, tablefmt="fancy_grid"))


def generate_graph(v1, v2, edges):
    Network_A = []
    Network_B = []
    G = nx.Graph()

    for i in range(1, v1 + 1):
        # G.add_node('A' + str(i))
        Network_A.append('A' + str(i))

    for j in range(1, v2 + 1):
        # G.add_node('B' + str(j))
        Network_B.append('B' + str(j))

    G.add_edges_from(edges)

    nx.draw(G, with_labels=True)
    plt.show()
    return G, Network_A, Network_B


def find_steady_state(G, network_A, network_B, attack_locations):
    subgraph_list = []
    temp_list = []
    node_numbers = len(G.nodes())
    for i in range(1, node_numbers + 1):
        temp_list.append(number_of_subgraph(G, i))
    subgraph_list.append(temp_list)
    temp_list = []

    for node in attack_locations:
        G.remove_node(node)
        remove_from_networks(node, network_A, network_B)

    nx.draw(G, with_labels=True)
    plt.show()

    while True:
        for i in range(1, node_numbers + 1):
            temp_list.append(number_of_subgraph(G, i))
        subgraph_list.append(temp_list)
        temp_list = []

        removal_list = []
        for node in G:
            neighbors_list = parser(G.edges(node))
            if node_is_not_functioning(neighbors_list, network_A, network_B):
                removal_list.append(node)

        if not removal_list:
            break

        for item in removal_list:
            G.remove_node(item)
            remove_from_networks(item, network_A, network_B)

        nx.draw(G, with_labels=True)
        plt.show()

    surviving_nodes = len(G.nodes)

    return G, network_A, network_B, surviving_nodes, subgraph_list


def k_reliability(G, network_A, network_B, k, p):
    V = len(network_A) + len(network_B)
    R = 0
    r = k
    S = []

    while r <= V:
        all_subgraph = list(itertools.combinations(G.nodes(), r))

        for i in range(0, len(all_subgraph)):
            if subgraph_is_functioning(G, all_subgraph[i], network_A, network_B):
                S.append(all_subgraph[i])

        # print(S)
        # print(len(S))
        Sr = len(S)
        R += Sr * (p ** r) * ((1 - p) ** (V - r))
        r += 1
        S = []

    return R


def cfr(G, network_A, network_B, attack_locations, p, k, R0):
    G, network_A, network_B, surviving_nodes, subgraph_list = find_steady_state(G, network_A, network_B,
                                                                                attack_locations)
    Rk = 0
    if surviving_nodes < k:
        CFR = 1
        return CFR, surviving_nodes, subgraph_list, Rk
    else:
        Rk = k_reliability(G, network_A, network_B, k, p)
        if Rk < R0:
            CFR = 1
        else:
            CFR = 0

    return CFR, surviving_nodes, subgraph_list, Rk


def main():
    v1 = int(input("Network A nodes count: "))
    v2 = int(input("Network B nodes count: "))
    edges = input("Edges: ( format :: A1 B1, A2 B2 ) ")
    edges = [tuple(str(i) for i in x.split()) for x in edges.split(',')]
    attack_locations = input("Attack Locations: ( format :: A1, B1 ) ")
    attack_locations = attack_locations.split(', ')
    p = float(input("Node reliability: "))
    k = int(input("k: "))
    R0 = float(input("R0: "))

    G, network_A, network_B = generate_graph(v1, v2, edges)
    CFR, surviving_nodes, subgraph_list, Rk = cfr(G, network_A, network_B, attack_locations, p, k, R0)

    print()
    print("Number of subgraphs induced from different node numbers:")
    create_table(subgraph_list)
    print()
    print("Number of surviving nodes: " + str(surviving_nodes))
    print("k-reliability: " + str(Rk))
    if CFR == 1:
        print("CFR: Yes")
    else:
        print("CFR: No")


if __name__ == '__main__':
    main()
