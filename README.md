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
            "name": "Fred",
            "channels": [
                {
                    "type": "sms",
                    "id_num": "4470000002"
                },
                {
                    "type": "sms",
                    "id_num": "4470000003"
                }
            ]
        },
        {
            "name": "Michael",
            "channels": [
                {
                    "type": "messenger",
                    "id_num": "123456789"
                },
                {
                    "type": "sms",
                    "id_num": "4470000004"
                },
                {
                    "type": "sms",
                    "id_num": "4470000005"
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

### Notes on use case 2

* User must have at least two channels.
* User can mix any number of channels and types as long as there is at least two channels. For example user could have 3 SMS numbers plus a Messenger ID.
* The last channel specified for a user will be taken to be the final failover channel. 
* Final failover channel does not have to be SMS although it typically will be.
* A workflow is created on a per user basis, but you can specify a workflow for each user.
* An atempt is made to apply a workflow to a user in the order in which they are listed in the configuration file.




