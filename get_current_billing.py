#!/usr/bin/env python
# coding: utf-8

import boto3
import pprint
import datetime

pp = pprint.PrettyPrinter(indent=4)

cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')

# list_metrics = cloudwatch.list_metrics()
response = cloudwatch.get_metric_statistics(
    Namespace = 'AWS/Billing',
    MetricName = 'EstimatedCharges',
    Dimensions = [
        {
            "Name": "Currency",
            "Value": "USD"
        }
    ],
    # StartTime = datetime.datetime.utcnow() - datetime.timedelta(seconds=3600),
    StartTime = datetime.datetime.utcnow() - datetime.timedelta(hours = 4),
    EndTime = datetime.datetime.utcnow(),
    Period = 3600,
    Statistics = ['Maximum']
)

pp.pprint(response)

# pp.pprint(list_metrics)