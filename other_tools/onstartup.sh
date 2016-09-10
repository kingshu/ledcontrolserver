#!/bin/bash

cd ~
echo "Initializing pigpiod"
sudo pigpiod
sleep 3
echo "Starting server screen"
screen -S "server" -d -m "./startServer.sh"
sleep 5
echo "Starting ngrok"
screen -S "ngrok" -d -m "./runngrok.sh"
sleep 10
echo "Sending URL via email"
python sendNgrokUrl.py
