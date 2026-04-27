import requests
from django.conf import settings

def send_sms(phone,message):

    url="https://www.fast2sms.com/dev/bulkV2"

    payload={
        "sender_id":"JEWELS",
        "message":message,
        "language":"english",
        "route":"q",
        "numbers":phone
    }

    headers={
        "authorization":settings.FAST2SMS_API_KEY
    }

    requests.post(url,data=payload,headers=headers)