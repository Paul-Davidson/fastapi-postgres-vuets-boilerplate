import asyncpg
import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import hello_world, postgres

app = FastAPI(
    title="fastapi-postgres-vue-boilerplate",
    version="0.0.1",
)

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
    max_age=3600,
)

# Place routers here
app.include_router(hello_world.router)
app.include_router(postgres.router)


async def init_connection(connection):
    await connection.set_type_codec(
        "json", encoder=json.dumps, decoder=json.loads, schema="pg_catalog"
    )


@app.on_event("startup")
async def startup():
    print("event - startup")
    # Handle pool creation
    # https://github.com/jordic/fastapi_asyncpg/blob/master/fastapi_asyncpg/__init__.py
    pool = await asyncpg.create_pool(
        dsn="postgres://{0}:{1}@{2}:5432/{3}".format(
            os.environ['POSTGRES_USER'],
            os.environ['POSTGRES_PASSWORD'],
            os.environ['DB_SERVER'],
            os.environ['POSTGRES_DB']
        ),
        init=init_connection,
    )
    app.state.pool = pool


@app.on_event("shutdown")
async def shutdown():
    print("event - shutdown")
    # Handle pool deletion
    # https://github.com/jordic/fastapi_asyncpg/blob/master/fastapi_asyncpg/__init__.py
    await app.state.pool.close()
