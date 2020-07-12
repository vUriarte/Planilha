import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
from googleapiclient import discovery

# use creds to create a client to interact with the Google Drive API
scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('Planilha Warzone-fc28e7965fd6.json', scope)
client = gspread.authorize(creds)
service = discovery.build('sheets', 'v4', credentials=creds)
# Find a workbook by name and open the first sheet
# Make sure you use the right name here.

sheet1 = client.open("Warzone Control - Xandebra").get_worksheet(1) # 1 = wz 1, 2 = wz 2, 3 = wz 3
sheet2 = client.open("Warzone Control - Xandebra").get_worksheet(2)
sheet3 = client.open("Warzone Control - Xandebra").get_worksheet(3)

## Extract and print all of the values
pp = pprint.PrettyPrinter()
ranges = ['Warzone 1!A:A']
spreadsheet_id = "13jfxgCpQdiK10Imlln57kpurztWuvKkWCPCeylnW9fg"
include_grid_data = True
request = service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=ranges, includeGridData=include_grid_data)
response = request.execute()

list_of_hashes = sheet3.get_all_records()

pp.pprint(response)
#list_of_hashes = sheet3.col_values(1)
#pp.pprint(list_of_hashes) # posição zero e posição 1 são lixo
#c = 0 
#for w1 in list_of_hashes:
#	c += 1
     #if w1[0] == w1[len(w1) - 1]:
