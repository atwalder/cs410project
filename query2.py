import couchdb
#find authors for a paper list
def find(db, papers):
    result = []
    for id in db:
        doc = db.get(id)
        if doc['type'] == "paper" or doc['type'] == "book" or doc['type'] == "msthesis":
            if doc['id'] in papers:
                result+=doc['authors']
    return result

def process(elimate, level):
    result = [x for x in level if x != elimate]
    result = list(set(result))
    return result
    
couchserver = couchdb.Server("http://couchdb:5984/")
dbname = "dblp"
db = couchdb.Database("http://localhost:5984/dblp/")
#looking for papers and got level1
papers = []
elimate = ""
for id in db:
    doc = db.get(id)
    if doc['type'] == "person" and doc['name'] == "Michael Stonebraker":
        papers = doc['author_of']
        elimate = doc['id']
level1 = find(db, papers)
level1 = process(elimate, level1)
#looking for papers within level1 and got level2
papers = []
for id in db:
    doc = db.get(id)
    if doc['type'] == "person" and doc['id'] in level1:
        papers+=doc['author_of']
level2 = find(db, papers)
level2 = process(elimate, level2)
#looking for papers within level2 and got level3
papers = []
for id in db:
    doc = db.get(id)
    if doc['type'] == "person" and doc['id'] in level2:
        papers+=doc['author_of']
level3 = find(db, papers)
level3 = process(elimate, level3)
level3 = level3-level2-level1
print("Michael Stonebraker: ", len(level3), " level 3 co-authors.")


            
    
    
