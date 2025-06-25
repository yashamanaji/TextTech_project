from pymongo import MongoClient

MONGO_URI = "mongodb+srv://viveksai0707:rrO5FEQylm03WodI@cluster0.gofp0ye.mongodb.net/"  # or your Atlas URI
DB_NAME = "texttech_db"
COLLECTION_NAME = "books"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

#  Find all books with confidence score greater than 0.9
results = collection.find({"confidence": {"$gt": "0.9"}})
for book in results:
    print(f"{book['title']} → {book['genre_predicted']} (Confidence: {book['confidence']})")

#  Find all books predicted as "Fantasy"
results = collection.find({"genre_predicted": "Fantasy"})
for book in results:
    print(book['title'], "→", book['genre_predicted'])

# Books where availability contains "in stock" (case-insensitive)
results = collection.find({"availability": {"$regex": "in stock", "$options": "i"}})
for book in results:
    print(book['title'], "→", book['availability'])

# Top 5 most confident predictions
results = collection.find().sort("confidence", -1).limit(5)
for book in results:
    print(book['title'], book['genre_predicted'], book['confidence'])