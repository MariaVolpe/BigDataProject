from pymongo import MongoClient
import loaddata
import querydata
#import 

client = MongoClient()

class Interaction:

    def __init__(self):
        #DB: GeneInformation
        self.db = client.GeneInformation
        #collection: genes
        self.genes = self.db.genes

    def load(self):
        obj = loaddata.LoadData()
        #obj.load_files()
        print("testing mode. feature not allowed")

    def get_stats(self, entrez_id):
        query_obj = querydata.QueryData()
        query_obj.get_all_information(entrez_id)

    def get_associated(entrez_id, n):
        dummy = 0

    def get_patient(patient_id):
        dummy = 0

    def find(dictionary):
        self.genes.find(dictionary)

def main():

    obj = Interaction()

    run = True
    while(run==True):
        print("Enter input:")
        s = input()
        s = s.strip()
        if "quit" in s:
            run = False
        elif "drop" in s:
            print("Please don't delete anything in the database.")
        else:
            s = "obj." + s
            eval(s)
    

if __name__ == "__main__":
    main()
