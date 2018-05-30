from __future__ import print_function
import os, boto3, json, base64
import urllib.request, urllib.parse
import logging

def decrypt(encrypted_url):
    region = os.environ['AWS_REGION']
    try:
        kms = boto3.client('kms', region_name=region)
        plaintext = kms.decrypt(CiphertextBlob=base64.b64decode(encrypted_url))['Plaintext']
        return plaintext.decode()
    except Exception:
        logging.exception("Failed to decrypt URL with KMS")

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

def notify_slack(message, region):
    slack_url = os.environ['SLACK_WEBHOOK_URL']
    slack_default_channel = os.environ['SLACK_DEFAULT_CHANNEL']
    slack_user = os.environ['SLACK_USERNAME']

    if not slack_url.startswith("http"):
        slack_url = decrypt(slack_url)

    payload = build_slack_payload(slack_default_channel, slack_user, message)

    data = urllib.parse.urlencode({"payload": json.dumps(payload)}).encode("utf-8")
    req = urllib.request.Request(slack_url)
    urllib.request.urlopen(req, data)

def lambda_handler(event, context):
    message = json.loads(event['Records'][0]['Sns']['Message'])
    region = event['Records'][0]['Sns']['TopicArn'].split(":")[3]
    logging.debug("message: %s" %message)
    notify_slack(message, region)

    return message
