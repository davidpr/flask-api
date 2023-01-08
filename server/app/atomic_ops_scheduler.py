import sys
import logging
from pymongo import MongoClient
import pprint
from dotenv import load_dotenv
from bson.objectid import ObjectId



class Atomic_ops_scheduler():

    algorithm = 'first_available'
    client = MongoClient(
        'mongodb+srv://david:@clustermongodb.kpcj7of.mongodb.net/test', 27017)

    def __init__(self):
        Atomic_ops_scheduler.algorithm = 'first_available'

        self.db = Atomic_ops_scheduler.client["antimetal"]  # db
        # collection instances
        self.collection_instances = self.db["instances"]
        # collection workloads
        self.collection_workloads = self.db["workloads"]
        self.env = load_dotenv()

        logging.basicConfig(stream=sys.stderr,
                            level=logging.os.getenv('PRINT_MODE'))

    def __repr__(self):
        return f'<Atomic_ops_scheduler {self.algorithm}>'

    def schedule(self, id_petition, ram, workload, runtime, cores, provider):
        logging.debug(str(id_petition)+" "+str(ram)+" "+str(workload) +
                      " "+str(runtime)+" "+str(cores)+" "+str(provider))
        logging.debug("I am scheduling")
        # just some queries to play
        logging.debug("collections: "+str(self.db.list_collection_names()))
        logging.debug("collection: "+str(self.collection_instances)+"\n")
        result=self.collection_instances.find_one({"available_ram": 512})
        logging.debug("result1: "+str(result)+"\n")
        result=self.collection_instances.find_one({"available_ram": 1536})
        logging.debug("result2: "+str(result)+"\n")
        # result = self.collection_instances.find_one({"runtimes": runtime})
        #  logging.debug("result2b: "+str(result)+"\n")
        # for res in self.collection_instances.find({"available_ram": "1536"}):
        #     logging.debug("result3: "+str(res)+"\n")

        if provider is "agnostic":
            logging.debug("agnostic:\n")

            result=self.collection_instances.find_one_and_update({"$and": \
                [{"available_ram": {"$gte": int(ram)}},\
                {"available_cores": {"$gte": int(cores)}},\
                {"runtimes":  runtime}]},\
                    {"$inc": {"available_cores": -1*int(cores), "available_ram": -1*int(ram)}, \
                     "$addToSet": {"workloads": {"_id": str(id_petition), "cores": int(cores), "ram": int(ram)} }}, \
                        upsert = False)

        else:  # provider is specified
            logging.debug("non-agnostic:\n")
            result=self.collection_instances.find_one_and_update({"$and": \
                [{"available_ram": {"$gte": int(ram)}}, \
                {"available_cores": {"$gte": int(cores)}}, \
                {"runtimes": runtime}, \
                {"provider": provider}]}, \
                    {"$inc": {"available_cores": -1*int(cores), "available_ram": -1*int(ram)}, \
                     "$addToSet": {"workloads": {"_id": str(id_petition), "cores": int(cores), "ram": int(ram)} }}, \
                        upsert = False)

        if result != None:
            logging.debug("result:" + str(result)+"\n")
            # INSERT WORKLOAD TO WORKLOADS
            json_workload={
                    "_id": str(id_petition),
                    "provider": str(provider),
                    "cores": cores,
                    "ram": ram,
                    "runtime": str(runtime),
                    "workload": str(workload)
                }
            self.collection_workloads.insert_one(json_workload)

        # if no schedulable instance was found
        else:
            logging.debug("workload was not schedulable")
            return 1

    def end_workload(self, id_petition):
        logging.debug("id_petition: " +str(id_petition)+"\n")

        result = self.collection_instances.find( \
                { "workloads": {"_id": "6b621442-7bf7-4d04-9ffd-77dd7653bf1a" }})

        for res in result:
            logging.debug("result: " +str(res)+"\n")

        
        result = self.collection_instances.find( { "workloads": { "cores": 1 } } )
        result = self.collection_instances.find( { "workloads.cores": 1 } )


        for res in result:
            logging.debug("result: " +str(res)+"\n")


        # for res in self.collection_instances.find({"available_ram": "1536"}):
        #     logging.debug("result3: "+str(res)+"\n")

        
        result = self.collection_instances.update_one( \
                {"workloads": {"_id": str(id_petition) }}, \
                {"$pull": { "workloads": {"_id": str(id_petition) }}} )
             

        result = self.collection_instances.find_one_and_update( \
                {"workloads.cores": 1 }, \
                {"$pull": { "workloads": {"cores": 1 } }} )
        
        
     
