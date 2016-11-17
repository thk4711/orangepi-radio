#!/usr/bin/python
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

RST = 24

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Get display width and height.
size_x = disp.width
size_y = disp.height

# Clear display.
disp.clear()
#font = ImageFont.load_default()
#disp.display()

image = Image.new('1', (size_x, size_y))
draw  = ImageDraw.Draw(image)

# relative positions of objects on the screen
class disp_positions:
    statusbar_pos       = -1
    statusbar_txt_pos   = -5
    wifi_icon_x         = int(size_x/1.2)
    wifi_text_x         = int(size_x/1.13)
    vol_icon_x          = int(size_x/40)
    time_text_x         = int(size_x/3)
    play_icon_x         = int(size_x/8)
    name_y              = int(size_y/4.2)
    artist_y            = int(size_y/2.9)
    title_y             = int(size_y/2.2)
    radio_icon_x        = 45
    tone_icon_x         = int(size_x/5)
    big_icon_y          = 16
    tone_text_x         = int(size_x/2.3)
    tone_text_y         = int(size_y/2.3)
    current_tone_text_x = int(size_x/5)
    bar_x_start         = int(size_x/16)
    bar_y_start         = int(size_y/1.6)
    bar_x_width         = int(size_x/1.14)
    bar_y_width         = int(size_y/12.8)


# define fonts
small_font      = ImageFont.truetype("fonts/NotoSans-Regular.ttf", int(size_y/4))
small_font_bold = ImageFont.truetype("fonts/NotoSans-Bold.ttf", int(size_y/4))
medium_font     = ImageFont.truetype("fonts/NotoSans-Regular.ttf", int(size_y/4))
large_font      = ImageFont.truetype("fonts/NotoSans-Regular.ttf", int(size_y/3))
bold_font       = ImageFont.truetype("fonts/NotoSans-Bold.ttf", int(size_y/5))
icon_font_small = ImageFont.truetype("fonts/Material-Design-Iconic-Font.ttf", int(size_y/4))
icon_font_large = ImageFont.truetype("fonts/Material-Design-Iconic-Font.ttf", 35)
spot_font       = ImageFont.truetype("fonts/socialicious.ttf", int(size_y/2))

# define icons
wifi_icon_high   = u'\uf2e8'
wifi_icon_medium = u'\uf2e2'
wifi_icon_low    = u'\uf2e7'
vol_icon_high    = u'\uf3bc'
vol_icon_medium  = u'\uf3b9'
vol_icon_low     = u'\uf3ba'
vol_icon_off     = u'\uf3bb'
play_icon        = u'\uf3aa'
pause_icon       = u'\uf3a7'
radio_icon       = u'\uf2c2'
airplay_icon     = u'\uf3d2'
spotify_icon     = u'\u0051'
aux_in_icon      = u'\uf29f'
usb_in_icon      = u'\uf2dd'
bluetooth_icon   = u'\uf282'
tone_icon        = u'\uf10f'

#txt = "17:23 "
#draw.text((0, -3), txt, 1, font=small_font)

time_text = "17:05"
draw.text((disp_positions.time_text_x,disp_positions.statusbar_txt_pos), time_text, 1, small_font)

draw.text((disp_positions.vol_icon_x,disp_positions.statusbar_pos), vol_icon_high , 1, icon_font_small)
draw.text((disp_positions.wifi_icon_x,disp_positions.statusbar_pos), wifi_icon_low , 1, icon_font_small)
#draw.text((disp_positions.time_text_x, -3), time_text, 1, small_font_bold)

draw.rectangle(((0,53),(127,63)), fill=0, outline = 1)
draw.rectangle(((2,55),(125,61)), fill=1, outline = 0)




#txt = "DRadio Wissen   "
#draw.text((0, 8), txt, 1, font=small_font)

#txt = "Volume    -72 dB   "
#draw.text((0, 20), txt, 1, font=small_font)

#txt = radio_icon
#draw.text((disp_positions.radio_icon_x, disp_positions.big_icon_y), txt, 1, font=icon_font_large)

txt = "DRadio Wissen"
width, height = draw.textsize(txt, font=small_font)
print width
print height
draw.text((-20,12), txt, 1, font=small_font)

#draw.text((50, 50), "hey")
disp.image(image)
disp.display()


# scroll text if longer that display width
def scroll_text(raw_text,font,y_pos,x_pos,speed):
    txt_width, txt_height =  draw.textsize(raw_text, font = font)
    if ( size_x < txt_width ):
        raw_text = raw_text + " * "
        txt_width, txt_height =  draw.textsize(raw_text, font = font)
        if x_pos < -txt_width:
            x_pos=0
        draw.text((x_pos,y_pos), raw_text, 0, font=font)
        draw.text((x_pos+txt_width,y_pos), raw_text, 0, font=font)
        x_pos = x_pos - speed
        draw.text((x_pos,y_pos), raw_text, 1, font=font)
        draw.text((x_pos+txt_width,y_pos), raw_text, 1, font=font)
        return x_pos
    else:
        x_pos = (size_x - text.get_width()) // 2
        draw.text((x_pos,y_pos), raw_text, 1, font=font)
        return 0

scroll_pos = 0
scroll_txt = "Das ist ein Test ob das denn scrollt"

while True:
    #image = Image.new('1', (size_x, size_y))
    #draw  = ImageDraw.Draw(image)
    scroll_pos = scroll_text(scroll_txt, small_font, 12, scroll_pos, 1)
    disp.image(image)
    disp.display()
    #time.sleep(0.1)




# time.sleep(10)
