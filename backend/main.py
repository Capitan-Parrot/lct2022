from fastapi import FastAPI
import uvicorn
from priceByCityDistrict import Parser
from backend.routes.index import router

app = FastAPI()
app.include_router(router)


@app.get("/")
async def root():
    print(1)
    return {"message": "Hello World"}

parser = Parser()
parser.start()
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)

