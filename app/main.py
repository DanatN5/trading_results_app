import yaml
from fastapi import FastAPI
from fastapi.responses import Response

from .router import router

app = FastAPI()

app.include_router(router=router, prefix='/v1')


@app.get('/api/healthchecker')
def check():
    return {'message': 'Hello'}


@app.get('/openapi.yaml', include_in_schema=False)
def openapi_yaml():
    return Response(
        content=yaml.safe_dump(
            app.openapi(),
            sort_keys=False,
            allow_unicode=True),
        media_type='application/yaml',
    )
