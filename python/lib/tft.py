#!/usr/local/bin/python
#!/usr/bin/env python

import pygame
from   pygame.locals import *
import os
import re

pygame.font.init()

if os.path.exists("/sys/class/graphics/fb1/virtual_size"):
    with open('/sys/class/graphics/fb1/virtual_size') as file:
        lines = file.readlines()
    lines[0] = lines[0].strip()
    parts = re.split(',', lines[0])
    size_x = int(parts[0])
    size_y = int(parts[1])
    print("found screen: " + str(size_x) + "x" + str(size_y))
    os.environ["SDL_FBDEV"] = "/dev/fb1"
    test_mode = False

else:
    print("running in test mode ...")
    size_x = 320
    size_y = 240
    test_mode = True

screen = pygame.display.set_mode((size_x,size_y))
pygame.init()
pygame.mouse.set_visible(False)


# define colors
white      = (255,255,255)
black      = (0,0,0)
light_gray = (200,200,200)
dark_gray  = (100,100,100)
red        = (255,0,0)

# define fonts
small_font      = pygame.font.Font("fonts/NotoSans-Regular.ttf", int(size_y/9.14))
small_font_bold = pygame.font.Font("fonts/NotoSans-Bold.ttf", int(size_y/9.14))
medium_font     = pygame.font.Font("fonts/NotoSans-Regular.ttf", int(size_y/7.8))
large_font      = pygame.font.Font("fonts/NotoSans-Regular.ttf", int(size_y/5.33))
bold_font       = pygame.font.Font("fonts/NotoSans-Bold.ttf", int(size_y/7.8))
icon_font_small = pygame.font.Font("fonts/Material-Design-Iconic-Font.ttf", int(size_y/8))
icon_font_large = pygame.font.Font("fonts/Material-Design-Iconic-Font.ttf", int(size_y/2.8))
spot_font       = pygame.font.Font("fonts/socialicious.ttf", int(size_y/2.8))

# render icons
wifi_icon_high   = icon_font_small.render(u'\uf2e8',True,black)
wifi_icon_medium = icon_font_small.render(u'\uf2e2',True,black)
wifi_icon_low    = icon_font_small.render(u'\uf2e7',True,red)
vol_icon_high    = icon_font_small.render(u'\uf3bc',True,black)
vol_icon_medium  = icon_font_small.render(u'\uf3b9',True,black)
vol_icon_low     = icon_font_small.render(u'\uf3ba',True,black)
vol_icon_off     = icon_font_small.render(u'\uf3bb',True,red)
play_icon        = icon_font_small.render(u'\uf3aa',True,black)
pause_icon       = icon_font_small.render(u'\uf3a7',True,red)
radio_icon       = icon_font_large.render(u'\uf2c2',True,black)
airplay_icon     = icon_font_large.render(u'\uf3d2',True,black)
spotify_icon     = spot_font.render(u'\u0051',True,black)
aux_in_icon      = icon_font_large.render(u'\uf29f',True,black)
usb_in_icon      = icon_font_large.render(u'\uf2dd',True,black)
bluetooth_icon   = icon_font_large.render(u'\uf282',True,black)
tone_icon        = icon_font_large.render(u'\uf10f',True,black)


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

# remember last position of scrolled text
class scroll_pos:
    name   = 0
    artist = 0
    title  = 0

# relative positions of objects on the screen
class disp_positions:
    statusbar_pos       = size_y//7.27
    wifi_icon_x         = int(size_x/1.3)
    wifi_text_x         = int(size_x/1.13)
    vol_icon_x          = int(size_x/40)
    time_text_x         = int(size_x/2.46)
    play_icon_x         = int(size_x/8)
    name_y              = int(size_y/4)
    artist_y            = int(size_y/2.7)
    title_y             = int(size_y/2.1)
    radio_icon_x        = int(size_x/2.91)
    tone_icon_x         = int(size_x/5)
    big_icon_y          = int(size_y/3.5)
    tone_text_x         = int(size_x/2.3)
    tone_text_y         = int(size_y/2.3)
    current_tone_text_x = int(size_x/5)

#-----------------------------------------------------------------#
#  update display                                                 #
#-----------------------------------------------------------------#
def update_display(now):
    screen.fill(white)
    show_wifi()
    show_vol()
    show_time()
    if disp_content.app_mode == "RAD": update_radio_display()
    if disp_content.app_mode == "AIR": update_airplay_display()
    if disp_content.app_mode == "SPOT": update_spotify_display()
    if disp_content.app_mode == "AUX": update_aux_display()
    if disp_content.app_mode == "USB": update_usb_display()
    pygame.display.update()

