import os, json, bcrypt
from fastapi.responses import JSONResponse
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from jose import JWTError, jwt
from dotenv import load_dotenv

load_dotenv()
#oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/login")
security = HTTPBearer()

class AuthService:
    # function to authenticate a user and return a JWT token
    def login(email:str, password:str):
        file_path = os.path.join("data", "users.json")

        # read the file
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []

        # search for the user
        user = next((user for user in data if user["email"] == email), None)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, content="Invalid credentials")
        
        # check the password
        if not bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, content="Invalid credentials")
        
        # create token JWT
        expiration = datetime.utcnow() + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)))
        token = jwt.encode({"sub": user["email"], "exp": expiration}, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))

        return JSONResponse(status_code=status.HTTP_200_OK, content={"access_token": token, "token_type": "bearer"})
    
    # function to verify the JWT token
    def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
        token = credentials.credentials
        try:
            payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
            #return payload
            email = payload.get("sub")
            return {"email": email}
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, content="Invalid token")
