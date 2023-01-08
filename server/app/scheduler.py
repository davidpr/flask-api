import sys
import logging
from pymongo import MongoClient
import pprint
from dotenv import load_dotenv



class Scheduler():
    algorithm = 'first_available'
    client = MongoClient('mongodb+srv://david:zG27NaQ1Fk47Qlbz@clustermongodb.kpcj7of.mongodb.net/test', 27017)


    def __init__(self):
        Scheduler.algorithm = 'first_available'
        
        self.db = Scheduler.client["antimetal"] # db
        self.collection_instances = self.db["instances"] # collection instances
        self.collection_workloads = self.db["workloads"] # collection workloads
        self.env = load_dotenv()
       
        logging.basicConfig(stream=sys.stderr,
                            level=logging.os.getenv('PRINT_MODE'))

    def __repr__(self):
        return f'<Schdeduler {self.algorithm}>'

    def schedule(self, id_petition, ram, workload, runtime, cores, provider):
        logging.debug(str(id_petition)+" "+str(ram)+" "+str(workload)+" "+str(runtime)+" "+str(cores)+" "+str(provider) )
        logging.debug("I am scheduling")

        # just some queries to play
        logging.debug("collections: "+str(self.db.list_collection_names()) )
        logging.debug("collection: "+str(self.collection_instances)+"\n")
        result = self.collection_instances.find_one({"available_ram": 512})
        logging.debug("result1: "+str(result)+"\n")
        result = self.collection_instances.find_one({"available_ram": 1536})
        logging.debug("result2: "+str(result)+"\n")
        # result = self.collection_instances.find_one({"runtimes": runtime})
        # logging.debug("result2b: "+str(result)+"\n")
        # for res in self.collection_instances.find({"available_ram": "1536"}):
        #     logging.debug("result3: "+str(res)+"\n")

        
        if provider is "agnostic":
            logging.debug("agnostic:\n")
            # for result in self.collection_instances.find({"$and": \
            #     [{"available_ram": { "$gte": int(ram) }},\
            #      {"available_cores": { "$gte": int(cores) }} ,\
            #      {"runtimes": runtime }   ]}):

            #     logging.debug("result4: "+str(result)+"\n")

            result = self.collection_instances.find_one({"$and": \
                [{"available_ram": { "$gte": int(ram) }},\
                {"available_cores": { "$gte": int(cores) }} ,\
                {"runtimes": runtime }   ]})

            logging.debug("result4: "+str(result)+"\n")
            
        else: # provider is specified
            logging.debug("non-agnostic:\n")
            # for result in self.collection_instances.find( {"$and": \
            #     [{"available_ram": { "$gte": int(ram) }},\
            #      {"available_cores": { "$gte": int(cores) }} ,\
            #      {"runtimes": runtime }, \
            #      {"provider": provider }  ] }):
                
            #     logging.debug("result4: "+str(result)+"\n")
            result = self.collection_instances.find_one( {"$and": \
                 [{"available_ram": { "$gte": int(ram) }},\
                  {"available_cores": { "$gte": int(cores) }} ,\
                  {"runtimes": runtime }, \
                  {"provider": provider }  ] })

            logging.debug("result4: "+str(result)+"\n")
        
        # if no schedulable instance was found
        if result is None:
            pprint.plogging.debug("workload was not schedulable", sys.stderr)
            return 1

        else:
            
            # INSERT WORKLOAD TO INSTANCE 
            logging.debug("type: "+str(type(result)))
            pprint.plogging.debug(result, sys.stderr)

            # update the instance with the new workload (instances collection)
            result['available_cores'] -= int(cores)
            result['available_ram'] -= int(ram)
            result['workloads'].append(str(id_petition))

            self.collection_instances.find_one_and_update({"_id":result['_id']}, \
            {"$set" : {"available_cores" : result['available_cores'], \
            "available_ram": result['available_ram'], \
            "workloads": result['workloads'] } },\
            upsert = False )
            
            # INSERT WORKLOAD TO WORKLOADS 
            json_workload = {
                    "_id": str(id_petition),
                    "provider": str(provider),
                    "cores": int(cores),
                    "ram": int(ram),
                    "runtime": str(runtime),
                    "workload": str(workload)
                }
            self.collection_workloads.insert_one(json_workload)
            return 0

        # $inc : { "points" : 5 } 
        # atomicity? https://www.mongodb.com/docs/manual/reference/method/db.collection.findOneAndUpdate/
        







   

        