# do special radio stuff
def update_radio_display():
    show_mpd()

# do special airplay stuff
def update_airplay_display():
    screen.blit(airplay_icon,(disp_positions.radio_icon_x,disp_positions.big_icon_y))

# do special spotify stuff
def update_spotify_display():
    screen.blit(spotify_icon,(disp_positions.radio_icon_x,disp_positions.big_icon_y))

# do special aux stuff
def update_aux_display():
    screen.blit(aux_in_icon,(disp_positions.radio_icon_x,disp_positions.big_icon_y))

# do special usb stuff
def update_usb_display():
    screen.blit(usb_in_icon,(disp_positions.radio_icon_x,disp_positions.big_icon_y))

# scroll text if longer that display width
def scroll_text(raw_text,font,y_pos,x_pos,speed):
    text = font.render(raw_text, True, black)
    if ( size_x < text.get_width() ):
        text = font.render(raw_text + " * ", True, black)
        x_pos = x_pos - speed
        if x_pos < -text.get_width():
            x_pos=0
        screen.blit(text,(x_pos,y_pos))
        screen.blit(text, (x_pos+text.get_width(),y_pos))
        return x_pos
    else:
        text = font.render(raw_text, True, black)
        x_pos = (size_x - text.get_width()) // 2
        screen.blit(text,(x_pos,y_pos))
        return 0

# print progress bar 0 - 100
def print_bar(value):
    bar_width = int(value * size_x/1.14/100)
    x_start   = int(size_x/16)
    y_start   = int(size_y/1.5)
    x_width   = int(size_x/1.14)
    y_width   = int(size_y/12.8)
    pygame.draw.rect(screen, black, (x_start - 2, y_start - 2, x_width + 4, y_width + 4))
    pygame.draw.rect(screen, light_gray, (x_start, y_start, x_width, y_width))
    pygame.draw.rect(screen, dark_gray, (x_start, y_start, bar_width, y_width))

# wifi signal display
def show_wifi():
    if disp_content.wifi > 70:
        screen.blit(wifi_icon_high,(disp_positions.wifi_icon_x,disp_positions.statusbar_pos))
    elif disp_content.wifi > 30:
        screen.blit(wifi_icon_medium,(disp_positions.wifi_icon_x,disp_positions.statusbar_pos))
    elif disp_content.wifi <= 30:
        screen.blit(wifi_icon_low,(disp_positions.wifi_icon_x,disp_positions.statusbar_pos))
    wifi_text = small_font.render(str(disp_content.wifi), True, black)
    screen.blit(wifi_text,(disp_positions.wifi_text_x,disp_positions.statusbar_pos))

# volume icon and bar
def show_vol():
    if disp_content.volume == 0:
        screen.blit(vol_icon_off,(disp_positions.vol_icon_x,disp_positions.statusbar_pos))
    elif disp_content.volume > 70:
        screen.blit(vol_icon_high,(disp_positions.vol_icon_x,disp_positions.statusbar_pos))
    elif disp_content.volume > 30:
        screen.blit(vol_icon_medium,(disp_positions.vol_icon_x,disp_positions.statusbar_pos))
    elif disp_content.volume <= 30:
        screen.blit(vol_icon_low,(disp_positions.vol_icon_x,disp_positions.statusbar_pos))
    print_bar(disp_content.tonevalue)
    current_tone_text = small_font.render(disp_content.tonemode, True, black)
    screen.blit(current_tone_text,(disp_positions.current_tone_text_x,disp_positions.statusbar_pos))

# time display update
def show_time():
    time_text = small_font_bold.render(disp_content.time, True, black)
    screen.blit(time_text,(disp_positions.time_text_x,disp_positions.statusbar_pos))

# mpd infos
def show_mpd():
    if disp_content.mpd_stat == "play":
        screen.blit(play_icon,(disp_positions.play_icon_x,disp_positions.statusbar_pos))
        scroll_pos.name   = scroll_text(disp_content.name,medium_font,disp_positions.name_y,scroll_pos.name,1)
        scroll_pos.artist = scroll_text(disp_content.artist,medium_font,disp_positions.artist_y,scroll_pos.artist,1)
        scroll_pos.title  = scroll_text(disp_content.title,bold_font,disp_positions.title_y,scroll_pos.title,2)
    else:
        screen.blit(pause_icon,(disp_positions.play_icon_x,disp_positions.statusbar_pos))
        screen.blit(radio_icon,(disp_positions.radio_icon_x,disp_positions.big_icon_y))
