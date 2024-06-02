

# -*- coding: utf-8 -*-
from fastapi import FastAPI, Request, HTTPException

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

configuration = Configuration(
    access_token='JWXOXf40VeKq/APq73N9QnXHoSCOXtTjIZTkY/3lYmF6e89NnVtFqFdSKShJZ+0ic6h5Qh1aHTWX9L4WoTUlWGddWF9BIiFpv0MRa9+XgaUQKsr91AMuwJBEQEH0RB2a12gwz3Vf+yTRkR1bm2yKZAdB04t89/1O/w1cDnyilFU=+XgaVwcp2T9cUBMG0L+69seM7cP0kj6AkoVTlDYeN8W47yiQdB04t89/1O/w1cDnyilFU='
)
api_client = ApiClient(configuration)
line_bot_api = MessagingApi(api_client)
parser = WebhookParser('7c50858e2a0c9a37c411b1b32f59afc0')


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
                messages=[TextMessage(text=event.message.text)]
            )
        )

    return 'OK'

@app.get("/")
async def home(id: str = None, msg: str = None):
    try:

        if id != None:
            line_bot_api.push_message(PushMessageRequest(
                    to='J Lai',
                    messages=[TextMessage(text="Push!")]
                ))
        else:
            msg = 'ok'   
        return msg
    
    except Exception as e:
        print('error', e)
        return '500 error'


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
