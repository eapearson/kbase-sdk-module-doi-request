import yaml
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from starlette.exceptions import HTTPException as StarletteHTTPException

from lib.authclient import KBaseAuthMissingToken
from lib.config import get_service_path
from lib.responses import error_response, exception_error_response
from lib.utils import get_kbase_config
from model_types import KBaseConfig
from routers import doiorg
from routers.doi_forms import root
from routers.doi_requests import doi_requests

app = FastAPI(
    docs_url=None,
    redoc_url=None,
)

app.include_router(doiorg.router)
app.include_router(root.router)
app.include_router(doi_requests.router)


#
# Custom exception handlers.
#

# Have this return JSON in our "standard", or at least uniform, format. We don't
# want users of this api to need to accept FastAPI/Starlette error format.
# These errors are returned when the API is misused; they should not occur in production.
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


#
# It is nice to let these exceptions propagate all the way up by default. There
# are many calls to auth, and catching each one just muddles up the code.
#
@app.exception_handler(KBaseAuthMissingToken)
async def kbase_auth_exception_handler(request: Request, exc: KBaseAuthMissingToken):
    # TODO: this should reflect the nature of the auth error,
    # probably either 401, 403, or 500.
    return exception_error_response('auth_error', 'Error authenticating with KBase', exc,
                                    status_code=401)


#
# This catches good ol' internal server errors. These are primarily due to internal programming
# logic errors. The reason to catch them here is to override the default FastAPI
# error structure.
#
@app.exception_handler(500)
async def internal_server_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder({
            'code': 'internal_server_error',
            'title': 'Internal Server Error',
            'message': 'An internal server error was detected',
            'data': {
                'original_message': str(exc)
            }
        })
    )


#
# Finally there are some other errors thrown by FastAPI which need overriding to return
# a normalized JSON form.
# This should be all of them.
# See: https://fastapi.tiangolo.com/tutorial/handling-errors/
#
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return error_response('not_found', "Not Found HTTP Exception", 'The requested resource was not found',
                              data={
                                  'path': request.url.path
                              },
                              status_code=404)

    return error_response('fastapi_exception', 'Other HTTP Exception', 'Internal FastAPI Exception',
                          data={
                              'detail': exc.detail
                          },
                          status_code=exc.status_code)


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

    openapi_url = root_path + app.openapi_url
    return get_swagger_ui_html(
        openapi_url=openapi_url,
        title="API",
    )
