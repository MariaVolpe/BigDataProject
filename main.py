# from pymongo import MongoClient
# import loaddata
# import querydata
import query_patient
import query_gene
import query_norder

#client = MongoClient()

class Interaction:

    def __init__(self):
        #DB: GeneInformation
        #self.db = client.GeneInformation
        #collection: genes
        #self.genes = self.db.genes

    def load(self):
        obj = loaddata.LoadData()
        #obj.load_files()
        print("testing mode. feature not allowed")

    def get_stats(self, entrez_id):
        query_obj = querydata.QueryData()
        query_obj.get_stats(entrez_id)

    def get_all(self, entrez_id):
        query_obj = querydata.QueryData()
        query_obj.get_all_information(entrez_id)

    def get_associated(self, entrez_id, n):
        dummy = 0

    def get_patient(self, patient_id):
        dummy = 0

    def find(self, dictionary):
        #self.genes.find(dictionary)
        dummy = 0

def main():

    obj = Interaction()

    projectInfo = """
    CSCI 49369 - Big Data Project I
    Creators: Maria Volpe and Maria Mahin
    Project Description:
    This project provides a python command-line interface for database
    creation and query pertaining to the genomics data of Alzheimer's Disease
    """
    print(projectInfo)

    selectionMenu = """
    Please select from one of the following options:
    A. Given an entrez id, find all of its n-order interacting genes
    B. Given an entrez id, find mean and std of gene expression values for AD/MCI/NCI, respectively
    C. Given an entrez id, find all other information associated with this gene
    D. Given a patient id, find all patient information (age, gender, education etc.)
    E. Query from the gene collection
    F. Exit program
    """
    print(selectionMenu)

    selectedOption = "A"

    while selectedOption != 'F':
        selectedOption = input("Select an option: ")
        if selectedOption == 'A':
            # query = query_norder.QueryNOrder()
            # query.promptUser()
            dummy = 0

        elif selectedOption == 'B':
            s = input("Entrez ID: ")
            obj.get_stats(s)

        elif selectedOption == 'C':
            s = input("Entrez ID: ")
            obj.get_all(s)

        elif selectedOption == 'D':
            # query = query_patient.QueryPatient()
            # query.promptUser()
            dummy = 0

        elif selectedOption == 'E':
            s = input("Field to search: ")
            s = s.strip()
            z = input("Value in field: ")
            z = z.strip()
            d = {s:z}
            obj.find(d)

        elif selectedOption == 'F':
            break
        else:
            selectedOption = input("Input Error: Please enter a letter from A-F")



if __name__ == "__main__":
    main()
