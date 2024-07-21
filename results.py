import networkx as nx
import main
import matplotlib.pyplot as plt

Network_A = []
Network_B = []
G = nx.Graph()

for i in range(1, 7):
    Network_A.append('A' + str(i))
    Network_B.append('B' + str(i))

# Intra-edge allocation
G.add_edges_from([('A1', 'A2'), ('A1', 'A3'), ('A2', 'A4'), ('A4', 'A5'), ('A4', 'A6'), ('A5', 'A6'),
                  ('B1', 'B2'), ('B1', 'B3'), ('B2', 'B3'), ('B3', 'B4'), ('B3', 'B6'), ('B4', 'B5')])

Case1 = G.copy()
Case2 = G.copy()

# Inter-edge allocation
Case1.add_edges_from([('A1', 'B1'), ('A1', 'B2'), ('A2', 'B2'), ('A2', 'B3'), ('A3', 'B3'), ('A3', 'B4'), ('A4', 'B4'),
                      ('A4', 'B5'), ('A5', 'B5'), ('A6', 'B6'), ('A6', 'B6'), ('A6', 'B1')])

# Inter-edge allocation
Case2.add_edges_from([('A1', 'B1'), ('A2', 'B1'), ('A2', 'B2'), ('A3', 'B3'), ('A3', 'B4'), ('A3', 'B5'), ('A4', 'B4'),
                      ('A5', 'B4'), ('A5', 'B5'), ('A6', 'B1'), ('A6', 'B2'), ('A6', 'B6')])

Case3 = nx.DiGraph()

# Intra-edge allocation
Case3.add_edges_from([('A1', 'A2'), ('A1', 'A3'), ('A2', 'A4'), ('A4', 'A5'), ('A4', 'A6'), ('A5', 'A6'),
                      ('B1', 'B2'), ('B1', 'B3'), ('B2', 'B3'), ('B3', 'B4'), ('B3', 'B6'), ('B4', 'B5'),
                      ('A2', 'A1'), ('A3', 'A1'), ('A4', 'A2'), ('A5', 'A4'), ('A6', 'A4'), ('A6', 'A5'),
                      ('B2', 'B1'), ('B3', 'B1'), ('B3', 'B2'), ('B4', 'B3'), ('B6', 'B3'), ('B5', 'B4')])

# Inter-edge allocation
Case3.add_edges_from([('A1', 'B1'), ('B1', 'A5'), ('B2', 'A3'), ('B3', 'A3'), ('A3', 'B1'), ('B5', 'A3'), ('B4', 'A4'),
                      ('B4', 'A5'), ('A5', 'B2'), ('B1', 'A6'), ('B2', 'A6'), ('A6', 'B6'), ('A4', 'B1')])

V = len(Network_A) + len(Network_B)
k_reliability_case1 = []
k_reliability_case2 = []
k_reliability_case3 = []
x = []

for i in range(1, V + 1):
    x.append(i)
    k_reliability_case1.append(main.k_reliability(Case1, Network_A, Network_B, i, 0.9))
    k_reliability_case2.append(main.k_reliability(Case2, Network_A, Network_B, i, 0.9))
    k_reliability_case3.append(main.k_reliability(Case3, Network_A, Network_B, i, 0.9))

print(k_reliability_case1)
print(k_reliability_case2)
print(k_reliability_case3)

plt.plot(x, k_reliability_case1, label="Strategy1")
plt.plot(x, k_reliability_case2, label="Strategy2")
plt.plot(x, k_reliability_case3, label="Strategy3")

plt.xlabel('k')
plt.ylabel('k-reliability')
plt.title('Simulation')

plt.legend()
plt.show()
