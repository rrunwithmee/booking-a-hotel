import uvicorn
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

# from router import router
from user import router as router_user
from room import router as router_room


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(
    title="Hotel Reserving",
    version="0.0.1",
    headers='test'
)

app.include_router(router_user)
app.include_router(router_room)

uvicorn.run(app, port=8001)