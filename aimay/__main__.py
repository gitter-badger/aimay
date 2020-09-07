from . import core

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent, MessageEvent, TextMessage, TextSendMessage, StickerMessage, StickerSendMessage, ImageMessage, ImageSendMessage
)

app = Flask(__name__)

import os

# get environment variables from Heroku(Settings/Config Variables)
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET       = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler      = WebhookHandler(LINE_CHANNEL_SECRET)

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
        abort(400)

    return 'OK'

# MessageEvent
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # get push message
    push_text = event.message.text
    # get reply message and type
    reply_text, reply_type, reply_package, reply_sticker = core.get_replymessage(push_text)
    # reply
    if (reply_type == 'text'):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )
    elif (reply_type == 'sticker'):
        line_bot_api.reply_message(
            event.reply_token,
            StickerSendMessage(package_id=reply_package,sticker_id=reply_sticker)
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='エラーみたいだニャン')
        )

if __name__ == "__main__":
   # get port from Heroku
   port = int(os.getenv("PORT"))
   app.run(host="0.0.0.0", port=port)