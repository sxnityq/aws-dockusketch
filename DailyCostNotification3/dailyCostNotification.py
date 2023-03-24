from datetime import datetime, timedelta

import boto3


region = "us-east-1"


class DailyCostNotification:
    
    def __init__(self):
        self.client = boto3.client("cloudwatch", region_name=region)
        

    def get_billing_dp(self, end_time : datetime, start_time : datetime, period=2400):
        response = self.client.get_metric_statistics(
            Namespace='AWS/Billing',
            MetricName='EstimatedCharges',
            Dimensions=[
                {
                    'Name': 'Currency',
                    'Value': 'USD'
                },
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=period,
            Statistics=[
                'Average',
            ]
        )
        return response


class BillingDays:
    
    @staticmethod
    def get_prev_month_first_day(): 
        today = datetime.now()
        if today.month == 1:
            return datetime(year=today.year - 1, month=12, day=1)
        return datetime(year=today.year, month=today.month - 1, day=1)

    @staticmethod
    def get_prev_month_last_day():
        today = datetime.now()
        cur_month_first_day = datetime(year=today.year, month=today.month, day=1) 
        return cur_month_first_day - timedelta(days=1)
    
    @staticmethod
    def get_cur_month_first_day():
        today = datetime.now()
        return datetime(year=today.year, month=today.month, day=1)

    @staticmethod
    def get_cur_month_last_day():
        today = datetime.now()
        if today.month == 12:
            return datetime(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        return datetime(year=today.year, month=today.month + 1, day=1) - timedelta(days=1)


DCN = DailyCostNotification()

if __name__ == "__main__":
    for k in DCN.get_billing_dp().get("Datapoints"):
        print(k)
