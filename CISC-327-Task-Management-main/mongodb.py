from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://zachkizell87:f9gYzb7e5LKSkQJX@cluster0.eyssqkn.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    mydb = client["mydatabase"]
    x = mydb.count.find({"_id": "UNIQUE COUNT DOCUMENT IDENTIFIER TASKS"})
    print(x[0]["COUNT"])
except Exception as e:
    print(e)