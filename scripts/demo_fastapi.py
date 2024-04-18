# pip install fastapi
# pip install uvicorn (Asynchronous Server Gateway Interface)
# Flask can connect with WSGI-Web Server Gateway Interface
import json
from fastapi import FastAPI, Response
from pydantic import BaseModel
from fastapi.openapi.utils import get_openapi

# uvicorn main:app --reload

# pydantic used for data validation
class MyItem(BaseModel):
    name: str
    price: float
    ready: int=0

app = FastAPI()

@app.get("/")
async def home():
    return "This is Home"

@app.post("/submit")
async def submit(item: MyItem):
    print(json.dumps(item.__dict__, indent=4))
    return "Save success"

# Custom Swagger UI HTML template
# Define your OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Linh Chi API",
        version="2.5.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi