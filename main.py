from fastapi import FastAPI, Request
from uvicorn import run
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.exc import SQLAlchemyError
import starlette.status as status
from src.api.routers import search, account, query
from src.config import get_config

config = get_config()
app = FastAPI()
for router in [search.router, account.router, query.router]:
    app.include_router(router)


@app.get('/')
async def root():
    return RedirectResponse(url='/docs', status_code=status.HTTP_302_FOUND)


@app.exception_handler(SQLAlchemyError)
async def hand_db_exceptions(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=400,
        content={'detail': str(exc)},
    )


if __name__ == '__main__':
    try:
        run(
            'main:app',
            host=config.fastapi.host,
            port=config.fastapi.port,
            reload=True,
        )
    except (KeyboardInterrupt, SystemExit):
        pass
