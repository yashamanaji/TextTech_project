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
    min_conf = request.args.get('min_conf', '0')
    max_price = request.args.get('max_price', '1000000')
    min_rating = request.args.get('min_rating', '0')

    query = {}

    if genre:
        query['genre_predicted'] = genre

    try:
        min_conf = float(min_conf)
        query['confidence'] = {"$gte": min_conf}
    except:
        pass

    try:
        max_price = float(max_price)
        query['price'] = {"$lte": max_price}
    except:
        pass

    try:
        min_rating = int(min_rating)
        query['rating'] = {"$gte": min_rating}
    except:
        pass

    results = collection.find(query)

    books = []
    for book in results:
        book['_id'] = str(book['_id'])
        books.append(book)
    
    return jsonify(books)

if __name__ == '__main__':
    app.run(debug=True)
