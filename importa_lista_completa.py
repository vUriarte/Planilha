import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
from googleapiclient import discovery

# use creds to create a client to interact with the Google Drive API
scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('planilha-warzone-581877ca2410.json', scope)
client = gspread.authorize(creds)
service = discovery.build('sheets', 'v4', credentials=creds)
# Find a workbook by name and open the first sheet
# Make sure you use the right name here.

## Extract and print all of the values
pp = pprint.PrettyPrinter()
#ranges = ['Warzone 1!A:A']
ranges = 'Warzone 1!A:A'
spreadsheet_id = "13jfxgCpQdiK10Imlln57kpurztWuvKkWCPCeylnW9fg"
include_grid_data = False # Incluir os dados da planilha
value_render_option = 'FORMATTED_VALUE'
date_time_render_option = 'SERIAL_NUMBER'

request2 = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=ranges,majorDimension='COLUMNS', valueRenderOption=value_render_option, dateTimeRenderOption=date_time_render_option)
request = service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=ranges, includeGridData=include_grid_data)
response = request2.execute()

playerslist = [] # Inicializa uma lista
for key,element in response.items(): # Response é um dicionário e a key values tem os nomes
	if key == 'values':
		playerslist.append(element)
			
uncleaned = str(playerslist[0]).split(',') # Cria lista de players
x = uncleaned[1] 
y = uncleaned [0]
uncleaned.remove(x) # Remove o segundo elemento
uncleaned.remove(y) # Remove o primeiro elemento

uncleaned = [w.replace(']', '') for w in uncleaned]
uncleaned = [w.replace("'", '') for w in uncleaned]
uncleaned = [w.strip() for w in uncleaned]
#for p in uncleaned:
#	print(p+"\n")

with open("ListaCompleta.txt","w+") as cleanfile:
	for line in uncleaned:
		cleanfile.write(line)
		cleanfile.write("\n")

#pp.pprint(playerslist)