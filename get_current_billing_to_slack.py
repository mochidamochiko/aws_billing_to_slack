#!/usr/bin/env python
# coding: utf-8

import boto3
import datetime

import slackweb
from config import *

cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')

response = cloudwatch.get_metric_statistics(
    Namespace = 'AWS/Billing',
    MetricName = 'EstimatedCharges',
    Dimensions = [
        {
            "Name": "Currency",
            "Value": "USD"
        }
    ],
    StartTime = datetime.datetime.utcnow() - datetime.timedelta(hours = 4),
    EndTime = datetime.datetime.utcnow(),
    Period = 3600,
    Statistics = ['Maximum']
)

bill = response['Datapoints'][0]['Maximum']
date = response['Datapoints'][0]['Timestamp'].strftime('%Y/%m/%d %H:%M:%S (UTC)')

slack = slackweb.Slack(url=slack_incomming_webhook_url)

slack.notify(
    text="*mochiko-2015* : $" + str(bill) + " at " + date + " :moneybag:",
    username="AWS-Billing-Notify",
    icon_emoji=":moneybag:",
    mrkdwn=True
)
