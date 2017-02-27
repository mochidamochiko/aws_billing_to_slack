#!/usr/bin/env python
# coding: utf-8

from config import *
import slackweb

slack = slackweb.Slack(url=slack_incomming_webhook_url)

slack.notify(
    text="Billing! :moneybag:",
    username="AWS-Billing-Notify",
    icon_emoji=":moneybag:",
    mrkdwn=True
)

