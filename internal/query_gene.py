import csv
import math
from pymongo import MongoClient
from pprint import pprint

client = MongoClient()

class QueryGene:

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
        print("Querying all information for Entrez_ID: {}...".format(gene_id))
        n = self.genes.find({'entrez_id':gene_id})
        return n

    #given an entrez id, find the mean and standard deviation of its expression for AD, MCI, and NCI
    # NCI - 1
    # MCI - 2, 3
    # AD - 4, 5
    def get_stats(self, gene_id):
        print("Calculating stats for Entrez ID: {}...".format(gene_id))
        nci = []
        mci = []
        ad = []
        
        arr = []

        if self.genes.find({'entrez_id':gene_id}).count() !=0:

            for doc in self.expression.find({'DIAGNOSIS':'1'}):
                nci.append(float(doc[gene_id]))

            for doc in self.expression.find({ '$or': [{'DIAGNOSIS':'2'}, {'DIAGNOSIS':'3'}]}):
                mci.append(float(doc[gene_id]))

            for doc in self.expression.find({ '$or': [{'DIAGNOSIS':'4'}, {'DIAGNOSIS':'5'}]}):
                ad.append(float(doc[gene_id]))

            x = self.find_mean(nci)
            arr.append(x)
            arr.append(self.find_standard_deviation(nci, x))

            x = self.find_mean(mci)
            arr.append(x)
            arr.append(self.find_standard_deviation(nci, x))

            x = self.find_mean(ad)
            arr.append(x)
            arr.append(self.find_standard_deviation(nci, x))

        return arr

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