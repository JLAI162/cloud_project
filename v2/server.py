from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, AudioSendMessage, VideoSendMessage, StickerSendMessage, ImageSendMessage, LocationSendMessage

line_bot_api = LineBotApi('//+++/1O/w1cDnyilFU=+XgaVwcp2T9cUBMG0L+69seM7cP0kj6AkoVTlDYeN8W47yiQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('')

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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text
    if mtext == '@傳送聲音':
        try:
            message = AudioSendMessage(
                original_content_url='./staticmario.m4a', 
                duration=20000  #聲音長度20秒
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

    elif mtext == '@傳送影片':
        try:
            message = VideoSendMessage(
                original_content_url='./static/robot.mp4',  #影片檔置於static資料夾
                preview_image_url='./staticrobot.jpg'
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

@app.get("/")
async def home(id: str = None, msg: str = None):
    try:
        if id != None:
            line_bot_api.push_message(id, TextSendMessage(text=msg))
        else:
            msg = 'ok'   
        return msg
    
    except Exception as e:
        print('error', e)
        return '500 error'

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
