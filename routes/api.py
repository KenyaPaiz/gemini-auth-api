from fastapi import APIRouter
from services.users import UserService, UserModel
from services.auth import AuthService, Depends
from models.authModel import AuthModel
from gemeni import generate_text, get_chat ,PromptModel

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
async def generate_prompt_kodigo(prompt: PromptModel, user: dict = Depends(AuthService.verify_token)):
    results = await generate_text(prompt, user)
    return results

@api_router.get("/chat/history", dependencies=[Depends(AuthService.verify_token)])
async def get_history_chat(user: dict = Depends(AuthService.verify_token)):
    results = await get_chat(user)
    return results

#test
@api_router.get("/test", dependencies=[Depends(AuthService.verify_token)])
def test():
    return {"message": "Hello World"}