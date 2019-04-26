# User-based fallback using the Dispatch API

The use case is to fallback on a per-user basis. For example:

1. Michael. If message not read then...
2. Tony. If message not read then...
3. Phil.

## Case 1

Could also have a version where you specify multiple channels per user:

1. Michael on primary channel. If message not read then...
2. Michael on secondary channel. If this fails then...
3. Tony on primary channel. If message not read then...
4. Tony on secondary channel. If this fails then...
5. Phil on primary channel. If message not read then...
6. Phil on secondary channel.

## Case 2

Users can have varying types and numbers of channels:

``` json
{
    "APP": {
        "APP_ID": "d640eb4c-8238-42d0-a03a-123...",
        "PRIVATE_KEY": "private.key"
    },
    "FROM": {
        "MESSENGER": "Messenger ID",
        "VIBER": "YOUR VIBER ID",
        "WHATSAPP": "Your whatsapp number",
        "SMS": "ACMEINC"
    },
    "USERS": [
        {
            "name": "Michael",
            "channels": [
                {
                    "type": "messenger",
                    "id_num": "123456789"
                },
                {
                    "type": "sms",
                    "id_num": "4470000002"
                }
            ]
        },
        {
            "name": "Tony",
            "channels": [
                {
                    "type": "viber",
                    "id_num": "4470000001"
                },
                {
                    "type": "whatsapp",
                    "id_num": "4470000001"
                },
                {
                    "type": "sms",
                    "id_num": "4470000001"
                }
            ]
        }
    ]
}
```

