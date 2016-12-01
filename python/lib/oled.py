#!/usr/local/bin/python
#!/usr/bin/env python

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

RST = "P9_12"

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_bus=0)

# Initialize library.
disp.begin()
disp.clear()

# Get display width and height.
size_x = disp.width
size_y = disp.height

image = Image.new('1', (size_x, size_y))
draw  = ImageDraw.Draw(image)

# define colors
white      = 1
black      = 0

needed = True

# define fonts
small_font      = ImageFont.truetype("fonts/NotoSans-Regular.ttf", int(size_y/4))
medium_font     = ImageFont.truetype("fonts/NotoSans-Regular.ttf", int(size_y/4))
icon_font_small = ImageFont.truetype("fonts/Material-Design-Iconic-Font.ttf", int(size_y/4))
icon_font_large = ImageFont.truetype("fonts/Material-Design-Iconic-Font.ttf", int(size_y/2))
spot_font       = ImageFont.truetype("fonts/socialicious.ttf", int(size_y/2.2))

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

# define display areas
class disp_content:
    tonemode      = ""
    tonevalue     = 0
    time          = ""
    name          = ""
    artist        = ""
    title         = ""
    app_mode      = 0
    source_string = 0
    wifi          = 0
    volume        = 0
    mpd_stat      = ""
    wifi_icon     = ""
    power_state   = ""

# define display areas
class last_disp_content:
    tonemode      = " "
    tonevalue     = 1
    time          = " "
    name          = " "
    artist        = " "
    title         = " "
    app_mode      = 1
    source_string = 1
    wifi          = 1
    volume        = 1
    mpd_stat      = " "
    wifi_icon     = ""
    power_state   = ""


# remember last position of scrolled text
class scroll_pos:
    name   = 0
    artist = 0
    title  = 0

# positions of objects on the screen
class disp_positions:
    statusbar_pos       = -1
    statusbar_txt_pos   = -5
    wifi_icon_x         = int(size_x/1.2)
    wifi_text_x         = int(size_x/1.13)
    vol_icon_x          = int(size_x/40)
    time_text_x         = int(size_x/2.7)
    play_icon_x         = int(size_x/6)
    name_y              = int(size_y/4.2)
    artist_y            = int(size_y/2.9)
    title_y             = int(size_y/2.2)
    radio_icon_x        = int(size_y/1.3)
    tone_icon_x         = int(size_x/5)
    big_icon_y          = int(size_y/4)
    tone_text_x         = int(size_x/2.3)
    tone_text_y         = int(size_y/2.3)
    current_tone_text_x = int(size_x/5)
    bar_x_start         = int(size_x/16)
    bar_y_start         = int(size_y/1.6)
    bar_x_width         = int(size_x/1.14)
    bar_y_width         = int(size_y/12.8)

disp.image(image)
disp.display()

def which_wifi_icon(value):
    icon = ""
    if value > 70:
        icon = "wifi_icon_high"
    elif value > 30:
        icon = "wifi_icon_medium"
    elif value <= 30:
        icon = "wifi_icon_low"
    return(icon)

def check_if_update_needed():
    #global nedded
    needed = 0
    disp_content.wifi_icon = which_wifi_icon(disp_content.wifi)
    if last_disp_content.wifi_icon != disp_content.wifi_icon:
        needed = 1
        last_disp_content.wifi_icon = disp_content.wifi_icon
    if last_disp_content.volume != disp_content.volume:
        needed = 2
    if last_disp_content.tonevalue != disp_content.tonevalue:
        needed = 3
    if last_disp_content.time != disp_content.time:
        needed = 4
    if last_disp_content.app_mode != disp_content.app_mode:
        needed = 5
    if disp_content.app_mode == "RAD":
        if disp_content.mpd_stat != last_disp_content.mpd_stat:
            needed = 6
        if ((last_disp_content.name != disp_content.name) and (disp_content.mpd_stat == "play")):
            needed = 7
    return(needed)

