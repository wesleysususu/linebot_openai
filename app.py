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

@app.route("/render_wake_up")
def render_wake_up():
    return "Hey!Wake Up!!"

import threading
import requests
def wake_up_render():
    while 1==1:
        url = 'https://linebot-openai-test-krs7.onrender.com/' + 'render_wake_up'
        res = requests.get(url)
        print(res)
        if res.status_code==200:
            print('喚醒render成功')
        else:
            print('喚醒失敗')
        time.sleep(14*60)

threading.Thread(target=wake_up_render).start()


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

    elif '3' in msg:
        message = TextSendMessage(A3)

    elif '4' in msg:
        message = TextSendMessage(A4)

    elif '5' in msg:
        message = TextSendMessage(A5)

    elif '6' in msg:
        message = TextSendMessage(A6)

    elif '7' in msg:
        message = TextSendMessage(A7)

    elif '8' in msg:
        message = TextSendMessage(A8)

    elif '9' in msg:
        message = TextSendMessage(A9)
    else:
        message = TextSendMessage('🌈親愛的朋友!➡️你可以重新輸入「0」即可透過主選菜單找到關鍵字解答你的問題喔‼️如需要真人服務,可直接加衛斯理LINE,謝謝!')
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
{name} 你好！！
歡迎加入我們的群組🎉
👋我是群組小助理：小瑞

🌈線上研討會會透過群組.簡訊.mail來告知!線上zoom研討會教室連結:https://zoom.us/j/8474897234 歡迎大家踴躍參與!!

⏰為了提升大家進群的效率，我來協助大家體驗智能管家的功能!

👉有任何問題你可以按「關鍵數 
     字」幫您解答 您的問題喔!

—>輸入 " 0 " 返回本目錄

—>輸入" 1 " 可以看Q1解答

—>輸入" 2 " 可以看Q2解答

依此類推‼️

Q1. 為何要學習自媒體??

Q2. 各行各業都可以使用嗎?

Q3. 老師能提供甚麼課程?

Q4. 自媒體學習使用上會不會很難?

Q5. 自媒體變現容易嗎?

Q6.關於自媒體的內容綱要有什麼？

Q7.我對3C不熟悉，會影響學習嗎？

Q8.我可以邀請朋友一起來參加學習嗎？

Q9.課程費用及開課時間？
    '''
    
    message = TextSendMessage(text_content)
    line_bot_api.reply_message(event.reply_token, message)       
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
