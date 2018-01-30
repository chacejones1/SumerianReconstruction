import networkx as nx
import processing as rw
import simplealgs as sa

G = rw.read_nx("gexf/GarshanaTabletGraph.gexf")

#remove high degree nodes
toremove = []
for n in G.nodes():
    if G.degree(n)>2000 or G.degree(n) < 3:
        toremove.append(n)
G.remove_nodes_from(toremove)


#Remove small isolated subgraphs
G = max((G.subgraph(c) for c in nx.connected_components(G)), key=len)


bestcom = sa.opt_async_fluid(G,kmin=5,kmax=8,rep=2)

G = sa.relabel(G,bestcom)

rw.write_file(G,"gexf/Tablets.gexf")

