#!/usr/bin/env python
# coding: utf-8

import boto3
from boto3.session import Session
import datetime
import dateutil

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

# 月初と月末の生成
start_of_month = datetime.datetime(metrics_date.year, metrics_date.month, 1, 0, 0, tzinfo=dateutil.tz.tzutc())
end_of_month = datetime.datetime(metrics_date.year, metrics_date.month + 1, 1, 0, 0, tzinfo=dateutil.tz.tzutc())
days_of_month = end_of_month - start_of_month
days_of_metrics_date = metrics_date - start_of_month

# 1日分の課金
bill_per_day = bill / days_of_metrics_date.days

# 月末予想
predict_monthly_bill = bill_per_day * days_of_month.days


slack = slackweb.Slack(url=slack_incomming_webhook_url)

slack.notify(
    text="*account-name* : $" + str(bill) + " at " + metrics_date_str + ", end-of-month forcast : $" + str(round(predict_monthly_bill,2)) + " :moneybag:",
    username="AWS-Billing-Notify",
    icon_emoji=":moneybag:",
    mrkdwn=True
)
