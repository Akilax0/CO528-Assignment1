from flask import Flask, request, jsonify, abort, render_template


app = Flask(__name__, static_folder='static')

books = []

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)


@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((book for book in books if book['id'] == book_id),None)
    if book is None:
        abort(404)
    return jsonify(book)
        
@app.route('/books', methods=['POST'])
def add_book():
    if not request.json or not 'title' in request.json:
        abort(400)
    book = {
        'id': books[-1]['id'] + 1 if books else 1,
        'title': request.json['title'],
        'author': request.json.get('author',""),
        'isbn': request.json.get('isbn',"")
    }
    books.append(book)
    return jsonify(book), 201
        
        
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id): 
    book = next((book for book in books if book['id'] == book_id),None)
    print(book)
    if book is None:
        abort(404)
    if not request.json:
        abort(400)

    book['title'] = request.json.get('title',book['title'])    
    book['author'] = request.json.get('author',book['author'])    
    book['isbn'] = request.json.get('isbn',book['isbn'])    
    
    return jsonify(book)

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id): 
    book = next((book for book in books if book['id'] ==  book_id),None)
    if book is None:
        abort(404)
        
    books.remove(book)
    return '',204

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)