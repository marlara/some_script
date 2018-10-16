import os
import csv

directory = os.getcwd() #recognize path of directory
print("Current working directory %s" % directory) #print the directory we are in

os.chdir("/home/utente/ic-data") #change the directory to another

print("Current working directory: ", os.getcwd()) #print the changed directory (1)

f = csv.writer(open("/home/utente/script_Bs4/identifier_ic.csv", "w")) #open a new csv in another directory (2)

for file in os.listdir(): #for every file in folder 1
	print(file) #print the file name
	read_file = open(file, "r") #read the file
	searchlines = read_file.readlines() #search in every line
	substring = "<dc:identifier>" #set the substring to search
	for linenum, line in enumerate(searchlines): #for every line and line number
		if substring in line: #if the substring is in line
				element = line.rstrip('\n') #set the line as the element
				print(linenum) #print the line number
				print(element) #print the element
		else:
			pass
	f.writerow([file,element]) #write the csv in folder 2 with the file name and the element found
file.close()
