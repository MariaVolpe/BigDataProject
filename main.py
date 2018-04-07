from pymongo import MongoClient
import loaddata
import querydata
import 

client = MongoClient()

class Interaction:

    def __init__(self):
        dummy = 0

    def load(self):
        obj = loaddata.LoadData()
        obj.load_files()

    def find_stats(self, entrez_id):
        query_obj = querydata.QueryData()
        query_obj.get_all_information(entrez_id)

    def find_associated(entrez_id, n):
        dummy = 0

    def find_patient(patient_id):
        dummy = 0


def main():

    #DB: GeneInformation
    db = client.GeneInformation
    #collection: genes
    genes = db.genes

    obj = Interaction()
    

    run == True
    while(run==True):
        print("Enter input:")
        s = input()
        if s == "quit":
            run == False
        elif "drop" in s:
            print("Please don't delete anything in the database.")
        elif "load" or "find" in s:
            s = "obj." + s
            eval(s)
        else:
            eval(s)
    

if __name__ == "__main__":
    main()
