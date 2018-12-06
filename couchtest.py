#the publication has most co-author
import couchdb
couchserver = couchdb.Server("http://couchdb:5984/")
dbname = "dblp"
db = couchdb.Database("http://localhost:5984/dblp/")
paper = ""
number = 0
temp = {}
for id in db:
    if id != "_design/co-authors":
        doc = db.get(id)
        if doc['type'] == "paper" or doc['type'] == "book" or doc['type'] == "msthesis":
            if len(doc['authors']) >= number:
                number = len(doc['authors'])
                paper = doc['title']
                if number in temp.keys():
                    temp[number].append(paper)
                else:
                    temp[number] = [paper]
resultN = max(temp.keys())
resultP = temp[resultN]
print(resultP, ": ",resultN)
        
