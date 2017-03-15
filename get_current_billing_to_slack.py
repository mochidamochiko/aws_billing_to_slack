#!/usr/bin/env python
# coding: utf-8

import boto3
from boto3.session import Session
import datetime

import slackweb
from config import *

session = Session(region_name='us-east-1', profile_name='default')
cloudwatch = session.client ('cloudwatch')

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
metrics_date = response['Datapoints'][0]['Timestamp']
metrics_date_str = metrics_date.strftime('%Y/%m/%d %H:%M:%S (UTC)')

slack = slackweb.Slack(url=slack_incomming_webhook_url)

slack.notify(
    text="*account-name* : $" + str(bill) + " at " + metrics_date_str + " :moneybag:",
    username="AWS-Billing-Notify",
    icon_emoji=":moneybag:",
    mrkdwn=True
)
