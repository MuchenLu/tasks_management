from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
import os

app = Flask(__name__)

# 從環境變數讀取
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('JHTIDJsaC0unpyW2f6tXANzmlfa0ycuuS31SSuyOguL8kBu06/bqhaqyBILWMSRLC8FKeDre9RMXP+r+vz+hsCczQ/mvETpW+3ryx+h26pzI/gW2Almgj1YhILsqgkV1F6Envmwsjjxc1jc+kyLgHgdB04t89/1O/w1cDnyilFU=')
LINE_CHANNEL_SECRET = os.getenv('f1beba2750b51fca5c5e44f5c5e961f8')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/webhook", methods=['POST'])
def webhook():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return 'Invalid signature', 400
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    line_bot_api.reply_message(
        event.reply_token, 
        TextMessage(text=f"你說：{text}")
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))