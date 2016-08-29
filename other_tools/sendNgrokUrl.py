import requests
import json
import os

r = requests.get("http://localhost:4040/api/tunnels")
resp = json.loads(r.content)
tunnels = resp["tunnels"]
subject = "New ngrok URL"
message = tunnels[0]["public_url"]+" is your new ngrok tunnel forwarding URL. The raspberry pi was rebooted."
bashCommand = 'echo "'+message+'" | mailx -v -A gmail -s "'+subject+'" example@gmail.com'
os.system(bashCommand)