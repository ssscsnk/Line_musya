from linebot import LineBotApi, WebhookHandler

#各クライアントライブラリのインスタンス作成
line_bot_api = LineBotApi(channel_access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(channel_secret=LINE_ACCESS_SECRET)

from django.http import HttpResponseForbidden, HttpResponse
from linebot.exceptions import InvalidSignatureError

def callback(request):
  #リクエストヘッダーから署名検証のための値を取得
  signature = request.META['HTTP_X_LINE_SIGNATURE']
  #リクエストボディを取得
  body = request.body.decode('utf-8')
  try:
    #署名を検証し、問題なければhandleに定義されている関数を呼び出す
    handler.handle(body, signature)
  except InvalidSignatureError:
    #署名検証で失敗した時は例外をあげる
    HttpResponseForbidden()
  #handleの処理を終えればOK
  return HttpResponse('OK', status=200)

#linebot.modelsから処理したいイベントをimport
from linebot.models import (
  FollowEvent, TextSendMessage
)

#addメソッドの引数にはイベントのモデルを入れる
#関数名は自由
@handler.add(FollowEvent)
def handle_follow(event):
  line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text='初めまして')
  )

