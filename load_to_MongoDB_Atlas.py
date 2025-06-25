import os
import xmltodict
from pymongo import MongoClient

def load_xml_files_as_dicts(xml_folder):
    book_dicts = []

    for filename in os.listdir(xml_folder):
        if filename.endswith(".xml"):
            filepath = os.path.join(xml_folder, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                try:
                    doc = xmltodict.parse(file.read())
                    book_dicts.append(doc['book'])  # Extract <book> node
                except Exception as e:
                    print(f"❌ Failed to parse {filename}: {e}")
    return book_dicts



# --- Update this with your actual MongoDB connection string ---
MONGO_URI = "mongodb+srv://viveksai0707:rrO5FEQylm03WodI@cluster0.gofp0ye.mongodb.net/"  # or your Atlas URI
DB_NAME = "texttech_db"
COLLECTION_NAME = "books"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Load and insert all books
xml_folder = "xml_output"
books = load_xml_files_as_dicts(xml_folder)

# # Optional: clear old entries
# collection.delete_many({})

# Insert books
collection.insert_many(books)
print(f"✅ Inserted {len(books)} book entries into MongoDB collection.")
