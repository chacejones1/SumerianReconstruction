import networkx as nx
import matplotlib.pyplot as plt
import processing as rw
from networkx.algorithms import community


def girvan_newman(G,verbose=False):
    """Runs the asynchronous fluid community detection algorithm
       G = Graph to look at
       verbose = whether or not to show steps
    """
    communities_generator = community.girvan_newman(G)
    bestcom=0
    bestq=0

    for next_level_communities in communities_generator: #iterate over dendrograms
        quality = community.performance(G,next_level_communities)
        if quality > bestq:
            bestq = quality
            bestcom = next_level_communities
        if verbose:
            print sorted(map(sorted, next_level_communities)) 
            print ("quality = {}".format(quality))

    if(verbose): 
        print "Best Communities:"
        print sorted(map(sorted, bestcom)) 

    return bestcom

def async_fluid(G, k=4):
    """Runs the asynchronous fluid community detection algorithm
       G = Graph to look at
       k = number of communities to look for, default 4
    """
    bestcom=community.asyn_fluidc(G,k)
    print bestcom
    return bestcom

def opt_async_fluid(G, kmin, kmax,verbose=True,rep=2):
    '''Searches for the best k within the given range
       rep is the number of repetitions to try (may have had bad initialization'''


    bestcom=0
    bestp=0
    bestk=0
    for k in range(0, rep):
        for k in range(kmin,kmax+1):
            com=async_fluid(G,k)
            
            partition=[]
            for c in com: partition.append(c);
            if verbose: print partition;

            p=community.performance(G,partition)
            if p > bestp:
                bestp = p
                bestcom=com
                bestk=k
        
    print "Best K: " + str(bestk)
    print "Best P: " + str(bestp)
        
    return bestcom
 


def test(graph="barbell",algorithm="o_fl",k=-1,v=False,kmin=3,kmax=5):
    """Runs a quic demo
       graph = 'karate', 'barbell', 'women', 'florentine'
         if not a specific graph it will be used as a seed for a random graph
       
       algorithm as
         'fl' = async fluid detection, requires k
         'o_fl' = optimizing fl, requires kmin and kmax
         'gn' = garvin_newman
       
       k = number of communities to look for if applicable
       v = verbose flag
    """
    #generate demo graph
    G=0
    if graph=="karate":
        G=nx.karate_club_graph()
    elif graph=="barbell":
        G=nx.barbell_graph(5,1)
    elif graph=="women":
        G=nx.davis_southern_women_graph()
    elif graph=="florentine":
        G=nx.florentine_families_graph()
    else:
        G=nx.planted_partition_graph(5,10,.85,.1,seed=graph)
    #switch on algorithm
    bestcom=0
    
    if algorithm=="fl":
        if k !=-1:
            bestcom=async_fluid(G, k)
        else:
            bestcom=async_fluid(G)
    elif algorithm=="o_fl": #optimized fl
        bestcom=opt_async_fluid(G,kmin,kmax)
    elif algorithm=="gn":
        bestcom=girvan_newman(G,v)


    #Label the data and export in gephi readable format
    comlabel = 1
    for c in bestcom:
        for n in c:
            G.node[n]['community']=str(comlabel)
        comlabel += 1 
        
    rw.write_file(G,"test.gexf")


if __name__ == "__main__":
    test()
