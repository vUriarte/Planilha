import os
import fileinput
import sys
from datetime import datetime
import shutil
from shutil import copyfile
import pathlib

class FileHandler:
	def __init__(self):
		pass
	
	def createfolder(self,c):
		today = datetime.now()
		#print(str(today.day) + "-" + str(today.month) + "-" + str(today.year))
		folder = str(today.day) + "-" + str(today.month) + "-" + str(today.year)+ " " + "wz " + c
		loop = 0
		while loop == 0:
			if os.path.exists(folder):
				shutil.rmtree(folder)
			else:
				os.mkdir(folder)
				loop = 1
		return folder
		

	def openanalyzer(self):
		with open("Analyzer.txt", "r") as file: #ler arquivo com o analyzer 
			l = file.readlines()
			file.close()
		return l
		
	
	def openacessso(self):
		with open("Comacesso.txt", "r") as file2: #ler arquivo dos com acesso
			acessos = file2.readlines()
			file2.close()
		return acessos
		
	
	def opencompleta(self):
		with open("ListaCompleta.txt", "r") as file4:
			comp = file4.readlines()
			file4.close()
		return comp
	
	def cleananalyzer(self,l,folder):
		with open("Analyzer.txt", "w") as file: #limpa o analyzer, deixa só os nomes
			for line in l:
				if ':' not in line:
					if "(Leader)" not in line:
						file.write(line)
					else:
						dummy = line.replace(" (Leader)\n",'\n')
						file.write(dummy)
		file.close()
		self.movetofolder(folder,"Analyzer.txt","Analyzer_limpo.txt")
	
	def generatenewmembers(self,comp,folder):
		destpath = str(pathlib.Path(__file__).parent.absolute()) + "/" + folder+ "/" + "Analyzer_limpo.txt"
		with open(destpath,"r+") as cleanfile, open("Novos membros.txt", "w") as newmembers:
			cleanlines = cleanfile.readlines()
			for line in cleanlines:
					#print("to na line:"+line+" e comparando com:"+line2)	
				if line not in comp:
					newmembers.write(line)
										
		cleanfile.close()
		newmembers.close()
		self.movetofolder(folder,"Novos membros.txt","Novos membros.txt")
		os.remove("Novos membros.txt")		
		
		
	def generateoldmembers(self, folder):
		destpath = str(pathlib.Path(__file__).parent.absolute()) + "/" + folder+ "/" + "Analyzer_limpo.txt"
		destpath2 = str(pathlib.Path(__file__).parent.absolute()) + "/" + folder+ "/" + "Novos membros.txt"
		with open(destpath,"r+") as cleanfile, open("Membros antigos.txt", "w+") as oldmembers, open(destpath2,"r") as newmembers:
			nm = newmembers.readlines()
			cleanlines = cleanfile.readlines()
			for line in cleanlines:
				#print(line)
				if line not in nm:
					oldmembers.write(line)
					
					
		cleanfile.close()
		oldmembers.close()
		newmembers.close()	
		self.movetofolder(folder,"Membros antigos.txt","Membros antigos.txt")
		os.remove("Membros antigos.txt")		
	
	def generateaccess(self,acessos,folder):
		destpath = str(pathlib.Path(__file__).parent.absolute()) + "/" + folder+ "/" + "Analyzer_limpo.txt"
		with open(destpath, "r") as file, open("Comacesso.txt", "r") as file2, open("Acessopresente.txt", "w") as file3:	
			l = file.readlines() #armazena o arquivo analyzer limpo na memória	
			for line in acessos:
				if line in l:					
					file3.write(line)
					
		file.close()
		file2.close()
		file3.close()
		self.movetofolder(folder,"Acessopresente.txt","Acessopresente.txt")
		os.remove("Acessopresente.txt")		
	
		
					
	def generatenoaccess(self,folder):
		destpath = str(pathlib.Path(__file__).parent.absolute()) + "/" + folder+ "/" + "Analyzer_limpo.txt"
		destpath2 = str(pathlib.Path(__file__).parent.absolute()) + "/" + folder+ "/" + "Acessopresente.txt"
		with open("Semacesso.txt", "w") as noaccess, open(destpath, "r") as file, open(destpath2, "r") as yesaccess: 
			l = file.readlines()
			ap = yesaccess.readlines()
			for line in l:
				if line not in ap:
					noaccess.write(line)
		noaccess.close()
		file.close()
		yesaccess.close()
		self.movetofolder(folder,"Semacesso.txt","Semacessopresente.txt")
		os.remove("Semacesso.txt")	
		
		
	def generatenoaccessandnonew(self,folder):
		destpath = str(pathlib.Path(__file__).parent.absolute()) + "/" + folder+ "/" + "Semacessopresente.txt"
		destpath2 = str(pathlib.Path(__file__).parent.absolute()) + "/" + folder+ "/" + "Novos membros.txt"
		with open("Antigossemacesso.txt", "w") as oldnoaccess, open(destpath, "r") as noaccess, open(destpath2, "r") as newmembers: 
			l = noaccess.readlines()
			nm = newmembers.readlines()
			for line in l:
				if line not in nm:
					oldnoaccess.write(line)
		
		oldnoaccess.close()
		noaccess.close()
		newmembers.close()
		self.movetofolder(folder,"Antigossemacesso.txt","Antigos sem acesso.txt")
		os.remove("Antigossemacesso.txt")			
	
	def movetofolder(self,folder,tocopy,txt):
		destpath = str(pathlib.Path(__file__).parent.absolute()) + "/" + folder+ "/" + txt
		print (destpath)
		copyfile(tocopy, destpath)
		
	def createcompletelist(self):
		os.system('py importa_lista_completa.py')
	

i = 0 
while i != 1:
	c = input("Warzone 1, 2 ou 3? (1,2,3)\n")
	if c == '1' or c == '2' or c == '3':
		i = 1
	else:
		i = 0
	

f1 = FileHandler()
#Criando pasta do dia 
folder = f1.createfolder(c)
#Abrindo os arquivos
l = f1.openanalyzer()
acessos = f1.openacessso()
f1.createcompletelist()
comp = f1.opencompleta()

#Processando a lista do analyzer
f1.cleananalyzer(l,folder)

#Gerando lista de novos membros
f1.generatenewmembers(comp,folder)

#Gerando lista de  membros antigos
f1.generateoldmembers(folder)

#Gera lista dos com acesso presente
f1.generateaccess(acessos,folder)

#Gera lista dos sem acesso presente
f1.generatenoaccess(folder)

#Gera lista dos antigos sem acesso
f1.generatenoaccessandnonew(folder)

