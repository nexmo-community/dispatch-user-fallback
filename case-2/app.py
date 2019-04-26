import json
import requests
import jwt
import time
from uuid import uuid4
from pprint import pprint

debug_mode = True

# Get the config
f = open ('config.json', 'r')
config = json.load(f)

app_id = config['APP']['APP_ID']
private_key = config['APP']['PRIVATE_KEY']

from_messenger = config['FROM']['MESSENGER']
from_viber = config['FROM']['VIBER']
from_whatsapp = config['FROM']['WHATSAPP']
from_sms = config['FROM']['SMS']

users = config['USERS']

msg = "Important message!"

f = open(private_key, 'r')
key = f.read()
f.close()

def set_field_types(channel_type):
    if channel_type == 'messenger':
        from_field = "id"
        to_field = "id"
    elif channel_type == 'whatsapp': 
        from_field = "number"
        to_field = "number"
    elif channel_type == "sms":
        from_field = "number"
        to_field = "number"
    elif channel_type == 'viber_service_msg':
        from_field = "id"
        to_field = "number"
    return (from_field, to_field)

def set_from_channel(channel_type):
    if channel_type == 'messenger':
        from_channel = from_messenger
    elif channel_type == 'whatsapp': 
        from_channel = from_whatsapp
    elif channel_type == "sms":
        from_channel = from_sms
    elif channel_type == 'viber_service_msg':
        from_channel = from_viber
    return from_channel

def build_user_workflow(user):
    
    flow = {}
    flow['template'] = 'failover'
    flow['workflow'] = []

    # pop fail object off end of array - last channel specified is our fallback channel
    channel = user['channels'].pop()
    fail_obj = {'from': {}, 'to': {}, 'message': {'content': {}}}
    
    from_field, to_field = set_field_types(channel['type'])
    from_channel = set_from_channel(channel['type'])
    
    fail_obj['from'][from_field] = from_channel  
    fail_obj['from']['type'] = channel['type']
    fail_obj['to'][to_field] = channel['id_num']
    fail_obj['to']['type'] = channel['type']

    fail_obj['message']['content']['type'] = 'text'
    fail_obj['message']['content']['text'] = "[%s]: %s" % (user['name'], msg)

    for channel in user['channels']:

        obj = {'from': {}, 'to': {}, 'message': {'content': {}}, 'failover': {}}

        from_field, to_field = set_field_types(channel['type'])
        from_channel = set_from_channel(channel['type'])

        obj['from'][from_field] = from_channel  
        obj['from']['type'] = channel['type']
        obj['to'][to_field] = channel['id_num']
        obj['to']['type'] = channel['type']

        obj['message']['content']['type'] = 'text'
        obj['message']['content']['text'] = "[%s]: %s" % (user['name'], msg)

        obj['failover']['expiry_time'] = 600
        obj['failover']['condition_status'] = 'read'    

        flow['workflow'].append(obj)

    flow['workflow'].append(fail_obj)
    return flow


def send_message_with_failover(workflow):

    expiry = 1*60*60 # JWT expires after one hour (default is 15 minutes)

    payload = {
        'application_id': app_id,
        'iat': int(time.time()),
        'jti': str(uuid4()),
        'exp': int(time.time()) + expiry,
    }

    gen_jwt  = jwt.encode(payload, key, algorithm='RS256')
    auth = b'Bearer '+gen_jwt
    headers = {'Authorization': auth, 'Content-Type': 'application/json'}
    r = requests.post('https://api.nexmo.com/v0.1/dispatch', headers=headers, data=workflow)
    j = r.json()
    #pprint(j)
    return j

# Main
for user in users:
    print("User: %s" % user['name'])
    workflow = build_user_workflow(user)
    if debug_mode:
        print(json.dumps(workflow, indent=4, sort_keys=False))
    j = send_message_with_failover(json.dumps(workflow))
    if 'dispatch_uuid' in j.keys():
        print('Message read: terminating...')
        break
    print('Trying next user with failover...')
print('Done')
