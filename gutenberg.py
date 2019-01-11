import csv
import os
import requests

data = csv.DictReader(open("statusGut_pdfEpub.csv", "r"), delimiter=',', quotechar='"') 
f = open("audioGutenberg", "w")

os.chdir('/home/utente/script-python/gutenberg/file')

for d in data:
	idMedia = d['idMedia']
	name_dir = d['idGut']
	if d['StatusPDF'] == "Ok": #check if it is a PDF
		os.mkdir(name_dir) #make dir with gutenberg id
		link_file= d['PDF'] #takes the PDF link
		file_name = 'pg%s.pdf' %(name_dir) #create filename
		os.chdir('/home/utente/script-python/gutenberg/file/'+ name_dir) #change directory
		r = requests.get(link_file, stream=True) 
		with open(file_name, 'wb') as fd: #save pdf as with the right filename
			for chunk in r.iter_content(chunk_size=128):
				fd.write(chunk)
		print(name_dir+' done')
		os.chdir('/home/utente/script-python/gutenberg/file') #return to the previous directory
	elif d['StatusEPUB'] == "Ok": #same thing with epub
		os.mkdir(name_dir)
		link_file= d['EPUB']
		file_name = 'pg%s.epub' %(name_dir)
		os.chdir('/home/utente/script-python/gutenberg/file/'+ name_dir)
		r = requests.get(link_file, stream=True)
		with open(file_name, 'wb') as fd:
			for chunk in r.iter_content(chunk_size=128):
				fd.write(chunk)
		print(name_dir+' done')
		os.chdir('/home/utente/script-python/gutenberg/file')
	else:		
		f.write(idMedia)
		f.write('\n')
print('Done!')
