import yaml
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from starlette.exceptions import HTTPException as StarletteHTTPException

from lib.config import get_service_path
from lib.exceptions import KBaseAuthException
from lib.utils import get_kbase_config
from model_types import KBaseConfig
from routers import doiorg, works
from routers.doi_forms import root

app = FastAPI(
    docs_url=None,
    redoc_url=None,
)

app.include_router(works.router)
app.include_router(doiorg.router)
app.include_router(root.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({
            'code': 'unprocessable_entity',
            'message': 'This request does not comply with the schema for this endpoint',
            "data": {
                "detail": exc.errors(),
                "body": exc.body
            }
        }),
    )


@app.exception_handler(500)
async def internal_server_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder({
            'code': 'internal_server_error',
            'message': 'An internal server error was detected'
        })
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder({
                'code': 'not_found',
                'message': 'The requested resource was not found',
                'data': {
                    'path': request.url.path
                }
            })
        )
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({
            'code': 'fastapi_exception',

        })
    )


@app.exception_handler(KBaseAuthException)
async def kbase_auth_exception_handler(request: Request, exc: KBaseAuthException):
    return JSONResponse(
        # TODO: this should reflect the nature of the auth error,
        # probably either 401, 403, or 500.
        status_code=401,
        content=jsonable_encoder({
            'code': 'autherror',
            'message': exc.message,
            'data': {
                'upstream_error': exc.upstream_error,
                'exception_string': exc.exception_string
            }
        })
    )


################################
# API
################################


class StatusResponse(BaseModel):
    status: str = Field(...)
    kbase_config: KBaseConfig = Field(...)


@app.get("/status", response_model=StatusResponse)
async def get_status():
    with open(get_kbase_config(), 'r') as kbase_config_file:
        kbase_config = yaml.load(kbase_config_file, yaml.SafeLoader)
        return {"status": "ok", "kbase_config": kbase_config}


#
# Link management
#

# Docs

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(req: Request):
    # root_path = req.scope.get("root_path", "").rstrip("/")

    root_path = get_service_path()
    print('DOCS', root_path, app.openapi_url)
    openapi_url = root_path + app.openapi_url
    return get_swagger_ui_html(
        openapi_url=openapi_url,
        title="API",
    )
