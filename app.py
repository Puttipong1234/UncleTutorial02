import os
import sys
from argparse import ArgumentParser
from Resource.reply import SetMenuMessage_Object , send_flex
from flask import Flask, request, abort ,send_from_directory
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)
richmenu = {
    'menu1':'richmenu-28e64a0f986d964993257c63ab2c46a9',
    'menu2':'richmenu-3d8a86629113fd74959bb3f88e0ac7f4'
}

# get channel_secret and channel_access_token from your environment variable
channel_secret = '85d6c7b172bc420bcf6fb1e60601b9ae'
channel_access_token = "zVxemPBnRLwSfHpWiziWpsAHCYkqGTYe9FOlirMAUI03NRtmDIyXyMrd4WcBTGCGEN5i/3SnVi/TsZs9hmxE08UDme4HaYtk45S+0mBJO6VxRQeaWYyYSGyBngtPBL7b7AnjFD6p9UZWNXlP3c6BqwdB04t89/1O/w1cDnyilFU="


line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/webhook", methods=['POST'])
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


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    print(event)
    Text_fromUser = event.message.text
    reply_Token = event.reply_token

    if 'เช็คราคา' in Text_fromUser:
        from Resource.bxAPI import GetBxPrice
        msg = GetBxPrice(Number_to_get=10)
        from Resource.FlexMessage import setCarousel
        flex = setCarousel(msg)  ### setup carousel
        flex = SetMenuMessage_Object(flex) ### setup flex
        send_flex(reply_Token , flex , channel_access_token)
    
    elif 'เช็คข่าวสาร' in Text_fromUser:
        from Resource.GetNews import get_cnn_news
        data = get_cnn_news()
        from Resource.FlexMessage import news_setbubble
        msg = news_setbubble(data['title'],data['description'],data['url'],data['image_url'])
        flex = SetMenuMessage_Object(msg)
        send_flex(reply_Token , flex , channel_access_token)
    
    else :
        message = '' ### message ที่เราจะส่งกลับไปให้ยูสเสอ
        text = []
        user_data = None

        from dialogflow_uncle import detect_intent_texts
        project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
        session_id = event.source.user_id  ## get user id
        message = detect_intent_texts(project_id,session_id,Text_fromUser,'th')
        

        for i in message['fulfillment_messages']: ### เพิ่มจากในคลิบ
            txt = TextSendMessage(text=i)### เพิ่มจากในคลิบ
            text.append(txt)### เพิ่มจากในคลิบ

        ## adding imagemap message เรียนอะไร
        if message['action'] == 'register':
            from MessageTemplate.Imgmap import selectCourse
            imagemap = Base.get_or_new_from_json_dict(selectCourse(),ImagemapSendMessage)
            text.append(imagemap)
            ### prepare imagemap message to send

        #### เรียนที่ไหน
        elif message['action'] == 'selectcourses':
            from MessageTemplate.Imgmap import selectWhere
            imagemap = Base.get_or_new_from_json_dict(selectWhere(),ImagemapSendMessage)
            text.append(imagemap)
            ### prepare Imagemap message to send

        ### ให้ยูสเซอลงเวลา
        elif message['action'] == 'selecttype':
            from MessageTemplate.Imgmap import selectTime
            msg = Base.get_or_new_from_json_dict(selectTime(),TemplateSendMessage)
            text.append(msg)
        
        #### confirm message
        elif message['action'] == 'selectmonth':
            from MessageTemplate.Imgmap import confirmRegis
            msg = Base.get_or_new_from_json_dict(confirmRegis(),TemplateSendMessage)
            text.append(msg)
        
        ### sumarize message
        elif message['action'] == 'confirm':
            from google.protobuf.json_format import MessageToDict
            data = message['parameters']
            data = MessageToDict(data)

            from MessageTemplate.Imgmap import GetStudentCard


            ####เนื้องจากการส่งข้อความแบบ flex2019 SDK python ยังไม่รองรับทำให้เราต้องกลับมาส่งแบบ manual
            msg = []
            for i in text:
                Dict = i.as_json_dict()
                msg.append(Dict)
            msg.append(GetStudentCard(data['courses']))
            flex = SetMenuMessage_Object(msg)
            send_flex(reply_Token,file_data = flex,bot_access_key = channel_access_token)
        #### กรณีเข้าโหมดถามตอบ
        elif message['action'] == 'q&a':
            line_bot_api.link_rich_menu_to_user(session_id,richmenu['menu2'])
        #### กรณีกำลังถามตอบ
        elif message['action'] == 'qa.qa-fallback':
            from MessageTemplate.Imgmap import AnwserMsg

            from Resource.wolf import search_wiki

            result = search_wiki(Text_fromUser)

            ### set msg + answer
            Flex_Ans = AnwserMsg(Text_fromUser,result)

            ### set quick reply
            qbtn = QuickReplyButton(image_url='https://cdn0.iconfinder.com/data/icons/online-education-butterscotch-vol-2/512/Questions_And_Answers-512.png'
            ,action=MessageAction('หยุดถาม','หยุดถาม'))
            q = QuickReply(items=[qbtn])

            ### set text as json
            new_text1 = TextSendMessage(text='ลุงขอหาแปรป...').as_json_dict()
            new_text2 = TextSendMessage(text='อยากถามต่อไหม ถ้าไม่... กดปุ่ม หยุดถามได้เลยจร้า',quick_reply=q).as_json_dict()

            ### send msg with quick reply
            flex = SetMenuMessage_Object(Message_data=[new_text1,Flex_Ans,new_text2])

            r = send_flex(Reply_token,file_data = flex,bot_access_key = channel_access_token)
        #### กรณีหยุดถาม
        elif message['action'] == 'qa.qa-custom':
            line_bot_api.link_rich_menu_to_user(session_id,richmenu['menu1'])
            text = TextSendMessage(text='แล้วกลับมาถามใหม่น่าาาา...')
            line_bot_api.reply_message(reply_Token,text)
        print(message['action'])
        line_bot_api.reply_message(reply_Token,text)
            
    
    return 'OK'

