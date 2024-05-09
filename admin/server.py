# pip install fastapi uvicorn requests
# server.py

import re
import os
import time
import threading
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from helper import rendom_dir_name


def _listen_status():
    last_read_time = {
        "node1": None,
        "node2": None,
        "node3": None
    }
    while True:
        for file_name in last_read_time.key():
            with open(file_name + ".txt", 'r') as file:
                for line in file:
                    match = re.search(r'(\d{2}:\d{2}:\d{2})', line)
                    if match:
                        time_str = match.group(1)
                        current_time = time.strptime(time_str, "%H:%M:%S")
                        
                        if last_read_time[file_name] is not None and (time.mktime(current_time) - time.mktime(last_read_time)) >= 2:
                            time_difference = time.mktime(current_time) - time.mktime(last_read_time)
                            if time_difference > 2:
                                node_status[file_name]['status'] = 'activate'        
                        
                        last_read_time[file_name] = current_time
        time.sleep(3)



app = FastAPI()

# Define a model for the request body
class Message(BaseModel):
    message: str

# Define a route to handle POST requests
@app.post("/send")
async def send_message(message: Message):

    work_address = "/share/work/"

    # 設定資料夾名稱長度
    folder_name_length = 15

    while True:
        # 隨機生成資料夾名稱 
        folder_name = rendom_dir_name(folder_name_length)

        # 檢查資料夾 "my_folder" 是否存在
        if not os.path.exists(work_address + folder_name):     
            # 創建資料夾
            os.makedirs(work_address + folder_name)
            break

    # 從消息對象中獲取消息文本
    message_text = message.message
    # 寫入
    with open(work_address + folder_name + "/input.txt", "w", encoding="utf-8") as f:
        f.write(message_text)

    with open(work_address + folder_name + "/status.txt", "w", encoding="utf-8") as f:
        f.write("wait")
    
    # 構建要發送的數據，這取決於目標服務器的要求
    payload = {"id": folder_name}
    
    try:
        # 發送POST請求
        response = requests.post(target_url, json=payload)
        
        # 檢查響應狀態碼
        if response.status_code == 200:
            # 獲取響應內容
            if response.json() == 'success':
                with open(work_address + folder_name + "/output.txt", "r", encoding="utf-8") as f:
                    response_content = f.read()

                with open(work_address + folder_name + "/status.txt", "w", encoding="utf-8") as f:
                    f.write("complete")

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

    node_status = {
        "node1": {"status": "inactive", "queue": [101, 102]},
        "node2": {"status": "inactive", "queue": [103]},
        "node3": {"status": "inactive", "queue": [104, 105]}
    }
    threading.Thread(target=_listen_status).start()

    import uvicorn
    uvicorn.run(app, host="172.17.0.3", port=8081)


