from pydantic import BaseModel

class UserModel(BaseModel):
    fullname: str
    email: str
    password: str