# https://towardsdatascience.com/how-to-import-google-sheets-data-into-a-pandas-dataframe-using-googles-api-v4-2020-f50e84ea4530

import pickle
import os.path
import pandas as pd
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import numpy as np
from scipy.optimize import curve_fit

from main import create_list_1RM
from test import create_graph, plateau_func

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '10febgCNMge5KAm-NQzOnsIIhSuybbEZ5KYNDknGNRlg'

DATA_TO_PULL_UPPER = 'Upper Body'
DATA_TO_PULL_LOWER = 'Lower Body'
DATA_TO_PULL_PUSH = 'Push'
DATA_TO_PULL_PULL = 'Pull'
DATA_TO_PULL_LEGGS = 'Legs'

def gsheet_api_check(SCOPES):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def pull_sheet_data(SCOPES, SPREADSHEET_ID, DATA_TO_PULL):
    creds = gsheet_api_check(SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=DATA_TO_PULL).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        rows = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                  range=DATA_TO_PULL).execute()
        data = rows.get('values')
        print("COMPLETE: Data copied")
        return data

def obtain_lift_data(df, exercise, next_exercise):
    lift_data = pd.DataFrame(df.iloc[df[0].str.contains(exercise,na=True).idxmax() + 1:df[0].str.contains(next_exercise,na=False).idxmax()])
    lift_data = lift_data.values
    y = np.array(create_list_1RM(lift_data))
    y = list(map(lambda x: (x / (1 + (5 / 30))), y))
    y = [exercise, y]
    create_graph(y)


upper_body_data = pull_sheet_data(SCOPES,SPREADSHEET_ID,DATA_TO_PULL_UPPER)
# lower_body_data = pull_sheet_data(SCOPES,SPREADSHEET_ID,DATA_TO_PULL_LOWER)
# push_body_data = pull_sheet_data(SCOPES,SPREADSHEET_ID,DATA_TO_PULL_PUSH)
# pull_body_data = pull_sheet_data(SCOPES,SPREADSHEET_ID,DATA_TO_PULL_PULL)
# legs_body_data = pull_sheet_data(SCOPES,SPREADSHEET_ID,DATA_TO_PULL_LEGGS)

df = pd.DataFrame(upper_body_data)

obtain_lift_data(df, "Bench Press", "DB Row")