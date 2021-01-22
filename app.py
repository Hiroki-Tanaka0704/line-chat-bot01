#./ngrok http 5000

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from time import time

app = Flask(__name__)

line_bot_api = LineBotApi('E2Y/+MbAiqMrNUw/me1ADnJV67i8+akxvfHtw8gfSBddTbDWFu1CiBbLCApnGtV6MiKiSDqrfg9bKnkVnk//uYf8b05fp/9uFU4aRDeO7bNQHGXqrgnwzb3XbtLBeoPQU5LDznmldZA7nqCmJroH0AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('9ba0bf3d1536b90eb9e64e5f244cddac')

@app.route("/")
def test():
    return "OK"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(200)

    return 'OK'

users = {}
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    userId = event.source.user_id
    if event.message.text=="勉強開始":
        reply_message = "計測を開始しました。"
        if not userId in users:
            users[userId] = {}
            users[userId]["total"] = 0
        users[userId]["start"] = time()

    elif event.message.text=="勉強終了":
        end = time()
        dif = int(end - users[userId]["start"])
        users[userId]["total"]+=dif
        hour = dif//3600
        minute = (dif%3600)//60
        second = dif %60
        total = users[userId]['total']
        hour_t = total//3600
        minute_t = (total%3600)//60
        second_t = total %60
        reply_message = f"ただいまの勉強時間は{hour}時間{minute}分{second}秒です。お疲れさまでした。\
            本日は合計で{hour_t}時間{minute_t}分{second_t}秒勉強しています。"
    else:
        reply_message = "1日の勉強時間を計測するボットです。勉強を開始する時に「勉強開始」、勉強が終わった時に「勉強終了」と言ってね。"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message))

if __name__ == "__main__":
    app.run()
