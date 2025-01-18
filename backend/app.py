
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from refresh import refreshPromData
from model import buildModel
from keplerbot import generate_response
import uvicorn

# Create an instance of the FastAPI class
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

metrics = refreshPromData()
predictive_model, predictions= buildModel(metrics)

@app.get('/hello')
def hello():
    return {"message": "Hi there, if you are just here to test, this works great. cheers! :) "}

# Define the message model
class ChatMessage(BaseModel):
    message: str

# Define the route for chat interaction
@app.post('/chat')
def chat(userinput: ChatMessage):
    user_message =userinput.message
    
    # print(user_message)
    if not user_message:
        return {'error': 'No message provided'}, 400
    # Get model response
    bot_response = generate_response(user_message, metrics,predictions, predictive_model)
    # print(bot_response)
    # Return the response as JSON
    return {'response': bot_response}

# Define the route for chat interaction
@app.get('/refresh')
def refresh():
    # print("here")
    metrics = refreshPromData()
    json_data = metrics.to_dict(orient="records")
    # print(json_data)
    return {'response': json_data}

# Define a route that listens for GET requests on the root path
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# Global error handler middleware
@app.middleware("http")
async def add_exception_handling(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"An unexpected error occurred: {str(e)}"},
        )

