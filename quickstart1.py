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
SAMPLE_SPREADSHEET_ID = "1mKz2YsgKevFvPI08XU7vCiaPBnUH9OvFzjBSO6TCvPg"
SAMPLE_RANGE_NAME = "Vehicles!C9:I56"


def main(dicts : dict, item_range : str):
  """Shows basic usage of the Sheets API.
  Prints values from a sample spreadsheet.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("/etc/secrets/token.json"):
    creds = Credentials.from_authorized_user_file("/etc/secrets/token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "/etc/secrets/credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    #with open("/etc/secrets/token.json", "w") as token:
      #print()
      #token.write(creds.to_json())

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
    i=9
    n_a = []
    for row in values:
      # Print columns A and E, which correspond to indices 0 and 4.
      if(i in n_a):
        i+=1
        continue
      
      update_date = str(date.today())
      update_date = datetime.strptime(update_date, '%Y-%m-%d').strftime('%d/%m/%Y')
      if item_range == 'Tires & Horns!C9:K200':
        dicts[row[0]] = ['', row[4],row[6],row[8],update_date]
        i+=1
      elif item_range == 'Hyperchromes!C10:I200':
        n_a = [18,19,28,29,38,39,48,49]
        if i in n_a:
          i+=1
          continue
        if i in range(10,18):
          name = str('Hyper ' + row[0] + ' level 5')
          dicts[name] = ['', row[2],row[4],row[6],update_date]
        elif i in range(20,28):
          name = str('Hyper ' + row[0] + ' level 4')
          dicts[name] = ['', row[2],row[4],row[6],update_date]
        elif i in range(30,38):
          name = str('Hyper ' + row[0] + ' level 3')
          dicts[name] = ['', row[2],row[4],row[6],update_date]
        elif i in range(40,48):
          name = str('Hyper ' + row[0] + ' level 2')
          dicts[name] = ['', row[2],row[4],row[6],update_date]
        else:
          dicts[row[0]] = ['', row[2],row[4],row[6],update_date]
        i+=1
      else:
        dicts[row[0]] = ['', row[2],row[4],row[6],update_date]
        i+=1
  except HttpError as err:
    print(err)
  #print(dicts)
  return dicts
  #for key, value in dicts.items() :
    #print (('"' + key +'"').strip(), ':', value, end=',\n')
  #np.save('ValueList.npy', dicts)

if __name__ == "__main__":
  main({}, "Hyperchromes!C10:I200")
