# pip install fastapi uvicorn

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from typing import List

app = FastAPI()

# Define a model for the request body
class Message(BaseModel):
    message: str

# Define a fake response for demonstration
fake_response = [
    {"title": "Example Title 1", "link": "http://example.com/1", "content": "Example Content 1"},
    {"title": "Example Title 2", "link": "http://example.com/2", "content": "Example Content 2"}
]

# Define a route to serve HTML page
@app.get("/", response_class=HTMLResponse)
async def get_html():
    with open("./homepage.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


# Define a route to handle POST requests
@app.post("/send")
async def send_message(message: Message):
    # For demonstration purposes, just return a fake response
    return {"response": fake_response}

# Run the server using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8081)