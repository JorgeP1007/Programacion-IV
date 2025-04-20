from flask import Flask, jsonify, request
import redis
import uuid
import json

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
API_URL = "http://localhost:5000"

@app.route('/books', methods=['GET'])
def get_books():
    books = [json.loads(r.get(key)) for key in r.scan_iter("book:*")]
    return jsonify(books), 200

@app.route('/books/<book_id>', methods=['GET'])
def get_book(book_id):
    data = r.get(f"book:{book_id}")
    return (jsonify(json.loads(data)), 200) if data else (jsonify({'error': 'Not found'}), 404)

@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    book_id = str(uuid.uuid4())
    data['id'] = book_id
    r.set(f"book:{book_id}", json.dumps(data))
    return jsonify({'id': book_id}), 201

@app.route('/books/<book_id>', methods=['PUT'])
def update_book(book_id):
    if not r.exists(f"book:{book_id}"):
        return jsonify({'error': 'Not found'}), 404
    data = request.json
    data['id'] = book_id
    r.set(f"book:{book_id}", json.dumps(data))
    return jsonify({'message': 'Updated'}), 200

@app.route('/books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    if not r.exists(f"book:{book_id}"):
        return jsonify({'error': 'Not found'}), 404
    r.delete(f"book:{book_id}")
    return jsonify({'message': 'Deleted'}), 200

if __name__ == '__main__':
    app.run(port=5001)
