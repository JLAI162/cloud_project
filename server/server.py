# pip install fastapi uvicorn

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
import socket 

app = FastAPI()

# Define a model for the request body
class Message(BaseModel):
    message: str

# Define a route to serve HTML page
@app.get("/", response_class=HTMLResponse)
async def get_html():
    with open("./homepage.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


# Define a route to handle POST requests
@app.post("/send")
async def send_message(message: Message):
    local_ip = '172.17.0.3'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((local_ip, 8001)) 
    data, addr = self.sock.recvfrom(1024)
    message_info = data.decode('utf-8')

    return {"response": {message_info}}

# Run the server using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)


