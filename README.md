ledcontrolserver
===================


Setup
-------------
**Parts required**

- One strip of RGB LEDs. Any generic one like [this one][amazon_led] will work.
- An appropriate [power supply][power_supply] if it doesn't come with the strip.
- Three N-Channel MOSFET transistors. I used IRLZ34N.
- A [Raspberry Pi][rpi]
- Optional
  * I used a breadboard and connector cables.
  * A USB wifi dongle.

---------

**Setup your raspberry pi**

- Follow [this guide][rpi_setup].
  - I didn't bother with an SD card pre installed with NOOBS, I just straight up installed Raspian using [this guide][rpi_images].
- If you went with the wifi dongle option, [here][rpi_wifi] are the setup instructions.

-------

**Make your connections like so:**

![alt text][circuit]
*The part on the top right is the power supply, or an extension (not necessarily a separate circuit-board part)*

---------

**Software setup**

- Run `sudo apt-get update`
- Install [ngrok][ngrok] on the Raspberry Pi. Use the Linux 32 bit version. 
- Install [PiGPIO][pigpio].
- Install screen using `sudo apt-get install screen`
- Clone this repo into your home directory which will be something like `/home/pi`
    - After cloning, you should get a `/home/pi/ledcontrolserver` directory.
- Edit `/home/pi/ledcontrolserver/led.py`. Change the PIN_RED, PIN_GRN and PIN_BLU variables to match whatever GPIO pins you connected your red, green and blue LED connections to (via the transistors of course) respectively.  

-------

**Running the whole thing**

- Run `sudo pigpiod`
- Run `screen -S ngrok`. In the screen that appears, do the following:
    - Run `./ngrok http 8080` (assuming you put it in your home directory)
    - Note down the Public URL once ngrok establishes the tunnel
    - Press <kbd>Ctrl+A </kbd> and then <kbd> D </kbd> to detach the screen.
- Run `screen -S server`. In the screen that appears , do the following:
    - Run `python /home/pi/ledcontrolserver/led.py`
    - Press <kbd>Ctrl+A </kbd> and then <kbd> D </kbd> to detach the screen.
- You can resume any of your screens using `screen -r ngrok` or `screen -r server` 
- You can now control your LED strip by using to the Public URL from the step above. See the [API section](#API).

-----

**Optional steps**

If your Raspberry Pi gets disconnected or rebooted for any reason or your internet router gets rebooted, you'll have to many of the above steps. To avoid that, I have added some automation. This will run ngrok and the server every time the Raspberry Pi boots and send you the new Public URL by email.

- Move all the files from `/home/pi/ledcontrolserver/other_tools/` to the home directory `/home/pi/`
- Run `sudo crontab -e`
    - Add `@reboot . /home/pi/onstartup.sh` to the end of the file that opens and save.
- Install [mailx][mailx]. 
- Edit the .mailrc file with your GMail details. 
   - If you use 2-factor authentication, use an [app password][gmail] instead.

-------

API
-------

You should have an ngrok Public URL from the above steps that looks something like `http://abcd123.ngrok.com`. Append one of the following endpoints and send a GET request to the full path to that URL to control the LED strip (eg: Go to `http://abcd123.ngrok.com/setstate/255/255/255` in your browser).

Endpoints:

- `/getstate` : Get the current state of the LED strip.
- `/setstate/100/128/234` : Set the color of the LED strip.
    - The 3 numbers are the Red, Green, and Blue intensities.
    - They can range between 0 and 255.
    - Use a [colorpicker tool][colorpicker] for finding out RGB values for colors.
- `/turnoff` :  Turn the LED strip off.
- `/turnon` : Turn the LED strip on.
    - The first time this is run, it will have no effect, because the color is set to black, which is the same as the strip being off. Use /setstate to set some color first before using `/turnon` and `/turnoff`
- `/turnonifdark` : If the strip is off, this turns the LED strip on, only if sunset has occurred and it is before sunrise the next morning. 
    - Edit the file `/home/pi/ledcontrolserver/suncycle.py` to use your latitude and longitude instead for correct sunset and sunrise times.
- `/flicker` : Flickers between colors.
- `/pulse` : Starts 1 slow pulse of color.

--------

[amazon_led]: https://www.amazon.com/SUPERNIGHT-5-Meter-Waterproof-Flexible-Changing/dp/B00ASHQQKI/ref=sr_1_4?ie=UTF8&qid=1472447350&sr=8-4&keywords=rgb+led+strip
[circuit]: https://dl.dropboxusercontent.com/u/33923910/raspi_rgb_led.png 
[rpi]: https://www.raspberrypi.org/products/raspberry-pi-3-model-b/
[power_supply]: https://www.youtube.com/watch?v=bTRLt-fzTwg#t=07m03s
[rpi_setup]: https://www.raspberrypi.org/documentation/setup/
[rpi_images]: https://www.raspberrypi.org/documentation/installation/installing-images/
[rpi_wifi]: https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md
[ngrok]: https://ngrok.com/download
[mailx]: http://www.thelinuxtips.com/2011/09/sending-email-via-gmail-in-linux/
[gmail]: https://support.google.com/accounts/answer/185833?hl=en
[pigpio]: https://www.raspberrypi.org/forums/viewtopic.php?p=486959
[colorpicker]: http://www.colorpicker.com