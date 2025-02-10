from fastapi import FastAPI
from app.routes import user
from app.database import Base, engine

# creating tables with database
Base.metadata.create_all(bind=engine)

app: FastAPI = FastAPI(
    title='User Management API',
    description="API para gerenciamento de usuários com validações detalhadas.",
    version='1.1.0'
)

app.include_router(router=user.router, prefix='/users', tags=['users'])


@app.get('/')
def read_root() -> dict[str, str]:
    return {'message': 'welcome to be User Api!'}
