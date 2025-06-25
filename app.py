from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  # enable cross-origin requests from frontend

# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://viveksai0707:rrO5FEQylm03WodI@cluster0.gofp0ye.mongodb.net/")
db = client["texttech_db"]
collection = db["books"]

@app.route('/books', methods=['GET'])
def get_books():
    genre = request.args.get('genre')
    min_conf = float(request.args.get('min_conf', 0))
    query = {}

    if genre:
        query['genre_predicted'] = genre
    if min_conf:
        query['confidence'] = {"$gte": str(min_conf)}  # Mongo may store confidence as string

    results = collection.find(query)
    books = []
    for book in results:
        book['_id'] = str(book['_id'])  # Make ObjectId serializable
        books.append(book)
    return jsonify(books)

if __name__ == '__main__':
    app.run(debug=True)
