import networkx as nx
import regex as re
#Written by Chace Jones


''' The purpose of this file is to process networks into different formats
    As well as to read and write files'''

def read_nx(file_name,file_type="gexf"):
    ''' Returns a graph read from a file. 
        By default searches the data directory.
        Default GEXF
        Also Supports: adj_list (al), edge_list (el), GML (gml)'''
    G=0
    file_name=process_directory(file_name)
    
    if file_type=="gexf":
        G=nx.read_gexf(file_name)
    elif file_type=="adj_list" or file_type=="al":
        G=nx.read_adjlist(file_name)
    elif file_type=="edge_list" or file_type=="el":
        G=nx.read_edgelist(file_name)
    elif file_type=="GML" or file_type=="gml":
        G=nx.read_gml(file_name)

    return G

def write_file(G,file_name,file_type="gexf"):
    file_name=process_directory(file_name)
    
    if file_type=="gexf":
        nx.write_gexf(G,file_name)
    elif file_type=="adj_list" or file_type=="al":
        nx.write_adjlist(G,file_name)
    elif file_type=="edge_list" or file_type=="el":
        nx.writeedgelist(G,file_name)
    elif file_type=="GML" or file_type=="gml":
        nx.write_gml(G, file_name)

def process_directory(s,default="data/"):
    ''' If no directory is specified, add the "data/" prefix '''
    default_folder=default
    match = re.search(".*/.*",s)
    if match:
        return s
    else:
        return (default_folder + s)
