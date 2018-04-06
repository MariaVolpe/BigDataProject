Maria Mahin

Maria Volpe

Project 1

CSCI 49371: Big Data

-----------------------------------
Introduction
-----------------------------------

_AD Knowledge Base_ contains information about patients with dementia and genes associated with dementia, and is comprised of 3 underlying databases: MongoDB, Neo4J, and Redis. Gene information is handled through MongoDB and Neo4J to map their associations, and patient information is handled through Redis.

-----------------------------------
Run Instructions
-----------------------------------
Install dependencies.

Open file ....

Type '''load()''' to begin loading the database. This will take around 40 minutes.

Begin querying.

-----------------------------------
Queries
-----------------------------------

Given an Entrez ID, fine all n-order interacting genes:

'''find\_associated(‘entrez_id’, n)'''


Given an Entrez ID, find mean and standard deviation of gene expression values for AD/MCI/NCI:

'''find\_gene(‘entrez_id’)'''


Given an Entrez ID, find all other information associated with this gene:

'''find\_gene(‘entrez_id’)'''


Given a patient id, find all patient information:

'''find\_patient(‘entrez_id’)'''


Search genes collection using pymongo query syntax:

'''genes.find({‘field’: ‘value‘})'''


EX: 
'''genes.find( { ‘$or’ [ {‘gene\_name’ : ‘LSM5’}, {uniprot\_id : ‘N42L1\_HUMAN’}]})'''


Search patient information using Redis query syntax:


-----------------------------------
Dependencies and Tools
-----------------------------------
Written in Python 3.6 with MongoDB v3.6.3 and PyMongo, Neo4J v3.3.4 and Py2neo, and Redis 4.0.9. 