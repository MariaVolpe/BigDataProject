
import csv
from pymongo import MongoClient
import xml.etree.ElementTree as ET

client = MongoClient()

class LoadGene:

    loaded = False

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

        if len( self.db.collection_names() ) != 0:
            self.loaded = True

    #load all files into database
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

        #expression of genes
        print("loading gene expression")
        self.add_to_db('data/ROSMAP_RNASeq_entrez.csv', self.expression, "csv")

        #xml file information
        print("adding xml")
        self.add_xml('data/uniprot-human.xml')

        print("adding uniprot")
        #add uniprot id to genes collection documents
        self.add_uniprot_id()

        print("adding associated")
        #add associated genes to genes collection documents
        self.add_associated_id()
    

    #add uniprot id to genes collection documents
    def add_uniprot_id(self):
        #for every item in collection, query the entrez id from uniprot collection
        for entrez_doc in self.genes.find():
            entrez_doc['uniprot_id'] = []
            for uni_doc in self.uniprot.find({'entrez_id': entrez_doc['entrez_id']}):
                #add the returned values as a list to the fields in expression profile document
                entrez_doc['uniprot_id'].append(uni_doc['uniprot_id'])
            self.genes.save(entrez_doc)


    #add associated genes to genes collection documents
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

    #adds dictionary returned from parsing the file to the specified collection
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

    #parses xml file and adds it to collection xml
    def add_xml(self, xmlfile):
        tree = ET.parse(xmlfile)
        root = tree.getroot()
        items = []
        for item in root.iter():
            itemdict = {}
            for child in item:
                itemdict[child.tag] = child.text
            items.append(itemdict)
        fields = ['accession', 'name', 'fullName', 'alt-fullName', 'gene-primary','gene-synonym', 'organism-sci', 'organism-common',
        'lineage', 'title', 'authorList', 'source']
        new_file = 'data/xmltocsv.csv'
        with open(new_file, 'w') as cf:
            writer = csv.DictWriter(cf, fieldnames = fields)
            writer.writeheader()
            writer.writerows(items)

        add_to_db(new_file, self.xml, 'csv') 
