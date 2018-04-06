import csv
#import xmljson
from pymongo import MongoClient

client = MongoClient()

class LoadData:

    def __init__(self):
        #name of DB is GeneInformation
        self.db = client.GeneInformation

        #collection: genes
        self.genes = self.db.genes
        #collection: uniprot ids
        self.uniprot = self.db.uniprot
        #collection: gene association
        self.association = self.db.association
        #collection: expression information
        self.expression = self.db.expression

    def load_files(self):
        #Expression Profile
        print("loading genes")
        self.add_to_db('data/entrez_ids_genesymbol.csv', self.genes, "csv")

        #entrez ID uniprot ID
        print("loading uniprot")
        self.add_to_db('data/entrez_ids_uniprot.txt', self.uniprot, "text")

        print("loading gene association")
        #gene association
        self.add_to_db('data/PPI.csv', self.association, "csv")

        print("adding uniprot")
        #add uniprot id to expression profile
        self.add_uniprot_id()

        print("adding associated")
        #add associated genes to expression profile
        self.add_associated_id()

        print("adding expression")
        self.add_to_db('data/ROSMAP_RNASeq_entrez.csv', self.expression, "csv")
    

    def load_xml(self):
        print("adding xml")
        #add associated genes to expression profile
        #self.add_associated_id()


    def test_append(self):
        for entrez_doc in self.genes.find({'entrez_id': '90639'}):
            entrez_doc['uniprot_id'] = []
            for uni_doc in self.uniprot.find({'entrez_id': '90639'}):
                #add the returned values as a list to the fields in expression profile document
                entrez_doc['uniprot_id'].append(uni_doc['uniprot_id'])
            self.genes.save(entrez_doc)

    #add uniprot id to expression profile
    def add_uniprot_id(self):
        #for every item in collection, query the entrez id from uniprot collection
        for entrez_doc in self.genes.find():
            entrez_doc['uniprot_id'] = []
            for uni_doc in self.uniprot.find({'entrez_id': entrez_doc['entrez_id']}):
                #add the returned values as a list to the fields in expression profile document
                entrez_doc['uniprot_id'].append(uni_doc['uniprot_id'])
            self.genes.save(entrez_doc)

    def add_associated_id(self):
        #for every item in collection, query the entrez id from uniprot collection
        for entrez_doc in self.genes.find():
            entrez_doc['associated_genes'] = []
            for uni_doc in self.association.find({'interactor_A': entrez_doc['entrez_id']}):
                #add the returned values as a list to the fields in expression profile document
                entrez_doc['associated_genes'].append(uni_doc['interactor_A'])
            for uni_doc in self.association.find({'interactor_B': entrez_doc['entrez_id']}):
                entrez_doc['associated_genes'].append(uni_doc['interactor_B'])
            self.genes.save(entrez_doc)

    def add_to_db(self, csv_file, collection, type):
        if type == "text":
            data_dicts = self.parse_text(csv_file)
            for i in data_dicts:
                collection.insert(i)
        else:
            data_dicts = self.parse_csv(csv_file)
            for i in data_dicts:
                collection.insert(i)

    #parses csv file and returns a list of dictionaries
    def parse_csv(self, csv_file):
        data = []
        with open(csv_file, 'rt') as cf:
            reader = csv.DictReader(cf)
            for line in reader:
                data.append(line)
        return data

    #parses tab-delimited text file and returns a list of dictionaries
    def parse_text(self, txt_file):
        data = []
        with open(txt_file, 'rt') as tf:
            reader = csv.DictReader(tf, delimiter='\t')
            for line in reader:
                data.append(line)
        return data