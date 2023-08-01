from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import logging

logging.basicConfig(level=logging.INFO)

from message import*

#======python的函數庫==========
import tempfile, os
import datetime
import openai
import time
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi("xAJ+N1oZ1cX4gZlo82ZPNzbGxREROpRMbqeAcN07HtuiQerS6YeAnhmeqm9PgdVINwwfb6sVj/7eZIjxrQCfXOlPU9kbtW0/r5K3gjzr5GKO3xUmNR96YMGoU0KdCRMiSdS2xlHmpOfWt8uTMQ3mEgdB04t89/1O/w1cDnyilFU=")
# Channel Secret
handler = WebhookHandler("07659ca99dd6aa7ea0b9c39f201ed0ec")
# OPENAI API Key初始化設定
# openai.api_key = os.getenv('OPENAI_API_KEY')


def GPT_response(text):
    # 接收回應
    response = openai.Completion.create(model="text-davinci-003", prompt=text, temperature=0.5, max_tokens=500)
    print(response)
    # 重組回應
    answer = response['choices'][0]['text'].replace('。','')
    return answer


# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'


# 處理訊息

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    print(msg)
    if '1' in msg:
        message = TextSendMessage(A1)
    elif '2' in msg:
        message = TextSendMessage(A2)
    elif '0' in msg:
        message = TextSendMessage(A0)


    else:
        message = TextSendMessage(text=msg)
    line_bot_api.reply_message(event.reply_token, message)
    
@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)

@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    text_content = f'''
{name}  你好!!
歡迎加入影響力溝通群組~
👋我是智能群管家：小衛
⏰為了提升大家進群的效率，我來
帶大家體驗智能管家的功能

📌輸入：0:返回本目錄📌
輸入「1」可以看Q1解答
輸入「2」可以看Q2解答
以此類推……………………….

Q1.影響力溝通是什麼？
Q2.關於課程內容有哪些？
Q3.課程內容可以幫助我得到什麼？
Q4.上完課如果有不懂的地方怎麼辦？
Q5.報名課程還能有什麼相關資訊？
Q6.課程前我要準備什麼？
Q7.關於自媒體的內容綱要有什麼？
Q8.我對3C不熟悉，會影響學習嗎？
Q9.我要如何透過平台變現？
Q10.我可以邀請朋友一起來參加學習嗎？
    '''
    
    message = TextSendMessage(text_content)
    line_bot_api.reply_message(event.reply_token, message)       
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
