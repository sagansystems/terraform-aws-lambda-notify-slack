import os, json
import urllib.request, urllib.parse
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def build_slack_payload(slack_default_channel, slack_username, message):
    payload = {
        "channel": slack_default_channel,
        "username": slack_username,
        "text": message['text'],
        "attachments": []
    }

    if 'channel' in message:
        payload["channel"] = message['channel']
        
    if 'attachments' in message:
        payload["attachments"] = message['attachments']
    
    return payload

def notify_slack(slack_url, slack_default_channel, slack_user, message):
    payload = build_slack_payload(slack_default_channel, slack_user, message)

    data = urllib.parse.urlencode({"payload": json.dumps(payload)}).encode("utf-8")
    req = urllib.request.Request(slack_url)
    urllib.request.urlopen(req, data)

def lambda_handler(event, context):
    message = json.loads(event['Records'][0]['Sns']['Message'])
    logger.debug("message: %s" %message)

    slack_default_channel = os.environ['SLACK_DEFAULT_CHANNEL']
    slack_user = os.environ['SLACK_USERNAME']
    slack_url = os.environ['SLACK_WEBHOOK_URL']

    notify_slack(slack_url, slack_default_channel, slack_user, message)

    return message
