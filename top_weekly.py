import config
import io
import requests
from discord_webhook import DiscordWebhook

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

xp_gained = requests.get(f"https://api.wiseoldman.net/v2/groups/{wom_group_id}/gained?metric=overall&period=week&limit=3").json()
ehb_gained = requests.get(f"https://api.wiseoldman.net/v2/groups/{wom_group_id}/gained?metric=ehb&period=week&limit=3").json()

xp_result = []
ehb_result = []
rank = {1: ":first_place:", 2: ":second_place:", 3: ":third_place:"}

for i, player in enumerate(xp_gained, start=1):
    xp_result.append((player["player"]["displayName"], human_format(player["data"]["gained"]), rank[i]))

for i, player in enumerate(ehb_gained, start=1):
    ehb_result.append((player["player"]["displayName"], human_format(player["data"]["gained"]), rank[i]))
  
response = "\n**XP Champions of the week!**\n\n"
for t in xp_result:
    response += f"{t[2]} **{t[0]}** - XP gained: {t[1]}\n"
response += "\n**Effective Hours Bossed Champions of the week!**\n\n"
for t in ehb_result:
    response += f"{t[2]} **{t[0]}** - EHB gained: {t[1]}\n"
webhook = DiscordWebhook(url=config.discord_webhook, content=response)
r = webhook.execute()
print(r)