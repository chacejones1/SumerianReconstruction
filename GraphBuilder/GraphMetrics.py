import json
import progressbar
import sys
import re

def loadData(fName):
    #print "Loading data"
    with open(fName, 'r') as f:
        data = json.load(f)
    return data

def readAttest(data):
    tabs = {}
    names={}
    #print "Reading attestations"
    b = progressbar.ProgressBar()
    for tab in b(data):
        tId = tab['idCDLI']
        for side in tab['sides']:
            for region in side['content']:
                for line in region['lines']:
                    if 'attestations' in line:
                        if tId not in tabs:
                            tabs[tId] = set()
                        for name in line['attestations']:
                            tabs[tId].add(name)
                            if name not in names:
                                names[name] = set()
                            names[name].add(line['text'])
    return tabs, names


def compileNames(tablets):
    names = {}
    #print "Compiling names"
    b = progressbar.ProgressBar()
    for tId in b(tablets):
        for nId in tablets[tId]:
            if nId not in names:
                names[nId] = set()
            if tId not in names[nId]:
                names[nId].add(tId)
    return names


def countEdges(verticies, connections, minDegree=None, maxDegree=None):
    sVert = sorted([i for i in verticies])
    count = 0
    b = progressbar.ProgressBar()
    for id1 in b(sVert):
        linked = set()
        for con in verticies[id1]:
            for id2 in connections[con]:
                if id1 != id2 and id2 not in linked:
                    linked.add(id2)
        degree = len(linked)
        if (minDegree == None or degree >= minDegree) and (maxDegree == None or degree <= maxDegree):
            for other in linked:
                if other > id1:
                    count += 1
    return count

#  type true - tablet, false - name
def countReport(tabs, names, type, minDegree=None, maxDegree=None):
    if type:
        s1 = "Tablet graph"
    else :
        s1 = "Name graph"

    if minDegree == None and maxDegree == None:
        s2 = "all degrees"
    else:
        s2 = "degree"
        if(minDegree != None):
            s2 = "{} <= {}".format(minDegree, s2)
        if(maxDegree != None):
            s2 = "{} <= {}".format(s2, maxDegree)

    print "\nCounting Edges : {}, {}".format(s1, s2)
    if type:
        n = countEdges(tabs, names, minDegree, maxDegree)
    else:
        n = countEdges(names, tabs, minDegree, maxDegree)
    print "{:,} edges found\n".format(n)

def removeBlacklist(tablets, blacklist):
    b = progressbar.ProgressBar()
    names=blacklist.keys()
    emptytabs=[]
    print "Removing blacklisted names"
    for tId in b(tablets):
        badN=[]
        #print tId
        #print tablets[tId]
        for nId in tablets[tId]:
            if (nId in blacklist):
                badN.append(nId)
                
        for n in badN:
            tablets[tId].remove(n)

        if (tablets[tId]=={}):
            emptytabs.append(tId)
    for t in emptytabs:
        tablets.pop(t,None)
    return tablets

def getBlacklist(names, cutoff=40000):
    blacklist={}
    #print "Getting Blacklist"
    for n in names:
        if (len(names[n]) > cutoff or len(names[n]) <0):
            #print(n, "was blacklisted with n=",names[n])
            #print(n)
            blacklist[n] = True
    return blacklist
def long_substr(data):
    substr = ''
    if len(data) > 1 and len(data[0]) > 0:
        for i in range(len(data[0])):
            for j in range(len(data[0])-i+1):
                if j > len(substr) and all(data[0][i:i+j] in x for x in data):
                    substr = data[0][i:i+j]
    return substr
def main(fName):

    data = loadData(fName)
    tabs, fakenames = readAttest(data)
    
    names = compileNames(tabs)
    blacklist = getBlacklist(names,40)
    aCount = sum([len(tabs[k]) for k in tabs])
    badnames={}
    for n in blacklist:
        badnames[n]=set()
        for att in fakenames[n]:
            badnames[n].add(re.sub('[\[\]<>#?!\*]','',att).lower())
        
    
    #for n in badnames:
        #print n+","+long_substr(list(badnames[n]))
    print len(names)
    print len(tabs)
    Umma=['P200331','P200286','P200766','P112135','P362994','P120591','P141735','P120600','P363119','P363032','P363019','P248761','P122570','P101250','P201896','P120926','P200310','P141718']
    PD=['P106217','P201060','P125911','P212046','P106154','P123488','P248907']
    #for tab in Umma:
        #print len(tabs[tab])
    #test='N00000024'
    #for att in badnames[test]:
    #    if 'ad-da' not in att:
    #    print att
    #print test, ":  ",long_substr(list(badnames[test]))
    #print "\n\n{:,} tablets total".format(len(data))
    #print "{:,} total attestations".format(aCount)
    #print "{:,} tablets w/ attestations".format(len(tabs))
    #print "{:,} names in attestations".format(len(names))
    #dpc=float(len(blacklist))/len(names)*100
    #print "{:,} names were blacklisted ({:.2f}%)".format(len(blacklist),dpc)

    
    #tabs = removeBlacklist(tabs, blacklist)
    #names= {k : names[k] for k in set(names)-set(blacklist)}
    #print "{:,} names left".format(len(names))
    #countReport(tabs, names, True)
    #countReport(tabs, names, True, maxDegree = 1000)
    
    #countReport(tabs, names, False)
    #countReport(tabs, names, False, maxDegree = 1000)


if __name__ == "__main__":
    main(sys.argv[1])
