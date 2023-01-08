import sys
import logging
from pymongo import MongoClient
import pprint
import json
from dotenv import load_dotenv


class Searcher():
   
    client = MongoClient('mongodb+srv://david:zG27NaQ1Fk47Qlbz@clustermongodb.kpcj7of.mongodb.net/test', 27017)

    def __init__(self):
        
        self.db = Searcher.client["antimetal"] # db
        self.collection_instances = self.db["instances"] # collection instances
        self.collection_workloads = self.db["workloads"] # collection workloads
        self.env = load_dotenv()

        logging.basicConfig(stream=sys.stderr,
                            level=logging.os.getenv('PRINT_MODE'))

    def retrieveWorkloads(self):
    
        instances_array_string = []

        result = self.collection_instances.find( { }, { "workloads": 1} )
        for res in result:
            instances_array_string.append( res )

        return str(instances_array_string)