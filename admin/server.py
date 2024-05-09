# pip install fastapi uvicorn requests
# server.py

import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

app = FastAPI()

# Define a model for the request body
class Message(BaseModel):
    message: str


node_status = {
    "node1": {"status": "active", "queue": [101, 102]},
    "node2": {"status": "inactive", "queue": [103]},
    "node3": {"status": "active", "queue": [104, 105]}
}

# Define a route to handle POST requests
@app.post("/send")
async def send_message(message: Message):
    # 從消息對象中獲取消息文本
    message_text = message.message
    
    # 構建要發送的數據，這取決於目標服務器的要求
    payload = {"message": message_text}
    
    try:
        # 發送POST請求
        response = requests.post(target_url, json=payload)
        
        # 檢查響應狀態碼
        if response.status_code == 200:
            # 獲取響應內容
            response_content = response.json()
            return response_content
        else:
            return {"response": f"無法將消息發送到服務器{response.status_code}。"}

    except Exception as e:
        return {"response": f"發生錯誤：{str(e)}"}


@app.get("/node", response_class=JSONResponse)
async def get_nodes():
    return node_status

# Run the server using Uvicorn
if __name__ == "__main__":
    # nginx 服務器的URL 加上路徑導向computing Node
    target_url = "http://172.17.0.2:8080/llm"

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)


