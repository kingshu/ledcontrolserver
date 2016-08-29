#!/bin/bash

cd ~
sudo pigpiod
sleep 3
python ledcontrolserver/led.py
./ngrok http 8080
sleep 10
python sendNgrokUrl.py
