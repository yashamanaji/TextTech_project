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
                    book = doc['book']

                    # 🔧 Clean and convert price
                    raw_price = book.get('price', '').replace('£', '').replace('€', '').strip()
                    try:
                        book['price'] = float(raw_price)
                    except:
                        book['price'] = None  # fallback if conversion fails

                    # (Optional) Convert confidence to float (if needed for filtering)
                    if 'confidence' in book:
                        try:
                            book['confidence'] = float(book['confidence'])
                        except:
                            book['confidence'] = None
                    
                    if 'rating' in book:
                        try:
                            book['rating'] = int(book['rating'])
                        except:
                            book['rating'] = None

                    book_dicts.append(book)
                except Exception as e:
                    print(f"❌ Failed to parse {filename}: {e}")
    return book_dicts


# --- MongoDB connection string ---
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

# Optional: clear old entries
# collection.delete_many({})

# Insert books
collection.insert_many(books)
print(f"✅ Inserted {len(books)} book entries into MongoDB collection.")
