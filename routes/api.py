from fastapi import APIRouter
from services.users import UserService, UserModel
from services.auth import AuthService, Depends
from models.authModel import AuthModel
from gemeni import generate_text, PromptModel

api_router = APIRouter(
    prefix="/api/v1"
)

@api_router.post("/users")
def create_user(user: UserModel):
    return UserService.save(user)

@api_router.post("/login")
def auth_user(credentials: AuthModel):
    return AuthService.login(credentials.email, credentials.password)

@api_router.post("/kodigo-query", dependencies=[Depends(AuthService.verify_token)])
async def generate_prompt_kodigo(prompt: PromptModel):
    results = await generate_text(prompt)
    return results

#test
@api_router.get("/test", dependencies=[Depends(AuthService.verify_token)])
def test():
    return {"message": "Hello World"}