from pymongo import MongoClient



try:
    mongo = MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS=1000
    )
    db = mongo.employeeManagement
    mongo.server_info()  # trigger exception if not connected to mongo db

except:
    print("ERROR CONNECTING TO MONGO DB")
