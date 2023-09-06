import config
import requests

code = config.wom_verification_code
group_id = config.wom_group_id
myobj = {"verificationCode": code}
r = requests.post(f"https://api.wiseoldman.net/v2/groups/{group_id}/update-all", data = myobj)
print(r.text)
