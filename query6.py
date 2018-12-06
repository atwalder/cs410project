##cs410 project
##query for DBLP Connectivity: Is the DBPL graph connected? (That is, is there a path between any two objects?)
##December 5, 2018

import couchdb
import numpy

couchserver = couchdb.Server("http://couchdb:5984/")
dbname = "cs410project"
if dbname in couchserver:
    db = couchserver[dbname]
else:
    db = couchdb.Database("http://localhost:5984/cs410project/")

stringView = "design/viewID"
startNodeName = "Moshe Y. Vardi" #if connected, the node chosen to start is arbitrary
##start_ID = "f3922219d063fe633641cd4b95e2ba54" #Moshe Y. Vardi

mangoQ = {"selector": {
    "$and": [
        {
            "type": {
                "$eq": "person"
            }
        },
        {
            "name": {
                "$eq": startNodeName
            }
        }
    ]
}}
##print(mangoQ)
for row in db.find(mangoQ):
   startID = row['_id']
   startName = row['name']

#print(startID)
#print(startName)
document = db.get(startID)

def retrieveConnections(doc):
    connections = []
    if doc['type'] == 'proceedings' or doc['type'] == 'journal':
        try:
            connections += doc['papers']
        except KeyError:
            return connections
    elif doc['type'] == 'book':
        connections += doc['authors']
        try:
            connections += doc['papers']
        except KeyError:
            return connections
    elif doc['type'] == 'phdthesis' or doc['type'] == 'msthesis':
        connections += doc['authors']
    elif doc['type'] == 'paper':
        try:
            connections += doc['authors']
            connections += doc['in_journal']
            connections += doc['in_proceedings']
            connections += doc['in_collection']
            connections += doc['cites']
        except KeyError:
            try:
                connections += doc['in_journal']
                connections += doc['in_proceedings']
                connections += doc['in_collection']
                connections += doc['cites']
            except KeyError:
                try:
                    connections += doc['in_proceedings']
                    connections += doc['in_collection']
                    connections += doc['cites']
                except KeyError:
                    try:
                        connections += doc['in_collection']
                        connections += doc['cites']
                    except KeyError:
                        try:
                            connections += doc['cites']
                        except KeyError:
                            return connections
    elif doc['type'] == 'person':
        try:
            connections += doc['editor-of']
            connections += doc['in-proceedings']
            connections += doc['author_of']
        except KeyError:
            try:
                connections += doc['in-proceedings']
                connections += doc['author_of']
            except KeyError:
                try:
                    connections += doc['author_of']
                except KeyError:
                    return connections
    return connections 

##def recursiveDepthLimitedSearch(doc, limit, goal, path): 
##    children = retrieveConnections(doc)
##    for child in children:
##        for item in db.view(stringView, key=child):
##            nextDoc = db.get(item.id)
##            if nextDoc['id'] not in path:
##                path.append(nextDoc['id'])
##                recursiveDepthLimitedSearch(nextDoc, limit-1, goal, path)
##    if len(path) == (goal - 1):
##        #print(len(path))
##        return "Connected"
##    else:
##        print(path)
##        print(len(path))
##        return "Disconnected"
##
##def depthLimitedSearch(doc, limit, goal):
##    path = [doc['id']]
##    return recursiveDepthLimitedSearch(doc, limit, goal, path)

def BFS(doc): 
    open_set = []
    open_set.append(doc)
    closed_set = []
    path = [doc['id']]
    level = -1
    while not len(open_set) == 0:
        root = open_set.pop()
        children = retrieveConnections(root)
        for child in children:
            for item in db.view(stringView, key=child):
                nextChild = db.get(item.id)
                if nextChild in closed_set:
                    continue
                if nextChild not in open_set:
                    path.append(nextChild['id'])
                    open_set.append(nextChild)
        closed_set.append(root)
        if len(closed_set) == 1193971:
            print("closed_set: ")
            print(closed_set)
            print("path: ")
            print(path)
            return "Connected"
    print("closed_set: " + str(len(close_set)))
    print("path: " + str(len(path)))
    return "Disconnected"

#print("DFS: ")
#resultDFS = depthLimitedSearch(document, numpy.Inf, 1193972)
#print(result)

print("BFS: Is the DBLP graph data fully connected? ")
connectivity = BFS(document) 
print(connectivity)
