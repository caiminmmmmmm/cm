from sanic import Sanic, response
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

app = Sanic(__name__)

mongodb_uri = "mongodb://localhost:27017"
database_name = 'cm'

class BookDB:
    def __init__(self, uri, database_name):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[database_name]

    async def find_all_books(self):
        collection = self.db['books']
        books = await collection.find().to_list(length=None)
        serialized_books = []
        for book in books:
            serialized_book = dict(book)
            serialized_book['_id'] = str(serialized_book['_id'])  # Convert ObjectId to string
            serialized_books.append(serialized_book)
        return serialized_books

    async def find_book_by_id(self, book_id):
        collection = self.db['books']
        return await collection.find_one({'_id': book_id})

    async def create_book(self, book_data):
        collection = self.db['books']
        result = await collection.insert_one(book_data)
        return result.inserted_id

    async def update_book(self, book_id, book_data):
        collection = self.db['books']
        result = await collection.update_one({'_id': book_id}, {'$set': book_data})
        return result.modified_count

    async def delete_book(self, book_id):
        collection = self.db['books']
        result = await collection.delete_one({'_id': book_id})
        return result.deleted_count

db_instance = BookDB(mongodb_uri, database_name)

@app.route("/books", methods=["GET"])
async def get_all_books(request):
    books = await db_instance.find_all_books()
    if books:
        return response.json(books)
    else:
        return response.json({'message': '书籍为空'})

@app.route("/books/<book_id:int>", methods=["GET"])
async def get_books(request, book_id):
    book = await db_instance.find_book_by_id(book_id)
    if book:
        return response.json(book)
    else:
        return response.json({'error': '未找到该书籍'}, status=404)

@app.route("/books/create", methods=["POST"])
async def create_books(request):
    data = request.json
    #data={'title':'1','description':'1'}
    inserted_id = await db_instance.create_book(data)
    return response.json({'message': '书籍创建成功', 'inserted_id': str(inserted_id)}, status=201)

@app.route("/books/update/<book_id:int>", methods=["PUT"])
async def update_books(request, book_id):
    data = request.json
    modified_count = await db_instance.update_book(book_id, data)
    if modified_count:
        return response.json({'message': '书籍更新成功'})
    else:
        return response.json({'message': '书籍更新失败'})

@app.route("/books/delete/<book_id:int>", methods=["DELETE"])
async def delete_books(request, book_id):
    deleted_count = await db_instance.delete_book(book_id)
    if deleted_count:
        return response.json({'message': '书籍删除成功'})
    else:
        return response.json({'message': '书籍删除失败'})

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000)
