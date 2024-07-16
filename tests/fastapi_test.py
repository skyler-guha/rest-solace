import uvicorn
from fastapi import FastAPI, APIRouter

app = FastAPI()
router = APIRouter()
    

async def read_root():
    return {"Hello": "World"}

# path_function_map = [('/', read_root)]


# for mapping in path_function_map:
#     router.add_api_route(path=mapping[0], endpoint=mapping[1])


# app.include_router(router)

app = FastAPI()

@app.post("/")
async def test():
    
    return {
        "msg": "we got data successfully",
        
    }
 

if __name__ == '__main__':

    try:
        uvicorn.run("fastapi_test:app", host="0.0.0.0", port=5000, log_level="info", workers= 1)

    except KeyboardInterrupt:
        print("Server stopped")


