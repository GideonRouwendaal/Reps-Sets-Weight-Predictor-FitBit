# https://towardsdatascience.com/collect-your-own-fitbit-data-with-python-ff145fa10873
# https://python-fitbit.readthedocs.io/en/latest/

import fitbit
from FitBit import gather_keys_oauth2 as Oauth2
import pandas as pd
import datetime
import os

CLIENT_ID = "22C8D9"
CLIENT_SECRET = "fefa5c686f92c124336fc68bc57229e6"
LBS_TO_KG = 0.45359237

data = pd.read_excel("C:/Users/gideo/Google Drive/Documenten-b/Self Study/Python/Fitness/FitBit/FitBit_data.xlsx", engine='openpyxl')

server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])

auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)

yesterday = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d"))
yesterday2 = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
today = str(datetime.datetime.now().strftime("%Y-%m-%d"))

# fit_statsHR = auth2_client.intraday_time_series('activities/heart', base_date=today, detail_level='1sec')
#
# time_list = []
# val_list = []
# for i in fit_statsHR['activities-heart-intraday']['dataset']:
#     val_list.append(i['value'])
#     time_list.append(i['time'])
# heartdf = pd.DataFrame({'Heart Rate':val_list,'Time':time_list})

# def stress_detection():
#     # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5058562/

# plot = plt
# plot.xlabel('Time')
# plot.ylabel('Heart Rate')
# x = heartdf["Time"]
# y = heartdf["Heart Rate"]
# plt.plot(x, y, alpha = 0.75)
# plot.show()
#
# print(heartdf["Heart Rate"])
#
# """Sleep data on the night of ...."""
# fit_statsSl = auth2_client.sleep(date='today')
# stime_list = []
# sval_list = []
# for i in fit_statsSl['sleep'][0]['minuteData']:
#     stime_list.append(i['dateTime'])
#     sval_list.append(i['value'])
# sleepdf = pd.DataFrame({'State':sval_list,
#                      'Time':stime_list})
# print(sleepdf)
#

def obtain_sleep_data():
    """Sleep Summary on the night of ...."""
    fit_statsSum = auth2_client.sleep(date='today')['sleep'][0]
    fit_bit_sleep = auth2_client.sleep(date='today')['summary']['stages']
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



def obtain_food_data(df):
    """foods_log"""
    fit_food_log = auth2_client.foods_log(date='today')['summary']
    df['calories in'] = fit_food_log['calories']
    df['protein'] = fit_food_log['protein']
    df['carbs'] = fit_food_log['carbs']
    df['fat'] = fit_food_log['fat']
    df['fiber'] = fit_food_log['fiber']
    df['sodium'] = fit_food_log['sodium']
    return df


# """activities"""
# fit_activity = auth2_client.activities(date='today')['activities']
# for i in range(len(fit_activity)):
#     if fit_activity[i]['activityParentName'] == 'Outdoor Bike':         # Get Biking stats
#         print(fit_activity[i])
#     if fit_activity[i]['activityParentName'] == 'Weights':              # Get Workout stats
#         print(fit_activity[i])

def obtain_weight_data(df):
    """weight_log"""
    fit_weight_log = auth2_client.body(date='today')['body']
    weight = round((fit_weight_log['weight'] * LBS_TO_KG), 1)
    df['weight'] = weight
    return df

def obtain_calorie_extens_data(df):
    """calories_burned"""
    heart_activities = auth2_client.intraday_time_series('activities/heart', base_date=today, detail_level='15min')[
        'activities-heart']
    heart_rate_zones = heart_activities[0]['value']['heartRateZones']
    calories_burned = 0
    for i in range(len(heart_rate_zones)):
        calories_burned += heart_rate_zones[i]['caloriesOut']
    df['calories burned'] = calories_burned
    """calorie_difference"""
    df['caloric difference'] = df['calories in'] - calories_burned
    return df


def insert_data():
    global data
    data = pd.DataFrame(data)
    df = obtain_sleep_data()
    df = obtain_food_data(df)
    df = obtain_weight_data(df)
    df = obtain_calorie_extens_data(df)
    data = data.append(df, ignore_index=True)
    os.remove("C:/Users/gideo/Google Drive/Documenten-b/Self Study/Python/Fitness/FitBit/FitBit_data.xlsx")
    data.to_excel("C:/Users/gideo/Google Drive/Documenten-b/Self Study/Python/Fitness/FitBit/FitBit_data.xlsx", index=False)