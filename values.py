
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from datetime import date
from datetime import datetime

import numpy as np

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "12aPBmrHP5MLwoht9QcBiERPYUmXTJiTbBF43630togE"
SAMPLE_RANGE_NAME = "C9:I56"


def main(dicts : dict, item_range : str):
  """Shows basic usage of the Sheets API.
  Prints values from a sample spreadsheet.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      print()
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=item_range)
        .execute()
    )
    values = result.get("values", [])

    if not values:
      print("No data found.")
      return

    #print("Name, Major:")
    i=20
    n_a = [68,69,70,121,122,123,184,185,186,246,247,248,268,269,270]
    og_dict = np.load('ValueList.npy',allow_pickle=True).item()
    for row in values:
      # Print columns A and E, which correspond to indices 0 and 4.
      update_date = str(date.today())
      update_date = datetime.strptime(update_date, '%Y-%m-%d').strftime('%d/%m/%Y')
      if item_range == "Hyperchromes!C22:E63":
        n_a = [29,30,31,40,41,42,51,52,53]
        if i in n_a:
          i+=1
          continue
        try:
          if i in range(21,29):
            name = str('Hyper' + row[0].lower() + ' Level 5')
            dicts[name] = ['', row[1],'N/A',row[2],update_date]
          elif i in range(32,40):
            name = str('Hyper' + row[0].lower() + ' Level 4')
            dicts[name] = ['', row[1],'N/A',row[2],update_date]
          elif i in range(43,51):
            name = str('Hyper' + row[0].lower() + ' Level 3')
            dicts[name] = ['', row[1],'N/A',row[2],update_date]
          elif i in range(53,62):
            name = str('Hyper' + row[0].lower() + ' Level 2')
            dicts[name] = ['', row[1],'N/A',row[2],update_date]
          else:
            dicts[row[0].strip()] = ['', row[1],'N/A',row[2],update_date]
        except Exception as e:
            print(e)
        i+=1
      else:
        if(i in n_a):
            i+=1
            continue
        if i in range(309,323):
            i+=1
            continue
        if row[0] == 'IFIHADONE':
            name = '"If I had one" Trophy Case'
        else:
            name = row[0].strip()
        try:
            dicts[name] = ['', row[1],row[2],row[3],update_date]
        except Exception as e:
            print(e)
            print(i)
        i+=1
  except HttpError as err:
    print(err)
  
  #for key in list(dicts.keys()):
    #if str(key) not in list(og_dict.keys()):
      #print(key, dicts[key])
  #print(dicts)
  #print(og_dict)
  return dicts
  #for key, value in dicts.items() :
    #print (('"' + key +'"').strip(), ':', value, end=',\n')
  #np.save('ValueList.npy', dicts)

if __name__ == "__main__":
  main({}, "Value List!C20:F400")
