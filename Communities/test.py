import networkx as nx
import processing as rw
import simplealgs as sa

G = rw.read_nx("UrTabletGraph.gexf")

#remove high degree nodes
toremove = []
print(nx.number_of_nodes(G))
for n in G.nodes():
    if G.degree(n)>250 or G.degree(n) < 2:
        toremove.append(n)
G.remove_nodes_from(toremove)
del toremove
print("removed high degree")
print(nx.number_of_nodes(G))



#Remove small isolated subgraphs
G = max((G.subgraph(c) for c in nx.connected_components(G)), key=len)

print("removed isolates")
print(nx.number_of_nodes(G))

bestcom = sa.async_fluid(G,k=6)

print("found the communities")

G = sa.relabel(G,bestcom)

print("relabeled, now printing")

rw.write_file(G,"gexf/Ur3Tablets.gexf")

