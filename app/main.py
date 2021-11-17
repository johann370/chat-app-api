from fastapi import FastAPI
from .routers import user, auth, server, message

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(server.router)
app.include_router(message.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
