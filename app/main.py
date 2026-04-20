from fastapi import FastAPI



app = FastAPI()

@app.get('/api/healthchecker')
def check():
    return {'message': 'Hello'}