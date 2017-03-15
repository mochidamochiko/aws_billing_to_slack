#!/usr/bin/env python
# coding: utf-8

import boto3
import pprint
#from datetime import datetime, date, timedelta
import datetime
import dateutil

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

bill = response['Datapoints'][0]['Maximum']
metrics_date = response['Datapoints'][0]['Timestamp']
metrics_date_str = metrics_date.strftime('%Y/%m/%d %H:%M:%S (UTC)')
pp.pprint(bill)
pp.pprint(metrics_date)
pp.pprint(metrics_date_str)

# 月初
start_of_month = datetime.datetime(metrics_date.year, metrics_date.month, 1, 0, 0, tzinfo=dateutil.tz.tzutc())
pp.pprint(start_of_month)

# 月末(というか来月頭)
end_of_month = datetime.datetime(metrics_date.year, metrics_date.month + 1, 1, 0, 0, tzinfo=dateutil.tz.tzutc())
#end_of_month = start_of_month + datetime.timedelta(month = 1)
pp.pprint(end_of_month)

# 今月が何日間か
days_of_month = end_of_month - start_of_month
pp.pprint(days_of_month)
pp.pprint(days_of_month.days)

# 今が月初から何日間か
days_of_metrics_date = metrics_date - start_of_month
pp.pprint(days_of_metrics_date)
pp.pprint(days_of_metrics_date.days)
pp.pprint(days_of_metrics_date.total_seconds()/3600/24)

# 1日分の課金
bill_per_day = bill / days_of_metrics_date.days
pp.pprint(bill_per_day)

# 月末予想
predict_monthly_bill = bill_per_day * days_of_month.days
pp.pprint(predict_monthly_bill)
