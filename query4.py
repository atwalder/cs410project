# CS 410/510
# Project Part 4
# Query #4: Which proceedings in 2010 had the most distinct authors across all papers?

import couchdb


def runQuery():
    # Setup from query3 code
    couchserver = couchdb.Server("http://couchdb:5984/")
    dbname = "dblp"
    if dbname in couchserver:
        db = couchserver[dbname]
    else:
        db = couchdb.Database("http://localhost:5984/%s/" % dbname)
    name = findProceedingsWithMaxAuthor(db)
    print 'Proceedings in 2004 with the most authors: %s' % name


def findProceedingsWithMaxAuthor(db):
    # Information about find method from https://couchdb-python.readthedocs.io/en/latest/client.html
    maxAuthors = 0
    proceedingsName = ""
    query = {"selector": {"year": "2004", "type": "proceedings"}, "fields": ["id", "papers", "title"]}
    result = db.find(query)
    for row in result:
        query = {"selector": {"id": {"$in": row['papers']}}, "fields": ["authors"]}
        authorResults = db.find(query)
        proceedingsAuthors = []
        for r in authorResults:
            if r.get('authors'):
                proceedingsAuthors += r['authors']
        proceedingsAuthors = list(set(proceedingsAuthors))
        if len(proceedingsAuthors) > maxAuthors:
            maxAuthors = len(proceedingsAuthors)
            proceedingsName = row['title']
    return proceedingsName


if __name__ == '__main__':
    runQuery()
