from sanic import Sanic
from sanic.response import json
from motor.motor_asyncio import AsyncIOMotorClient
from model import UserModel, PermissionModel, DepartmentModel

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
    try:
        user_data = request.json
        if user_data:
            await user_model.create_user(user_data)
            return json({"message": "User created successfully"}, status=200)
        else:
            return json({"message": "User created failed"}, status=404)
    except Exception as e:
        return json({"message": "User created failed"}, status=500)


@app.route("/users/<user_id>", methods=["PUT"])
async def update_user(request, user_id):
    try:
        user_data = request.json
        if user_data:
            await user_model.update_user(user_id, user_data)
            return json({"message": "User updated successfully"}, status=200)
        else:
            return json({"message": "User updated failed"}, status=404)
    except Exception as e:
        return json({"message": "User updated failed"}, status=500)


@app.route("/users/<user_id>", methods=["DELETE"])
async def delete_user(request, user_id):
    try:
        if user_id:
            await user_model.delete_user(user_id)
            return json({"message": "User deleted successfully"},status=200)
        else:
            return json({"message": "User deleted failed"}, status=404)
    except Exception as e:
        return json({"message": "User deleted failed"}, status=500)


db = client["permission_management_db"]
permissions_collection = db["permissions"]

permission_model = PermissionModel(permissions_collection)


@app.route("/permissions", methods=["POST"])
async def create_permission(request):
    try:
        permission_data = request.json
        if permission_data:
            await permission_model.create_permission(permission_data)
            return json({"message": "Permission created successfully"},status=200)
        else:
            return json({"message": "Permission created failed"}, status=404)
    except Exception as e:
        return json({"message": "User created failed"}, status=500)


@app.route("/permissions/<permission_id>", methods=["PUT"])
async def update_permission(request, permission_id):
    try:
        permission_data = request.json
        if permission_data:
            await permission_model.update_permission(permission_id, permission_data)
            return json({"message": "Permission updated successfully"}, status=200)
        else:
            return json({"message": "Permission updated failed"}, status=400)
    except Exception as e:
        return json({"message": "Permission updated failed"}, status=500)

@app.route("/permissions/<permission_id>", methods=["DELETE"])
async def delete_permission(request, permission_id):
    try:
        await permission_model.delete_permission(permission_id)
        return json({"message": "Permission deleted successfully"}, status=200)
    except Exception as e:
        return json({"message": "Permission deleted failed"}, status=500)

db = client["department_management_db"]
departments_collection = db["departments"]

department_model = DepartmentModel(departments_collection)

@app.route("/departments", methods=["POST"])
async def create_department(request):
    try:
        department_data = request.json
        if department_data:
            await department_model.create_department(department_data)
            return json({"message": "Department created successfully"}, status=200)
        else:
            return json({"message": "Department created failed"}, status=400)
    except Exception as e:
        return json({"message": "Department created failed"}, status=500)

@app.route("/departments/<department_id>", methods=["PUT"])
async def update_department(request, department_id):
    try:
        department_data = request.json
        if department_data:
            await department_model.update_department(department_id, department_data)
            return json({"message": "Department updated successfully"}, status=200)
        else:
            return json({"message": "Department updated failed"}, status=400)
    except Exception as e:
        return json({"message": "Department updated failed"}, status=500)

@app.route("/departments/<department_id>", methods=["DELETE"])
async def delete_department(request, department_id):
    try:
        await department_model.delete_department(department_id)
        return json({"message": "Department deleted successfully"}, status=200)
    except Exception as e:
        return json({"message": "Department deleted failed"}, status=500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
