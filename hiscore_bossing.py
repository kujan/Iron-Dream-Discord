import requests
from discord_webhook import DiscordWebhook
import io
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
bosses = data["metricLeaders"]["bosses"]
response = "\n"

for k in bosses:
    boss = data["metricLeaders"]["bosses"][k]["metric"]
    name = data["metricLeaders"]["bosses"][k]["player"]["displayName"]
    kc = data["metricLeaders"]["bosses"][k]["kills"]
    # Any custom formatting goes here
    response += (f"{bosses_map[boss]}: **{name}** | KC: **{kc}**\n")

buf = io.StringIO(response)
response_arr = []
chars = 0
temp = ""
# Discord only allows a maximum of 2000 chars in a webhook message, this splits it up into separate messages
for line in buf.readlines():
    if chars > 1800:
        chars = 0
        response_arr.append(temp)
        temp = "\n"
        
    temp += line
    chars += len(line)
response_arr.append(temp)
for response in response_arr:
    webhook = DiscordWebhook(url=config.discord_webhook, content=response)
    r = webhook.execute()
    print(r)
