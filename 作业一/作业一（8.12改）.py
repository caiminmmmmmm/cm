
from motor.motor_asyncio import AsyncIOMotorClient

class BookDB:
    def __init__(self, uri, database_name):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[database_name]

    async def find_all_books(self):
        collection = self._get_books_collection()
        books = await collection.find().to_list(length=None)
        return [self._serialize_book(book) for book in books]

    async def find_book_by_id(self, book_id):
        collection = self._get_books_collection()
        book = await collection.find_one({'_id': book_id})
        return self._serialize_book(book) if book else None

    async def create_book(self, book_data):
        try:
            collection = self.db['books']
            result = await collection.insert_one(book_data)
            return result.inserted_id
        except Exception as e:
            return response.json({'message': str(e)},status=500)

    async def update_book(self, book_id, book_data):
        try:
            collection = self._get_books_collection()
            result = await collection.update_one({'_id': book_id}, {'$set': book_data})
            return result.modified_count
        except Exception as e:
            return response.json({'message': str(e)},status=500)

    async def delete_book(self, book_id):
        try:
            collection = self._get_books_collection()
            result = await collection.delete_one({'_id': book_id})
            return result.deleted_count
        except Exception as e:
            return response.json({'message': str(e)},status=500)

    def _get_books_collection(self):
        try:
            return self.db['books']
        except Exception as e:
            return response.json({'message': str(e)},status=500)

    def _serialize_book(self, book):
        if book:
            serialized_book = dict(book)
            serialized_book['_id'] = str(serialized_book['_id'])  # 将 ObjectId 转换为字符串
            return serialized_book
        return None




from sanic import Sanic, response
#from book_db import BookDB

app = Sanic(__name__)

mongodb_uri = "mongodb://localhost:27017"
database_name = 'cm'
db_instance = BookDB(mongodb_uri, database_name)

@app.route("/books", methods=["GET"])
async def get_all_books(request):
    try:
        books = await db_instance.find_all_books()
        if books:
            return response.json(books,status=200)
        else:
            return response.json({'message': '书籍为空'},status=404)
    except Exception as e:
        return response.json({"message": "获取书籍失败"}, status=500)

@app.route("/books/<book_id:int>", methods=["GET"])
async def get_books(request, book_id):
    try:
        book = await db_instance.find_book_by_id(book_id)
        if book:
            return response.json(book,status=200)
        else:
            return response.json({'message': '未找到该书籍'}, status=404)
    except Exception as e:
        return response.json({"message": "获取书籍失败"}, status=500)

@app.route("/books/create", methods=["POST"])
async def create_books(request):
    try:
        data = request.json
        inserted_id = await db_instance.create_book(data)
        if inserted_id:
            return response.json({'message': '书籍创建成功', 'inserted_id': inserted_id}, status=201)
        else:
            return response.json({'message': '书籍创建失败'},status=404)
    except Exception as e:
        return response.json({"message": e}, status=500)

@app.route("/books/update/<book_id:int>", methods=["PUT"])
async def update_books(request, book_id):
    try:
        data = request.json
        modified_count = await db_instance.update_book(book_id, data)
        if modified_count:
            return response.json({'message': '书籍更新成功'},status=200)
        else:
            return response.json({'message': '书籍更新失败'},status=404)
    except Exception as e:
        return response.json({"message":e}, status=500)

@app.route("/books/delete/<book_id:int>", methods=["DELETE"])
async def delete_books(request, book_id):
    try:
        deleted_count = await db_instance.delete_book(book_id)
        if deleted_count:
            return response.json({'message': '书籍删除成功'},status=200)
        else:
            return response.json({'message': '书籍删除失败'},status=404)
    except Exception as e:
        return response.json({"message": e}, status=500)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000)


