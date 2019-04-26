import jwt # https://github.com/jpadilla/pyjwt -- pip3 install PyJWT
import time
import json
import requests
from uuid import uuid4
from pprint import pprint

debug_mode = True

class Client:

    expiry = 1*60*60 # JWT expires after one hour (default is 15 minutes)
    from_messenger = ""
    from_viber = ""
    from_whatsapp = ""
    from_sms = ""

    def __init__(self, app_id, filename, messenger, viber, whatsapp, sms):
        
        f = open(filename, 'r')
        self.private_key = f.read()
        f.close()

        self.app_id = app_id
        self.from_messenger = messenger
        self.from_viber = viber
        self.from_whatsapp = whatsapp
        self.from_sms = sms
        
        return

    def build_data_body(self, user, msg):

        pri_channel_type = user['primary']['type']
        sec_channel_type = user['secondary']['type']

        if debug_mode:
            print("** debug ** Primary --> [%s]: type: %s id_num: %s" % (user['name'], user['primary']['type'], user['primary']['id_num']))
            print("** debug ** Secondary --> [%s]: type: %s id_num: %s" % (user['name'], user['secondary']['type'], user['secondary']['id_num']))

        if pri_channel_type == 'messenger':
            pri_from_field = "id"
            pri_to_field = "id"
            pri_from_id_num = self.from_messenger
        elif pri_channel_type == 'whatsapp': 
            pri_from_field = "number"
            pri_to_field = "number"
            pri_from_id_num = self.from_whatsapp
        elif pri_channel_type == "sms":
            pri_from_field = "number"
            pri_to_field = "number"
            pri_from_id_num = self.from_sms            
        elif pri_channel_type == 'viber_service_msg':
            pri_from_field = "id"
            pri_to_field = "number"
            pri_from_id_num = self.from_viber
               
        if sec_channel_type == 'messenger':
            sec_from_field = "id"
            sec_to_field = "id"
            sec_from_id_num = self.from_messenger
        elif sec_channel_type == 'whatsapp': 
            sec_from_field = "number"
            sec_to_field = "number"
            sec_from_id_num = self.from_whatsapp
        elif sec_channel_type == "sms":
            sec_from_field = "number"
            sec_to_field = "number"
            sec_from_id_num = self.from_sms            
        elif sec_channel_type == 'viber_service_msg':
            sec_from_field = "id"
            sec_to_field = "number"
            sec_from_id_num = self.from_viber

        msg = "[%s]: %s" % (user['name'], msg)
            
        data_body = json.dumps({
            "template":"failover",
            "workflow": [
                {
                    "from": { "type": pri_channel_type, pri_from_field: pri_from_id_num },
                    "to": { "type": pri_channel_type, pri_to_field: user['primary']['id_num'] },
                    "message": {
                        "content": {
                            "type": "text",
                            "text": msg
                        }
                    },
                    "failover": {
                        "expiry_time": 600,
                        "condition_status": "read"
                    }
                },
                {
                    "from": { "type": sec_channel_type, sec_from_field: sec_from_id_num},
                    "to": { "type": sec_channel_type, sec_to_field: user['secondary']['id_num']},
                    "message": {
                        "content": {
                            "type": "text",
                            "text": msg
                        }
                    }
                }
            ]})        
        
        return data_body

    def send_message_with_failover(self, user, msg):

        data_body = self.build_data_body(user, msg)

        self.payload = {
            'application_id': self.app_id,
            'iat': int(time.time()),
            'jti': str(uuid4()),
            'exp': int(time.time()) + self.expiry,
        }

        gen_jwt  = jwt.encode(self.payload, self.private_key, algorithm='RS256')
        auth = b'Bearer '+gen_jwt
        headers = {'Authorization': auth, 'Content-Type': 'application/json'}
        r = requests.post('https://api.nexmo.com/v0.1/dispatch', headers=headers, data=data_body)
        j = r.json()
        pprint(j)
        return j
