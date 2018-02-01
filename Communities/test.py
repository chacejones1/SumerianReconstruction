import networkx as nx
import processing as rw
import simplealgs as sa

G = rw.read_nx("GarshanaNameGraph.gexf")

#remove high degree nodes
toremove = []
for n in G.nodes():
    if G.degree(n)>400 or G.degree(n) < 3:
        toremove.append(n)
G.remove_nodes_from(toremove)


#Remove small isolated subgraphs
G = max((G.subgraph(c) for c in nx.connected_components(G)), key=len)


bestcom = sa.opt_async_fluid(G,kmin=10,kmax=15,rep=5)

G = sa.relabel(G,bestcom)

rw.write_file(G,"gexf/NameComsAll.gexf")

