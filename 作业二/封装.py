from motor.motor_asyncio import AsyncIOMotorCollection

class UserModel:
    def __init__(self, db: AsyncIOMotorCollection):
        self.db = db

    async def get_users(self):
        users = await self.db.find().to_list(None)
        return users

    async def create_user(self, user_data):
        await self.db.insert_one(user_data)

    async def update_user(self, user_id, user_data):
        await self.db.update_one({"_id": user_id}, {"$set": user_data})

    async def delete_user(self, user_id):
        await self.db.delete_one({"_id": user_id})

class PermissionModel:
    def __init__(self, db: AsyncIOMotorCollection):
        self.db = db

    async def create_permission(self, permission_data):
        await self.db.insert_one(permission_data)

    async def update_permission(self, permission_id, permission_data):
        await self.db.update_one({"_id": permission_id}, {"$set": permission_data})

    async def delete_permission(self, permission_id):
        await self.db.delete_one({"_id": permission_id})

class DepartmentModel:
    def __init__(self, db: AsyncIOMotorCollection):
        self.db = db

    async def create_department(self, department_data):
        await self.db.insert_one(department_data)

    async def update_department(self, department_id, department_data):
        await self.db.update_one({"_id": department_id}, {"$set": department_data})

    async def delete_department(self, department_id):
        await self.db.delete_one({"_id": department_id})