import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
from googleapiclient import discovery

# use creds to create a client to interact with the Google Drive API
scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('planilha-warzone-581877ca2410.json', scope)
client = gspread.authorize(creds)
service = discovery.build('sheets', 'v4', credentials=creds)

pp = pprint.PrettyPrinter()

spreadsheet_id = "13jfxgCpQdiK10Imlln57kpurztWuvKkWCPCeylnW9fg"
include_grid_data = True # Incluir os dados da planilha
value_render_option = 'FORMATTED_VALUE'
date_time_render_option = 'SERIAL_NUMBER'

ranges = 'Warzone 1!A:A'
request1 = service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=ranges, includeGridData=include_grid_data)
response1 = request1.execute()
ranges = 'Warzone 2!A:A'
request2 = service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=ranges, includeGridData=include_grid_data)
response2 = request2.execute()
ranges = 'Warzone 3!A:A'
request3 = service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=ranges, includeGridData=include_grid_data)
response3 = request3.execute()

playerslist1 = []
for key,element in response1.items(): # Response é um dicionário e a key sheets tem as informações
	if key == 'sheets':
		playerslist1.append(element)

playerslist2 = []
for key,element in response2.items(): # Response é um dicionário e a key sheets tem as informações
	if key == 'sheets':
		playerslist2.append(element)
		
playerslist3 = []		
for key,element in response3.items(): # Response é um dicionário e a key sheets tem as informações
	if key == 'sheets':
		playerslist3.append(element)
		
		
uncleaned1 = str(playerslist1[0]).split("{") # Separa a string em uma lista
uncleaned2 = str(playerslist2[0]).split("{")
uncleaned3 = str(playerslist3[0]).split("{")

cleaned1 =[]
cleaned2 =[]
cleaned3 =[]

for line in uncleaned1:
	if 'pixelSize' not in line: # Remove todos os pixelsize da lista
		cleaned1.append(line)
		
for line in uncleaned2:
	if 'pixelSize' not in line: # Remove todos os pixelsize da lista
		cleaned2.append(line)
		
for line in uncleaned3:
	if 'pixelSize' not in line: # Remove todos os pixelsize da lista
		cleaned3.append(line)

cond = '\'formattedValue\':'
count = 0
players_dict={}
s2 = '\'formattedValue\':'

stp = 1
cleaned = list(cleaned1)	

while stp != 0:
	
	while (count < len(cleaned)): # percorre a lista
		if cond in cleaned[count]: # Quando achar formattedValue, entra no if 
			string = cleaned[count] # Elemento da lista para string
			substring = string[string.index(s2) + len(s2):] # Pega uma substring com o nome do player
			final = substring.split(",") # Retira tudo depois do nome do player, que tá na posição 0 da lista
			final[0] = final[0].replace('\'', '') # Retira aspas
			players_dict[final[0]] = cleaned[count+2] # Forma um dicionário onde key = nome do player
		count = count+1						  # e value = cor do background da célula
	
	count = 0
	redcolour = '\'red\': 1'
	bluecolour = '\'blue\': 1'
	greencolour =	'\'green\': 1'
	accesslist = []
	for key, value in players_dict.items(): # Retorna só os players com bg azul na planilha
		if redcolour not in value:
			if bluecolour not in value:
				if greencolour not in value:
					accesslist.append(key)
					#print(key+':'+value+'\n')

	replace1 = '\''
	replace2 = ']'
	
	accesslist.pop(0)
	for element in range(len(accesslist)):
		if replace1 in accesslist[element]:
			accesslist[element] = str(accesslist[element].replace ('\'', ''))
		if replace2 in accesslist[element]:
			accesslist[element] = str(accesslist[element].replace (']', ''))
		
	#for line in accesslist:
	#	print (line)
	
	if stp == 3:
		stp = 0
		with open("comacessowz3.txt","w+") as cleanfile:
			for line in accesslist:
				line = line.strip()
				cleanfile.write(line)
				cleanfile.write("\n")
	if stp == 2:
		stp = 3
		with open("comacessowz2.txt","w+") as cleanfile:
			for line in accesslist:
				line = line.strip()
				cleanfile.write(line)
				cleanfile.write("\n")		
		cleaned = list(cleaned3)
		players_dict.clear()
	if stp == 1:
		stp = 2
		with open("comacessowz1.txt","w+") as cleanfile:
			for line in accesslist:
				line = line.strip()
				cleanfile.write(line)
				cleanfile.write("\n")
		cleaned = list(cleaned2)
		players_dict.clear()
		
	#print (stp)
	