@handler.add(FollowEvent)
def LinkRichmenu(event):
    userid = event.source.user_id  ### get user id มาก่อน
    disname = line_bot_api.get_profile(user_id=userid).display_name ## display name

    qbtn1 = QuickReplyButton(image_url='https://i1.wp.com/sbo2com.net/wp-content/uploads/2018/10/register-icon.png?fit=250%2C242&ssl=1',
    action=MessageAction(label='สมัครเรียนไพทอน',text='สนใจสมัครเรียนไพทอน'))
    qbtn2 = QuickReplyButton(action=MessageAction(label='ทดสอบความรู้บอท',text='ไหนขอทดสอบความรู้หน่อยซฺิ'))
    q_reply = QuickReply(items=[qbtn1,qbtn2])

    text = TextSendMessage(text='ยินดีต้อนรับคุณ {} เข้าสู่บริการ ลุงวิศวกรสอนคำนวณ'.format(disname),quick_reply=q_reply)
    reply_Token = event.reply_token
    line_bot_api.reply_message(reply_Token,text)

    line_bot_api.link_rich_menu_to_user(userid,richmenu['menu1'])

@handler.add(PostbackEvent)  ### สำหรับรับ date time picker
def GetPostback(event):
    Reply_token = event.reply_token
    Text_fromUser = event.postback.params['datetime']
    print(Text_fromUser)

    month = int(Text_fromUser[5:7])
    print(month)

    import datetime

    monthinteger = month

    month = str(datetime.date(1900, monthinteger, 1).strftime('%B'))
    if month == 'October':
        month = 'ตุลาคม'
    elif month == 'December':
        month = 'ธันวาคม'

    print (month)

    message = '' ### message ที่เราจะส่งกลับไปให้ยูสเสอ
    from dialogflow_uncle import detect_intent_texts
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    session_id = event.source.user_id  ## get user id
    message = detect_intent_texts(project_id,session_id,month,'en')
    
    text = []
    user_data = None

    for i in message['fulfillment_messages']:### เพิ่มจากในคลิบ
        txt = TextSendMessage(text=i)### เพิ่มจากในคลิบ
        text.append(txt)### เพิ่มจากในคลิบ
    
    if message['action'] == 'selectmonth':
        from MessageTemplate.Imgmap import summary_msg
        data = message['parameters']
        from google.protobuf.json_format import MessageToDict
        data = MessageToDict(data)
        when = data['month']
        where = data['Type']
        course = data['courses']
        msg = Base.get_or_new_from_json_dict(summary_msg(when,where,course),FlexSendMessage)
        text.append(msg)### เพิ่มจากในคลิบ
    


    res = line_bot_api.reply_message(Reply_token,messages=text)

@app.route('/MessageTemplate/<image>/1040')
def serveimage(image):
    return send_from_directory('MessageTemplate',image)

### serve simple image
@app.route('/MessageTemplate/<PICNAME>')
def getpicbyname_static(PICNAME):
    print('PIC : ' + PICNAME)
    path = 'MessageTemplate'
    return send_from_directory(path,PICNAME)


if __name__ == "__main__":
    os.environ['DIALOGFLOW_PROJECT_ID'] = 'loongwissawa-uixaxu'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'Credentials.json'
    app.run(port=8000)