import csv
import pymongo

client = pymongo.MongoClient()

#name of DB is GeneInformation
db = client.GeneInformation

#collection genes
genes = db.genes

#parse gene collection