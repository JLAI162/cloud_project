

# -*- coding: utf-8 -*-

import subprocess
import asyncio

from fastapi import FastAPI, Request, HTTPException
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

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class Item(BaseModel):
    id: str

configuration = Configuration(
    access_token=''
)
api_client = ApiClient(configuration)
line_bot_api = MessagingApi(api_client)
parser = WebhookParser('')


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

        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text="sucess")]
            )
        )
        
        id = event.source.user_id
        output = f"--output=/shared-data/tasks/{id}"
        # 调用 sbatch 命令执行作业脚本，并传递参数
        result = subprocess.run(['sbatch', output, 'compute.sh', id, event.message.text])

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
        print(id)
        if id != None:
            output = f"/shared-data/tasks/{id}"

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

@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    result_sinfo = subprocess.run(['sinfo'], capture_output=True, text=True)
    result_squeue = subprocess.run(['squeue'], capture_output=True, text=True)
    return templates.TemplateResponse("index.html", {"request": request, "sinfo": result_sinfo.stdout, "squeue": result_squeue.stdout})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)
