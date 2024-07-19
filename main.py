import uvicorn
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from starlette.staticfiles import StaticFiles
# from router import router
from user import router as router_user
from room import router as router_room
from hotel import router as router_hotel
from rent import router as router_rent

from router import router as router_pages

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(
    title="Hotel Reserving",
    version="0.0.1",
    headers='test'
)


app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(router_user)
app.include_router(router_hotel)
app.include_router(router_room)
app.include_router(router_rent)

app.include_router(router_pages)

uvicorn.run(app, host="0.0.0.0", port=8002)