#-----------------------------------------------------------------#
#  blank screen when power off                                    #
#-----------------------------------------------------------------#
def check_power_state():
    if disp_content.power_state == "OFF":
        if last_disp_content.power_state == "ON":
            draw.rectangle(((0,0),(127,62)), fill=0, outline = 0)
            disp.image(image)
            disp.display()
            disp_content.tonemode      = " "
            disp_content.tonevalue     = 1
            disp_content.time          = " "
            disp_content.name          = " "
            disp_content.artist        = " "
            disp_content.title         = " "
            disp_content.app_mode      = 1
            disp_content.source_string = 1
            disp_content.wifi          = 1
            disp_content.volume        = 1
            disp_content.mpd_stat      = " "
            disp_content.wifi_icon     = ""
        last_disp_content.power_state = disp_content.power_state
        return(0)
    else:
        if last_disp_content.power_state == "OFF":
            disp_content.tonemode      = " "
            disp_content.tonevalue     = 1
            disp_content.time          = " "
            disp_content.name          = " "
            disp_content.artist        = " "
            disp_content.title         = " "
            disp_content.app_mode      = 10
            disp_content.source_string = 1
            disp_content.wifi          = 1
            disp_content.volume        = 1
            disp_content.mpd_stat      = " "
            disp_content.wifi_icon     = ""
        last_disp_content.power_state = disp_content.power_state
        return(1)

#-----------------------------------------------------------------#
#  update display                                                 #
#-----------------------------------------------------------------#
def update_display(now):
    power_state = check_power_state()
    if power_state == 0:
        return None
    needed = check_if_update_needed()
    if needed == 0:
        return None
    if last_disp_content.wifi != disp_content.wifi:
        show_wifi(0,last_disp_content.wifi)
        show_wifi(1,disp_content.wifi)
        last_disp_content.wifi = disp_content.wifi
    if last_disp_content.volume != disp_content.volume:
        show_vol(0,last_disp_content.volume)
        show_vol(1,disp_content.volume)
        last_disp_content.volume = disp_content.volume
    if last_disp_content.tonevalue != disp_content.tonevalue:
        print_bar(disp_content.tonevalue)
        last_disp_content.tonevalue = disp_content.tonevalue
    if last_disp_content.time != disp_content.time:
        show_time(0,last_disp_content.time)
        show_time(1,disp_content.time)
        last_disp_content.time = disp_content.time
    if last_disp_content.app_mode != disp_content.app_mode:
        if last_disp_content.app_mode == "RAD": update_radio_display()
        if last_disp_content.app_mode == "AIR": update_airplay_display(0)
        if last_disp_content.app_mode == "SPOT": update_spotify_display(0)
        if last_disp_content.app_mode == "AUX": update_aux_display(0)
        if last_disp_content.app_mode == "USB": update_usb_display(0)
        if disp_content.app_mode      == "RAD": update_radio_display()
        if disp_content.app_mode      == "AIR": update_airplay_display(1)
        if disp_content.app_mode      == "SPOT": update_spotify_display(1)
        if disp_content.app_mode      == "AUX": update_aux_display(1)
        if disp_content.app_mode      == "USB": update_usb_display(1)
        last_disp_content.app_mode = disp_content.app_mode
    if disp_content.app_mode == "RAD":
        update_radio_display()
    disp.image(image)
    disp.display()

# do special radio stuff
def update_radio_display():
    show_mpd()

# do special airplay stuff
def update_airplay_display(color):
    update_station(0,disp_content.name)
    draw.text((disp_positions.radio_icon_x, disp_positions.big_icon_y), airplay_icon, color, font=icon_font_large)

# do special spotify stuff
def update_spotify_display(color):
    update_station(0,disp_content.name)
    draw.text((disp_positions.radio_icon_x, disp_positions.big_icon_y), spotify_icon, color, font=spot_font)

# do special aux stuff
def update_aux_display(color):
    update_station(0,disp_content.name)
    draw.text((disp_positions.radio_icon_x, disp_positions.big_icon_y), aux_in_icon, color, font=icon_font_large)

# do special usb stuff
def update_usb_display(color):
    update_station(0,disp_content.name)
    draw.text((disp_positions.radio_icon_x, disp_positions.big_icon_y), usb_in_icon, color, font=icon_font_large)

