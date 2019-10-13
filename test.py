from linebot.models import *

text = TextSendMessage(text='สวัสดีครับ')


text = TextSendMessage(text='สวัสดีครับ').as_json_dict()

image = ImageSendMessage(original_content_url='www.google.com')
print(image)
