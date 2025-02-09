from typing import Any
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routes import user
from app.database import Base, engine
from pydantic import ValidationError, errors

# creating tables with database
Base.metadata.create_all(bind=engine)

app: FastAPI = FastAPI(
    title='User Management API',
    description="API para gerenciamento de usuários com validações detalhadas.",
    version='1.1.0'
)


# global error handling Validation
async def validation_exepption_handler(request: Request, exc: ValidationError) -> JSONResponse:
    erros: list[Any] = []
    for error in exc.errors():
        erros.append({
            "loc": error['loc'],
            "msg": error['msg'],
            "type": error["type"]
        })
    return JSONResponse(
        status_code=422,
        content={'detail': errors}
    )

app.include_router(router=user.router, prefix='/users', tags=['users'])


@app.get('/')
def read_root() -> dict[str, str]:
    return {'message': 'welcome to be User Api!'}
