

# -*- coding: utf-8 -*-

import os
from datetime import datetime
import subprocess
import asyncio

from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from linebot.v3.webhook import WebhookParser
from linebot.v3.messaging import (
    AsyncApiClient,
    AsyncMessagingApi,
    ApiClient,
    MessagingApi,
    Configuration,
    ReplyMessageRequest,
    PushMessageRequest,
    TextMessage
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
###################
##  configuation
################### 
app = FastAPI()
templates = Jinja2Templates(directory="templates")

class Item(BaseModel):
    id: str
    ftime: str

configuration = Configuration(
    access_token=''
)
api_client = ApiClient(configuration)
line_bot_api = MessagingApi(api_client)
parser = WebhookParser('')

#############################
#############################


#####################
## line bot
#####################

@app.post("/callback")
async def handle_callback(request: Request):
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = await request.body()
    body = body.decode()

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessageContent):
            continue
        '''
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text="sucess")]
            )
        )
        '''
        mtext = event.message.text
        id = event.source.user_id

        # Get the current time
        current_time = datetime.now()

        concatenated_time = (
            f"{current_time.year}"
            f"{current_time.month:02d}"
            f"{current_time.day:02d}"
            f"{current_time.hour:02d}"
            f"{current_time.minute:02d}"
            f"{current_time.second:02d}"
        )

        if not os.path.exists("/shared-data/tasks/{id}"):     
            # 創建資料夾
            os.makedirs("/shared-data/tasks/{id}")

        output = f"--output=/shared-data/tasks/{id}/{concatenated_time}"

        # 调用 sbatch 命令执行作业脚本，并传递参数
        if mtext[0] == '@':
            result = subprocess.run(['sbatch', output, 'compute.sh', id, concatenated_time, mtext[1:]])
        else:
            result = subprocess.run(['sbatch', output, 'normal.sh', id, concatenated_time, mtext])

        # 检查 sbatch 命令的返回码
        if result.returncode == 0:
            print('作业提交成功')
        else:
            print('作业提交失败，返回码:', result.returncode)


    return 'OK'

@app.post("/response")
async def home(item: Item):
    try:
        id = item.id
        ftime = item.ftime
        print(id)
        if id != None:
            output = f"/shared-data/tasks/{id}/{ftime}"

            await asyncio.sleep(5)
            reposnse_message = open(output, "r", encoding="utf-8").read()

            line_bot_api.push_message(PushMessageRequest(
                    to=id,
                    messages=[TextMessage(text=reposnse_message)]
                ))
            msg = 'ok'
        else:
            msg = 'id error'   
        return msg
    
    except Exception as e:
        print('error', e)
        return '500 error'


#####################
## admin webpage
#####################

@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    result_sinfo = subprocess.run(['sinfo'], capture_output=True, text=True)
    result_squeue = subprocess.run(['squeue'], capture_output=True, text=True)
    result_sprio = subprocess.run(['sprio'], capture_output=True, text=True)
    return templates.TemplateResponse("index.html", {"request": request, "sinfo": result_sinfo.stdout, "squeue": result_squeue.stdout, "sprio": result_sprio.stdout})

@app.post("/submit_id")
async def submit_id(request: Request, job_id: str = Form(...)):
    result = subprocess.run(['scancel', job_id])

    # 检查 scancel 命令的返回码
    if result.returncode == 0:
        print(f"作業 {job_id} 刪除成功")
    else:
        print(f"作業 {job_id} 刪除失敗，返回碼: {result.returncode}, 錯誤信息: {result.stderr}")

    result_sinfo = subprocess.run(['sinfo'], capture_output=True, text=True)
    result_squeue = subprocess.run(['squeue'], capture_output=True, text=True)
    result_sprio = subprocess.run(['sprio'], capture_output=True, text=True)
    return templates.TemplateResponse("index.html", {"request": request, "sinfo": result_sinfo.stdout, "squeue": result_squeue.stdout, "sprio": result_sprio.stdout})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)
