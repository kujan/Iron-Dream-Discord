import config
from discord_webhook import DiscordWebhook
import requests
import time
import io
from datetime import date

wom_group_id = config.wom_group_id
discord_webhook = config.discord_webhook

def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

def response_split(response):
    buf = io.StringIO(response)
    response_list = []
    temp = "```"
    for line in buf.readlines():
        if len(temp) + len(line) >= 1995:
            response_list.append(temp + "```")
            temp = "```"
            
        temp += line
    response_list.append(temp + "```")
    return response_list


payload = []
offset = 0
while len(payload) < 50:
    r = requests.get(f"https://api.wiseoldman.net/v2/groups/{wom_group_id}/hiscores?metric=overall&limit=50&offset={offset}", headers={'Accept': 'application/json'})
    data = r.json()
    for player in data:
        if player["player"]["type"] == "ironman" and len(payload) < 50:
            name = player["player"]["displayName"]
            level = player["data"]["level"]
            xp = player["data"]["experience"]
            player_list = [name, level, human_format(xp)]
            if player_list not in payload:
                payload.append(player_list)
    offset += 50
    time.sleep(1)
payload.sort(key = lambda x: x[1], reverse=True)

response = f"\nIron Dream Overall Hiscores (Top 50 - iron only): {date.today().strftime('%d/%m/%Y')}\n"
for i, e in enumerate(payload, start=1):
    name = e[0]
    level = e[1]
    xp = e[2]
    placement = str(i) + "."
    response += f"{placement:<3} {name:<12} {xp:^12} Total:{level:>5}\n"

response_list = response_split(response)
for response in response_list:
    webhook = DiscordWebhook(url=config.discord_webhook, content=response)
    r = webhook.execute()
    print(r)