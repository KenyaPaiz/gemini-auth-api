import os, json, bcrypt
from models.userModel import UserModel
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

class UserService():
    
    def save(user: UserModel):
        # Hash the password
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

        user_data = jsonable_encoder(user)
        # Update the password with the hashed
        user_data['password'] = hashed_password.decode('utf-8')

        file_path = os.path.join("data", "users.json")

        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        data.append(user_data)
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(user))
    