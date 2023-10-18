from PIL import Image, ImageDraw, ImageFont
import requests
from discord_webhook import DiscordWebhook
import config


wom_group_id = config.wom_group_id
discord_webhook = config.discord_webhook

# Used to rename bosses for proper display in webhook
bosses_map = {"abyssal_sire": "Abyssal Sire", "alchemical_hydra": "Alchemical Hydra", "artio": "Artio", "barrows_chests": "Barrows",
              "bryophyta": "Bryophyta", "callisto": "Callisto", "calvarion": "Calvar'ion", "cerberus": "Cerberus", "chambers_of_xeric": "CoX",
              "chambers_of_xeric_challenge_mode": "CoX CM", "chaos_elemental": "Chaos Elemental", "chaos_fanatic": "Chaos Fanatic",
              "commander_zilyana": "Commander Zilyana", "corporeal_beast": "Corporeal Beast", "crazy_archaeologist": "Crazy Archaeologist",
              "dagannoth_prime": "Dagannoth Prime", "dagannoth_rex": "Dagannoth Rex", "dagannoth_supreme": "Dagannoth Supreme", 
              "deranged_archaeologist": "Deranged Archaeologist", "duke_sucellus": "Duke Sucellus", "general_graardor": "General Graardor",
              "giant_mole": "Giant Mole", "grotesque_guardians": "Grotesque Guardians", "hespori": "Hespori", "kalphite_queen": "Kalphite Queen",
              "king_black_dragon": "King Black Dragon", "kraken": "Kraken", "kreearra": "Kree'Arra", "kril_tsutsaroth": "Kril'Tsutsaroth", 
              "mimic": "Mimic", "nex": "Nex", "nightmare": "Nightmare", "phosanis_nightmare": "Phosanis Nightmare", "obor": "Obor", 
              "phantom_muspah": "Phantom Muspah", "sarachnis": "Sarachnis", "scorpia": "Scorpia", "skotizo": "Skotizo", "spindel": "Spindel",
              "tempoross": "Tempoross", "the_gauntlet": "The Gauntlet", "the_corrupted_gauntlet": "Red Prison", "the_leviathan": "The Leviathan", "the_whisperer": "The Whisperer",
              "theatre_of_blood": "ToB", "theatre_of_blood_hard_mode": "ToB HM", "thermonuclear_smoke_devil": "Termonuclear Smoke Devil", 
              "tombs_of_amascut": "ToA Normal", "tombs_of_amascut_expert": "ToA Expert", "tzkal_zuk": "Zuk", "tztok_jad": "Jad", "vardorvis": "Vardorvis",
              "venenatis": "Venenatis", "vetion": "Vet'ion", "vorkath": "Vorkath", "wintertodt": "Wintertodt", "zalcano": "Zalcano", "zulrah": "Zulrah"}

r = requests.get(f"https://api.wiseoldman.net/v2/groups/{wom_group_id}/statistics", headers={'Accept': 'application/json'})
data = r.json()
print(data)
group_details = requests.get(f"https://api.wiseoldman.net/v2/groups/{wom_group_id}/", headers={'Accept': 'application/json'}).json()
bosses = data["metricLeaders"]["bosses"]

data_dict = {}
for k in bosses:
    boss = data["metricLeaders"]["bosses"][k]["metric"]
    name = data["metricLeaders"]["bosses"][k]["player"]["displayName"]
    kc = data["metricLeaders"]["bosses"][k]["kills"]
    data_dict[boss] = {}
    data_dict[boss]["name"] = name
    data_dict[boss]["kc"] = data["metricLeaders"]["bosses"][k]["kills"]
    role = ""
    # Any custom formatting goes here
    for player in group_details["memberships"]:
        if data_dict[boss]["name"] in player["player"]["displayName"]:
            data_dict[boss]["role"] = player["role"]

fnt = ImageFont.truetype("/usr/share/fonts/droid/DroidSansMono.ttf", 17)
img = Image.open("bg.png").convert("RGBA")
draw = ImageDraw.Draw(img)
x_pos = 50
y_pos = 100
print(data_dict)
headers = f"{'Boss':<28} {'Player Name':<20} {'Kill Count':>10}"
draw.text((x_pos, y_pos), headers, font=fnt, fill = (255, 255, 255, 255), stroke_width=1)
y_pos += 40
for i, k in enumerate(data_dict.keys()):
    print(k)
    #print(line)
    boss_img = Image.open(f"images/{k}.png").convert("RGBA")
    role_img = Image.open(f"images/{data_dict[k]['role']}.png").convert("RGBA")
    img.paste(role_img, (x_pos +282, y_pos + 3), role_img)
    img.paste(boss_img, (x_pos - 22, y_pos + 1), boss_img)
    text = f"{bosses_map[k]:<28} {data_dict[k]['name']:<20} {data_dict[k]['kc']:<10}\n"
    if i % 2:
        draw.text((x_pos, y_pos), text, font=fnt, fill = (255, 255, 255, 255))
    else:
        draw.text((x_pos, y_pos), text, font=fnt, fill = (150, 150, 150, 255))
    y_pos += 20

img.save("output.png")
webhook = DiscordWebhook(url=discord_webhook)
with open("output.png", "rb") as f:
    webhook.add_file(file=f.read(), filename="hiscore.png")
    response = webhook.execute()
print(response)