import json
from Client.Client import Client

# Get the config
f = open ('config.json', 'r')
config = json.load(f)

app_id = config['APP']['APP_ID']
private_key = config['APP']['PRIVATE_KEY']
messenger = config['FROM']['MESSENGER']
viber = config['FROM']['VIBER']
whatsapp = config['FROM']['WHATSAPP']
sms = config['FROM']['SMS']
users = config['USERS']

# useful work
client = Client(app_id, private_key, messenger, viber, whatsapp, sms)
msg = "Server is about to melt!"
for user in users:
    j = client.send_message_with_failover(user, msg)
    if 'dispatch_uuid' in j.keys():
        break
