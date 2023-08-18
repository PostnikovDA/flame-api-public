from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.mongodb import connect_to_mongo, close_mongo_connection
from app.api.routes import router as api_router

app = FastAPI(docs_url=None)

app.add_event_handler('startup', connect_to_mongo)
app.add_event_handler('shutdown', close_mongo_connection)

origins = [
    "*",
    # "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix='/api')
