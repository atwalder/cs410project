##Python 3.4.3
##cs410 project
##query for DBLP: At what level is Moshe Vardi from Michael J. Franklin?
##December 5, 2018

import couchdb
import numpy

goalValue = -3
cutoffValue = -2
failureValue = -1

couchserver = couchdb.Server("http://couchdb:5984/")
dbname = "cs410project" #change to the name of the database you want to use
if dbname in couchserver:
    db = couchserver[dbname]
else:
    db = couchdb.Database("http://localhost:5984/" + dbname + "/")

stringView = "design/viewID" #change to view url that emits the attribute 'id' as a key
startNodeName = "Moshe Y. Vardi" #729526 = id, change to person name you want to start with
goalNodeName = "Michael J. Franklin" #747452 = id, change to person name you want to use as a goal
##start_ID = "f3922219d063fe633641cd4b95e2ba54" #Moshe Y. Vardi
##goal_ID = "7eed831a4d055da93f33e9eff8d55916" #Michael J. Franklin
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
if startName == startNodeName:
    document = db.get(startID)

def retrieveConnections(doc):
    connections = []
    if doc['type'] == 'proceedings' or doc['type'] == 'journal':
        connections += doc['papers']
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

def recursiveDepthLimitedSearch(doc, limit, goal, path): 
    cutoffBool = False
    #print(doc['_id'])
    if doc['type'] == 'person' and doc['name'] == goal:
        return goalValue
    elif limit == 0:
        return cutoffValue
    else:
        if cutoffBool == False:
            children = retrieveConnections(doc)
            for child in children:
                for item in db.view(stringView, key=child):
                    nextDoc = db.get(item.id)
                    if nextDoc['id'] not in path:
                        path.append(nextDoc['id'])
                        result = recursiveDepthLimitedSearch(nextDoc, limit-1, goal, path)
                        if result == cutoffValue:
                            cutoffBool = True
                        elif result != failureValue:
                            return result
            if cutoffBool == True:
                return cutoffValue
            else:
                return failureValue

def depthLimitedSearch(doc, limit, goal, path):
    return recursiveDepthLimitedSearch(doc, limit, goal, path)

def iterativeDeepeningSearch(doc, goal):
    for depth in range(7):
        path = []
        print("Depth Level: " + str(depth))
        path.append(doc['id'])
        result = depthLimitedSearch(doc, depth, goal, path)
        print("Solution Path: " + str(path))
        print("Solution Path Length: " + str(len(path)))
        if result != cutoffValue:
            return numpy.floor(depth/2)

authorLevel = iterativeDeepeningSearch(document, goalNodeName)
print("Co-Author distance: At what level is Moshe Vardi from Michael J. Franklin? ")
print("Level: " + str(authorLevel))
