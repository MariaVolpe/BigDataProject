from pymongo import MongoClient
import loaddata
import querydata

def main():
    client = MongoClient()

    #client.drop_database('GeneInformation')

    obj = loaddata.LoadData()
    #obj.load_files()
    #obj.load_xml()
    #obj.load_expression()

    query_obj = querydata.QueryData()
    #query_obj.get_all_information('2')
    query_obj.get_stats('14')

if __name__ == "__main__":
    main()