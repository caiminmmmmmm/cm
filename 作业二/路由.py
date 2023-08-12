from sanic import Sanic
from sanic.response import json
from motor.motor_asyncio import AsyncIOMotorClient
from 封装 import UserModel,PermissionModel,DepartmentModel


app = Sanic(__name__)
app.config.DB_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(app.config.DB_URL)
db = client["user_management_db"]
users_collection = db["users"]

user_model = UserModel(users_collection)

@app.route("/users", methods=["GET"])
async def get_users(request):
    users = await user_model.get_users()
    return json(users)

@app.route("/users", methods=["POST"])
async def create_user(request):
    user_data = request.json
    await user_model.create_user(user_data)
    return json({"message": "User created successfully"})

@app.route("/users/<user_id>", methods=["PUT"])
async def update_user(request, user_id):
    user_data = request.json
    await user_model.update_user(user_id, user_data)
    return json({"message": "User updated successfully"})

@app.route("/users/<user_id>", methods=["DELETE"])
async def delete_user(request, user_id):
    await user_model.delete_user(user_id)
    return json({"message": "User deleted successfully"})

db = client["permission_management_db"]
permissions_collection = db["permissions"]

permission_model = PermissionModel(permissions_collection)

@app.route("/permissions", methods=["POST"])
async def create_permission(request):
    permission_data = request.json
    await permission_model.create_permission(permission_data)
    return json({"message": "Permission created successfully"})

@app.route("/permissions/<permission_id>", methods=["PUT"])
async def update_permission(request, permission_id):
    permission_data = request.json
    await permission_model.update_permission(permission_id, permission_data)
    return json({"message": "Permission updated successfully"})

@app.route("/permissions/<permission_id>", methods=["DELETE"])
async def delete_permission(request, permission_id):
    await permission_model.delete_permission(permission_id)
    return json({"message": "Permission deleted successfully"})


db = client["department_management_db"]
departments_collection = db["departments"]

department_model = DepartmentModel(departments_collection)

@app.route("/departments", methods=["POST"])
async def create_department(request):
    department_data = request.json
    await department_model.create_department(department_data)
    return json({"message": "Department created successfully"})

@app.route("/departments/<department_id>", methods=["PUT"])
async def update_department(request, department_id):
    department_data = request.json
    await department_model.update_department(department_id, department_data)
    return json({"message": "Department updated successfully"})

@app.route("/departments/<department_id>", methods=["DELETE"])
async def delete_department(request, department_id):
    await department_model.delete_department(department_id)
    return json({"message": "Department deleted successfully"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
