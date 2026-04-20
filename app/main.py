from fastapi import FastAPI
from .router import router



app = FastAPI()

app.include_router(router=router)

@app.get('/api/healthchecker')
def check():
    return {'message': 'Hello'}