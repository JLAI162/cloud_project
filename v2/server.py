from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse


from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from linebot.models import MessageEvent, TextMessage, AudioSendMessage, VideoSendMessage


configuration = Configuration(access_token='JWXOXf40VeKq/APq73N9QnXHoSCOXtTjIZTkY/3lYmF6e89NnVtFqFdSKShJZ+0ic6h5Qh1aHTWX9L4WoTUlWGddWF9BIiFpv0MRa9+XgaUQKsr91AMuwJBEQEH0RB2a12gwz3Vf+yTRkR1bm2yKZAdB04t89/1O/w1cDnyilFU=+XgaVwcp2T9cUBMG0L+69seM7cP0kj6AkoVTlDYeN8W47yiQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('7c50858e2a0c9a37c411b1b32f59afc0')

app = FastAPI()

@app.post("/callback")
async def callback(request: Request):
    # Get request header
    signature = request.headers['x-line-signature']

    # Get request body as text
    body = await request.body()
    body = body.decode('utf-8')

    try:
        # Handle webhook body
        handler.handle(body, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):

    mtext = event.message.text

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        if mtext == '@傳送聲音':
            try:
                message = AudioSendMessage(
                    original_content_url='./staticmario.m4a', 
                    duration=20000  #聲音長度20秒
                )
                line_bot_api.reply_message(event.reply_token, message)
            except:
                line_bot_api.reply_message(event.reply_token, messages=[TextMessage(text='發生錯誤！')])

        elif mtext == '@傳送影片':
            try:
                message = VideoSendMessage(
                    original_content_url='./static/robot.mp4',  #影片檔置於static資料夾
                    preview_image_url='./staticrobot.jpg'
                )
                line_bot_api.reply_message(event.reply_token, message)
            except:
                line_bot_api.reply_message(event.reply_token, messages=[TextMessage(text='發生錯誤！')])

@app.get("/")
async def home(id: str = None, msg: str = None):
    try:
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)

            if id != None:
                line_bot_api.push_message(id, messages=[TextMessage(text=msg)])
            else:
                msg = 'ok'   
            return msg
    
    except Exception as e:
        print('error', e)
        return '500 error'


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
