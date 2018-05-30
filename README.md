# terraform-aws-lambda-notify-slack

This module creates an AWS Lambda function that consumes messages from an SNS queue and sends them  as notifications to Slack using the incoming webhooks API. The SNS queue can be provided, or created by this module.

## Module Usage

```
module "notify_slack" {
    source = "git::git@github.com:sagansystems/terraform-aws-lambda-notify-slack.git"

    sns_topic_name = "slack-topic"

    slack_webhook_url = "https://hooks.slack.com/services/AAA/BBB/CCC"
    slack_channel     = "aws-notification"
    slack_username    = "reporter"
}
```

## SNS Payload

The SNS payload must be a valid slack JSON payload. See https://api.slack.com/docs/messages

Example payload:

```json
{
    "text": "My Slack Message",
    "attachments": [
        {
            "text": "Optional text that appears within the attachment",
            "fields": [
                {
                    "title": "Priority",
                    "value": "High",
                    "short": false
                }
            ],
        }
    ]
}
```

## References

Based on the official terraform module: https://github.com/terraform-aws-modules/terraform-aws-notify-slack