# scroll text if longer that display width
def scroll_text(raw_text,font,y_pos,x_pos,speed,color):
    txt_width, txt_height =  draw.textsize(raw_text, font = font)
    if ( size_x < txt_width ):
        #raw_text = raw_text + " * "
        #txt_width, txt_height =  draw.textsize(raw_text, font = font)
        #x_pos = x_pos - speed
        #if x_pos < -txt_width:
        #    x_pos=0
        x_pos = 0
        draw.text((x_pos,y_pos), raw_text, color, font=font)
        #draw.text((x_pos+txt_width,y_pos), raw_text, 1, font=font)
        #return x_pos
        return 0
    else:
        x_pos = (size_x - txt_width) // 2
        draw.text((x_pos,y_pos), raw_text, color, font=font)
        return 0

# print progress bar 0 - 100
def print_bar(value):
    bar_size = int(value * 123/100) + 2
    draw.rectangle(((0,52),(127,62)), fill=0, outline = 1)
    draw.rectangle(((2,54),(bar_size,60)), fill=1, outline = 0)

# wifi signal display
def show_wifi(color, value):
    if value > 70:
        draw.text((disp_positions.wifi_icon_x,disp_positions.statusbar_pos), wifi_icon_high , color, icon_font_small)
    elif value > 30:
        draw.text((disp_positions.wifi_icon_x,disp_positions.statusbar_pos), wifi_icon_medium , color, icon_font_small)
    elif value <= 30:
        draw.text((disp_positions.wifi_icon_x,disp_positions.statusbar_pos), wifi_icon_low , color, icon_font_small)

# volume icon and bar
def show_vol(color, value):
    if value == 0:
        draw.text((disp_positions.vol_icon_x,disp_positions.statusbar_pos), vol_icon_off , color, icon_font_small)
    elif value > 70:
        draw.text((disp_positions.vol_icon_x,disp_positions.statusbar_pos), vol_icon_high , color, icon_font_small)
    elif value > 30:
        draw.text((disp_positions.vol_icon_x,disp_positions.statusbar_pos), vol_icon_medium , color, icon_font_small)
    elif value <= 30:
        draw.text((disp_positions.vol_icon_x,disp_positions.statusbar_pos), vol_icon_low , color, icon_font_small)

# time display update
def show_time(color, value):
    draw.text((disp_positions.time_text_x,disp_positions.statusbar_txt_pos), value, color, small_font)

# clear Station name
def update_station(color, txt):
    txt_width, txt_height =  draw.textsize(txt, font = medium_font)
    if ( size_x < txt_width ):
        draw.text((0,20), txt, color, font=medium_font)
    else:
        x_pos = (size_x - txt_width) // 2
        draw.text((x_pos,20), txt, color, font=medium_font)

# mpd infos
def show_mpd():
    if disp_content.mpd_stat != last_disp_content.mpd_stat:
        if disp_content.mpd_stat == "play":
            draw.text((disp_positions.play_icon_x,disp_positions.statusbar_pos), pause_icon, 0, icon_font_small)
            draw.text((disp_positions.play_icon_x,disp_positions.statusbar_pos), play_icon, 1, icon_font_small)
            draw.text((disp_positions.radio_icon_x, disp_positions.big_icon_y), radio_icon, 0, font=icon_font_large)
            update_station(1,disp_content.name)
        else:
            draw.text((disp_positions.play_icon_x,disp_positions.statusbar_pos), play_icon, 0, icon_font_small)
            draw.text((disp_positions.play_icon_x,disp_positions.statusbar_pos), pause_icon, 1, icon_font_small)
            update_station(0,last_disp_content.name)
            draw.text((disp_positions.radio_icon_x, disp_positions.big_icon_y), radio_icon, 1, font=icon_font_large)
        last_disp_content.mpd_stat = disp_content.mpd_stat
    if disp_content.mpd_stat == "play":
        if last_disp_content.name != disp_content.name:
            update_station(0,last_disp_content.name)
            update_station(1,disp_content.name)
            last_disp_content.name = disp_content.name
