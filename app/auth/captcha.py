from PIL import Image, ImageDraw, ImageFont, ImageFilter
from flask import session,make_response,current_app
from io import BytesIO
import random
from . import auth

# 随机字母:
def rndChar():

    return chr(random.randint(65, 90))


# 随机颜色1:
def rndColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))


# 随机颜色2:
def rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

def caeate_captcha(font):
    # 240 x 60:
    width = 60 * 4
    height = 60
    image = Image.new('RGB', (width, height), (255, 255, 255))
    # 创建Font对象:
    font = ImageFont.truetype(font, 36)
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)
    # 填充每个像素:
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=rndColor())
    # 输出文字:
    str=''
    for t in range(4):
        xrandom=chr(random.randint(65, 90))
        str+=xrandom
        draw.text((60 * t + 10, 10), xrandom, font=font, fill=rndColor2())

    # 模糊:
    image = image.filter(ImageFilter.BLUR)
    buf = BytesIO()

    image.save(buf, 'jpeg')
    return buf,str

@auth.route('/captcha/', methods=['GET', 'POST'])
def captcha():
    font=current_app.config['FONT']
    buf,str = caeate_captcha(font)
    session['captcha'] = str
    # print(session['captcha'],str)
    response = make_response(buf.getvalue())
    response.headers['Content-Type'] = 'image/jpeg'
    return response