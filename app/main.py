from fastapi import FastAPI
from app.routes import user
from app.database import Base, engine

# criação das tabelas coom banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router, prefix='/users', tags=['users'])


@app.get('/')
def read_root():
    return {'message': 'welcome to be User Api!'}
