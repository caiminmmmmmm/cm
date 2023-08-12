from idlelib import query
from pymongo import response
from sanic import Sanic, json
from motor.motor_asyncio import AsyncIOMotorClient

app = Sanic(__name__)

mongodb_uri="mongodb://localhost:27017"
database_name='cm'

class Database:
    def __init__(self,uri,database_name):
        self.client=AsyncIOMotorClient(uri)
        self.db=self.client[database_name]

    async def insert(self,collection_name,document):
        collection=self.db[collection_name]
        await collection.find(query)

    def find(self,collection_name,query=None):
        collection=self.db[collection_name]
        return collection.find(query)

    async def update(self,collection_name,query,update):
        collection =self.db[collection_name]
        await collection.update_many(query,update)

    async def delete(self,collection_name,query):
        collection=self.db[collection_name]
        await collection.delete_many(query)

db_instance=Database(mongodb_uri,database_name)

@app.route("/books",methods=["GET"])
async def get_all_books(request):
    books=db_instance.find('books')
    if books:
        return response.json([book async for book in books])
    else:
        return response.json({'Book is None'})
    #return response.json([book async for book in books])

@app.route("/books/<id:int>",methods=["GET"])
async def get_books(request,id):
    book=await db_instance.find('books',{'_id':id}).to_list(length=None)
    if book:
        return response.json(book)
    else:
        return response.json({'error': 'Book not found'}, status=404)

@app.route("/books/create",methods=["POST"])
async def create_books(request):
    data=request.json
    n=await db_instance.insert('books',data)
    if n:
        return response.json({'message': 'Book created successfully'}, status=201)
    else:
        return response.json({'message': 'Book created successfully'}, status=404)

@app.route("/books/update/<id:int>",methods=["PUT"])
async def update_books(request,id):
    query={'_id':id}
    update={'$set':request.json}
    n=await db_instance.update('books',query,update)
    if n:
        return response.json({'message': 'Book updated successfully'})
    else:
        return response.json({'message': 'Book updated failed'})

@app.route("/books/delete/<id:int>",methods=["DELETE"])
async def delete_books(request,id):
    query={'_id':id}
    n=await db_instance.delete('books',query)
    if n:
        return response.json({'message': 'Book deleted successfully'})
    else:
        return response.json({'message': 'Book deleted failed'})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)