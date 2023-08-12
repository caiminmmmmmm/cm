from sanic import Sanic, response
from pymongo import MongoClient

app = Sanic(__name__)

# MongoDB setup
client = MongoClient('localhost', 27017)
database = client['cm']#cm是数据库
BookRepo = database['book']#book是表，二者都是有就使用，没有就创建，在这里二者可以随便起名字

# Model for Book
class Book:
    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description

#获取全部图书信息
# 1. GET /books
@app.route('/', methods=['GET'])
async def get_books(request):
    books = []
    for book_data in BookRepo.find():
        book = Book(book_data['id'], book_data['title'], book_data['description'])
        books.append(book.__dict__)
        if books:
            return response.json(books)
        else:
            return response.json({'Book is None'})

#获取特定图书信息
# 2. GET /book/id
@app.route('/book/<id>', methods=['GET'])
async def get_book(request, id):
    #print(id)
    book_data = BookRepo.find_one({'id': int(id)})
    #print(book_data)
    # for book_data1 in BookRepo.find():
    #     print(book_data1)
    # for book_data1 in BookRepo.find():
    #     print(book_data1['id'])
    #     print(type(book_data1['id']))
    # 如果找到了图书数据
    if book_data:
        book = Book(book_data['id'], book_data['title'], book_data['description'])
        return response.json(book.__dict__)
    else:
        return response.json({'error': 'Book not found'}, status=404)

#创建图书信息
# 3. POST /book/create
@app.route('/book/create', methods=['POST'])
async def create_book(request):
    data = request.json
    book = Book(data['id'], data['title'], data['description'])
    # book = Book(1,1,1)
    n=BookRepo.insert_one(book.__dict__)
    if n:
        return response.json({'message': 'Book created successfully'}, status=201)
    else:
        return response.json({'message': 'Book created successfully'}, status=404)
#更新图书信息
# 4. PUT /book/update
@app.route('/book/update', methods=['PUT'])
async def update_book(request):
    data = request.json
    book = Book(data['id'], data['title'], data['description'])
    n=BookRepo.update_one({'id': data['id']}, {'$set': book.__dict__})
    if n:
        return response.json({'message': 'Book updated successfully'})
    else:
        return response.json({'message': 'Book updated failed'})
#删除图书信息
# 5. DELETE /book/id
@app.route('/bookup/<id>', methods=['GET'])#DELETE
async def delete_book(request, id):
    n=BookRepo.delete_one({'id': int(id)})
    if n:
        return response.json({'message': 'Book deleted successfully'})
    else:
        return response.json({'message': 'Book deleted failed'})
if __name__ == '__main__':
    app.run(port=8000)
