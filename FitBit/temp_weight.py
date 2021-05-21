# https://towardsdatascience.com/collect-your-own-fitbit-data-with-python-ff145fa10873
# https://python-fitbit.readthedocs.io/en/latest/

import fitbit
from FitBit import gather_keys_oauth2 as Oauth2
import datetime
import pandas as pd
import os

CLIENT_ID = "22C8D9"
CLIENT_SECRET = "fefa5c686f92c124336fc68bc57229e6"
LBS_TO_KG = 0.45359237

data = pd.read_excel("C:/Users/gideo/Google Drive/Documenten-b/Self Study/Python/Fitness/FitBit/temp_weight.xlsx", engine='openpyxl')

server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])

auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)


two_to_seven_days_ago = []
for i in range(2, 9):
    two_to_seven_days_ago.append(str((datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%Y-%m-%d")))
yesterday = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
today = str(datetime.datetime.now().strftime("%Y-%m-%d"))

def obtain_sleep_data():
    """Sleep Summary on the night of ...."""
    fit_statsSum = auth2_client.sleep(date=yesterday)['sleep'][0]
    fit_bit_sleep = auth2_client.sleep(date=yesterday)['summary']['stages']
    ssummarydf = pd.DataFrame({'Date': fit_statsSum['dateOfSleep'],
                               'MainSleep': fit_statsSum['isMainSleep'],
                               'Efficiency': fit_statsSum['efficiency'],
                               'Duration': fit_statsSum['duration'],
                               'Minutes Asleep': fit_statsSum['minutesAsleep'],
                               'Minutes Awake': fit_statsSum['minutesAwake'],
                               'Awakenings': fit_statsSum['awakeCount'],
                               'Restless Count': fit_statsSum['restlessCount'],
                               'Restless Duration': fit_statsSum['restlessDuration'],
                               'Time in Bed': fit_statsSum['timeInBed'],
                               'Deep Sleep': fit_bit_sleep['deep'],
                               'Light Sleep': fit_bit_sleep['light'],
                               'REM Sleep': fit_bit_sleep['rem'],
                               'Wake Sleep': fit_bit_sleep['wake']
                               }, index=[0])
    return ssummarydf


def obtain_weight_data_average(days):
    sum = 0
    for i in range(days):
        fit_weight_log = auth2_client.body(date=two_to_seven_days_ago[i])['body']
        weight = round((fit_weight_log['weight'] * LBS_TO_KG), 1)
        sum += weight
    result = sum / days
    return result

def obtain_weight_data(df):
    """weight_log"""
    fit_weight_log = auth2_client.body(date=yesterday)['body']
    weight = round((fit_weight_log['weight'] * LBS_TO_KG), 1)
    df['weight'] = weight
    df['weight_yesterday'] = obtain_weight_data_average(1)
    if df.iloc[0]['weight_yesterday'] == 0:
        df._set_value(0, 'weight_yesterday', weight)
    df['average_3_days'] = obtain_weight_data_average(3)
    if df.iloc[0]['average_3_days'] == 0:
        df._set_value(0, 'average_3_days', df['weight_yesterday'])
    df['average_1_week'] = obtain_weight_data_average(7)
    if df.iloc[0]['average_1_week'] == 0:
        df._set_value(0, 'average_1_week', df['average_3_days'])
    return df

def obtain_calorie_extens_data(df):
    """calories_burned"""
    heart_activities = auth2_client.intraday_time_series('activities/heart', base_date=yesterday, detail_level='15min')[
        'activities-heart']
    heart_rate_zones = heart_activities[0]['value']['heartRateZones']
    calories_burned = 0
    for i in range(len(heart_rate_zones)):
        calories_burned += heart_rate_zones[i]['caloriesOut']
    df['calories burned'] = calories_burned
    return df


def insert_data():
    global data
    data = pd.DataFrame(data)
    df = obtain_sleep_data()
    df = obtain_weight_data(df)
    df = obtain_calorie_extens_data(df)
    name_yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%A")
    df['name_day'] = name_yesterday
    data = data.append(df, ignore_index=True)
    os.remove("C:/Users/gideo/Google Drive/Documenten-b/Self Study/Python/Fitness/FitBit/temp_weight.xlsx")
    data.to_excel("C:/Users/gideo/Google Drive/Documenten-b/Self Study/Python/Fitness/FitBit/temp_weight.xlsx", index=False)