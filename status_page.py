from bs4 import BeautifulSoup

import requests
import csv


#data = []

f = csv.writer(open("file_to_write", "w"))

data = open("file_to_read", "r")
for d in data:
	r = requests.get(d)
	html = r.text
	soup = BeautifulSoup(html, "lxml")
	if r.status_code == 200:
		status = "Ok"
		print(status)
	else:
		status = "Error"
		print(status)
	f.writerow([d,status])
data.close()
