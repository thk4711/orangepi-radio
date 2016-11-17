#!/usr/bin/env python

import iwlib

wifi_stat = iwlib.iwconfig.get_iwconfig("wlan0")
#display.disp_content.wifi = wifi_stat['stats']['level']
print wifi_stat
