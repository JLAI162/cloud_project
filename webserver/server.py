# pip install fastapi uvicorn
# server.py

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

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
    # 從消息對象中獲取消息文本
    message_text = message.message
    
    # 構建要發送的數據，這取決於目標服務器的要求
    payload = {"message": message_text}
    
    # 目標服務器的URL
    target_url = "http://172.17.0.3:8081/inference"
    
    try:
        # 發送POST請求
        response = requests.post(target_url, json=payload)
        
        # 檢查響應狀態碼
        if response.status_code == 200:
            # 獲取響應內容
            response_content = response.json()
            return {"response": response_content}
        else:
            return {"response": "無法將消息發送到服務器。"}

    except Exception as e:
        return {"response": f"發生錯誤：{str(e)}"}

# Run the server using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)


