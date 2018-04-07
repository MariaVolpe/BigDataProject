import loaddata
import csv
import math
from pymongo import MongoClient
from pprint import pprint

client = MongoClient()

class QueryData:

    def __init__(self):
        #DB: GeneInformation
        self.db = client.GeneInformation
        #collection: genes
        self.genes = self.db.genes
        #collection: uniprot ids
        self.uniprot = self.db.uniprot
        #collection: gene association
        self.association = self.db.association
        #collection: expression information
        self.expression = self.db.expression

    #given an entrez id, find all other information associated with the gene
    def get_all_information(self, gene_id):
        print("Querying for Entrez_ID: {}...".format(gene_id))
        for entrez_doc in self.genes.find({'entrez_id':gene_id}):
            pprint(entrez_doc)

    #given an entrez id, find the mean and standard deviation of its expression for AD, MCI, and NCI
    # NCI - 1
    # MCI - 2, 3
    # AD - 4, 5
    def get_stats(self, gene_id):
        print("calculating stats for gene_id")
        nci = []
        mci = []
        ad = []
        for doc in self.expression.find({'DIAGNOSIS':'1'}):
            nci.append(float(doc[gene_id]))

        for doc in self.expression.find({ '$or': [{'DIAGNOSIS':'2'}, {'DIAGNOSIS':'3'}]}):
            mci.append(float(doc[gene_id]))

        for doc in self.expression.find({ '$or': [{'DIAGNOSIS':'4'}, {'DIAGNOSIS':'5'}]}):
            ad.append(float(doc[gene_id]))

        x = self.find_mean(nci)
        print("mean of nci: {}".format(x))
        print("std of nci: {}".format( self.find_standard_deviation(nci, x) ))

        x = self.find_mean(mci)
        print("mean of mci: {}".format(x))
        print("std of mci: {}".format( self.find_standard_deviation(mci, x) ))

        x = self.find_mean(ad)
        print("mean of ad: {}".format(x))
        print("std of ad: {}".format( self.find_standard_deviation(ad, x) ))

    #return mean of items in list data
    def find_mean(self, data):
        x = 0
        for i in data:
            x += i

        return ( x/len(data) )

    #return standard deviation of items in list data
    def find_standard_deviation(self, data, mean):
        x = 0
        for i in data:
            n = i - mean
            n *= n
            x += n
        x = x/len(data)
        x = math.sqrt(x)
        return x