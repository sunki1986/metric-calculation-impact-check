from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# 1. Define your logic class
class Processor:
    def __init__(self, multiplier: int = 2):
        self.multiplier = multiplier

    def process_data(self, value: int) -> int:
        return value * self.multiplier

# 2. Initialize the app and the class
app = FastAPI()
logic = Processor(multiplier=10)

class CalcRequest(BaseModel):
    value: int

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI + uv!"}

# 3. Call the class method inside the endpoint
@app.post("/calculate")
def calculate(data: CalcRequest):
    result = logic.process_data(data.value)
    return {"input": data.value, "result": result}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


