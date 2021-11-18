from fastapi import FastAPI
from .routers import user, auth, server, message
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(server.router)
app.include_router(message.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
