import networkx as nx
import processing as rw
import random as rng

G = rw.read_nx("gexf/cdliNames6lt500.gexf")

rate=1-.2
count=nx.number_of_nodes(G)
print count
remcount=int(rate*count)
print count-remcount
torem=rng.sample(set(G.nodes()), remcount)
G.remove_nodes_from(torem)

rw.write_file(G,"gexf/cdliNamesSub10.gexf")

