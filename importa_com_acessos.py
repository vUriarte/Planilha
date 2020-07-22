import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
from googleapiclient import discovery

# use creds to create a client to interact with the Google Drive API
scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('Planilha Warzone-fc28e7965fd6.json', scope)
client = gspread.authorize(creds)
service = discovery.build('sheets', 'v4', credentials=creds)

pp = pprint.PrettyPrinter()
#ranges = ['Warzone 1!A:A']
ranges = 'Warzone 1!A:A'
spreadsheet_id = "13jfxgCpQdiK10Imlln57kpurztWuvKkWCPCeylnW9fg"
include_grid_data = True # Incluir os dados da planilha
value_render_option = 'FORMATTED_VALUE'
date_time_render_option = 'SERIAL_NUMBER'

request = service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=ranges, includeGridData=include_grid_data)
response = request.execute()
playerslist = []


for key,element in response.items(): # Response é um dicionário e a key sheets tem as informações
	if key == 'sheets':
		playerslist.append(element)
		
		

uncleaned = str(playerslist[0]).split("{") # Separa a string em uma lista

cleaned =[]

for line in uncleaned:
	if 'pixelSize' not in line: # Remove todos os pixelsize da lista
		cleaned.append(line)

cond = '\'formattedValue\':'
count = 0
players_dict={}
s2 = '\'formattedValue\':'

while (count < len(cleaned)): # percorre a lista
	if cond in cleaned[count]: # Quando achar formattedValue, entra no if 
		string = cleaned[count] # Elemento da lista para string
		substring = string[string.index(s2) + len(s2):] # Pega uma substring com o nome do player
		final = substring.split(",") # Retira tudo depois do nome do player, que tá na posição 0 da lista
		final[0] = final[0].replace('\'', '') # Retira aspas
		players_dict[final[0]] = cleaned[count+2] # Forma um dicionário onde key = nome do player
	count = count+1								  # e value = cor do background da célula
	
pp.pprint(players_dict)

