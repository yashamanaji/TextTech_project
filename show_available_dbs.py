from pymongo import MongoClient

uri = "mongodb+srv://viveksai0707:rrO5FEQylm03WodI@cluster0.gofp0ye.mongodb.net/"
client = MongoClient(uri)

# Test DB and collection
db = client.test
print("✅ Connected! DBs:", client.list_database_names())
