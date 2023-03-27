import json
from datetime import datetime, timedelta
import os

import requests
from dotenv import load_dotenv

from dailyCostNotification import DCN, BillingDays
from utils import MyJsonEncoder


load_dotenv()
myEncoder = MyJsonEncoder()
today = datetime.now()
yesterday = today - timedelta(days=1)
billing_data = BillingDays()

def collect_prev_month_bills() -> int:
        
    month_bill = [dp.get('Average') for dp in DCN.get_billing_dp(start_time=billing_data.get_prev_month_first_day(),
                                end_time=billing_data.get_prev_month_last_day(),
                                period=3600).get("Datapoints")]
        
    return 0.0 if not month_bill else max(month_bill)

def collect_current_month_bills() -> int:
  
    month_bill = [dp.get('Average') for dp in DCN.get_billing_dp(start_time=billing_data.get_cur_month_first_day(),
                                end_time=billing_data.get_cur_month_last_day(),
                                period=3600).get("Datapoints")]

    return 0.0 if not month_bill else max(month_bill)

def get_todays_bills() -> int:
    
    today_billing = [dp.get('Average') for dp in DCN.get_billing_dp(start_time=datetime(today.year, today.month, today.day),
                                end_time=today,
                                period=3600).get("Datapoints")]
    if not today_billing:
        today_billing = 0.0
    else:
        today_billing = max(today_billing)
    
    yesterday_billing = [dp.get('Average') for dp in DCN.get_billing_dp(start_time=datetime(yesterday.year, yesterday.month, yesterday.day),
                                end_time=datetime(today.year, today.month, today.day),
                                period=3600).get("Datapoints")]
    
    if not yesterday_billing:
        yesterday_billing = 0.0
    else:
        yesterday_billing = max(yesterday_billing)
        
    return today_billing if yesterday_billing > today_billing else round(today_billing - yesterday_billing, 2)

def get_yesterday_bills() -> int:
    
    yesterday_billing = [dp.get('Average') for dp in DCN.get_billing_dp(start_time=datetime(yesterday.year, yesterday.month, yesterday.day),
                                end_time=datetime(today.year, today.month, today.day),
                                period=3600).get("Datapoints")]
    
    if not yesterday_billing:
        yesterday_billing = 0.0
    else:
        yesterday_billing = max(yesterday_billing)
    
    two_days_ago_billing = [dp.get('Average') for dp in DCN.get_billing_dp(start_time=datetime(yesterday.year, yesterday.month, yesterday.day) - timedelta(days=1),
                                end_time=datetime(yesterday.year, yesterday.month, yesterday.day),
                                period=3600).get("Datapoints")]
    
    if not two_days_ago_billing:
        two_days_ago_billing = 0.0
    else:
        two_days_ago_billing = max(two_days_ago_billing)
        
    return yesterday_billing if two_days_ago_billing > yesterday_billing  else  round(yesterday_billing - two_days_ago_billing, 2)

def send_message():
    pF_month = billing_data.get_prev_month_first_day()
    pL_month = billing_data.get_prev_month_last_day()
    cL_month = billing_data.get_cur_month_last_day()
    response = {
           "text" : f"""[TODAY🗓]: {today.year}-{str(today.month).zfill(2)}-{str(today.day).zfill(2)}\
                    \nExpenses: {get_todays_bills()} USD\
                    \n[YESTERDAY🗓]: {yesterday.year}-{str(yesterday.month).zfill(2)}-{str(yesterday.day).zfill(2)}\
                    \nExpenses: {get_yesterday_bills()} USD\
                    \n[CUR MONTH🗓]: {today.year}-{str(today.month).zfill(2)}-01 to {today.year}-{str(today.month).zfill(2)}-{str(cL_month.day).zfill(2)}\
                    \nExpenses: {collect_current_month_bills()} USD\
                    \n[PREV MONTH🗓]: {pF_month.year}-{str(pF_month.month).zfill(2)}-01 to {pL_month.year}-{str(pL_month.month).zfill(2)}-{str(pL_month.day).zfill(2)}\
                    \nExpenses: {collect_prev_month_bills()} USD
                    """}
    response = json.dumps(response)
    return requests.post(url=os.getenv("webhook_url"), data=response)

def main(event, context):
    send_message()
    return "expense statistics sent successfully"