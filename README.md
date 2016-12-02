# orangepi-radio
Streaming Client with AirPlay Spotify Connect and Internet Radio based on Orange Pi Lite

![Streamin_Client_with_Speaker](https://github.com/thk4711/orangepi-radio/blob/master/images/Front.jpg)

Half a year ago I built a streaming client based an a Raspberry Pi ( https://github.com/thk4711/raspiradio ). This device is working very well. But I had the feeling that is might be too much effort and cost for most people to built one.

So I was thinking - how could one built a device at the lowest possible cost and without the need for custom circuit boards but still preserve an acceptable sound quality.

The features are:
- WIFI
- Remote controllable
- Controls on the device itself
- Status display
- Volume control
- Internet radio, AirPlay and Spotify Connect
- Low power consumption

After searching for some time I came to the conclusion that the best basis for such a device would be not a Raspberry PI it is an Orange Pi Lite. This device does have WIFI and an infrared receiver on board as well as I2C/SPI, I2S audio and several GPIO's. You can get it including shipping for about 15$. An alternative would be the Raspberry Pi Zero. It is 5$ but you need an additional WIFI adapter, an OTG USB adapter, cables and an infrared receiver. So including shipping you will need at least the same amount of money but you get a less powerful device and the setup looks not very nice if you think about the cables between all the components.

The downside is clearly that there is a lot more and much better documentation on the internet for the Raspberry PI. But since I knew what I was looking for (because I built such a device already with a Raspberry PI) I got everything working. And at the end I have to say it works as well as on the raspberry.

So basically everything you need does cost less that 50$. Or if you want to connect it to active speakers or to an amplifier you do not need the power amplifier board and it will be less that 40$.

Please see the [WIKI](https://github.com/thk4711/orangepi-radio/wiki) for details.
