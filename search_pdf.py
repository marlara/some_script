from bs4 import BeautifulSoup

#import re
import requests
import csv

file = csv.writer(open("outputchecked.csv", "w")) 
file.writerow(["url", "controllo"]) #write header

f = open('url_list', 'r') #open file with list of urls
start_urls = [url.strip() for url in f.readlines()]

for url in start_urls: #for each url in the list 
	r = requests.get(url) #get the url
	soup = BeautifulSoup(r.text, "lxml") #and make a soup
	if r.status_code != 200: #this check if the url is 200 or not
		print("404!")
		file.writerow([url, "404"])
	else: #once the url is callable
		for link in soup.find_all("a"): #find all the "a"
			current_link = link.get("href") #and get the href
			if current_link.endswith('.pdf'): #if the href end with pdf you can do things
				print("Scaricabile")
				file.writerow([url, current_link])
			else: #else there's no pdf
				print("No pdf")
				file.writerow([url,"No pdf"])
f.close()
r.close()

'''
#that's for searching precise text inside an HTML page, and it uses re to compile the word to search

	if soup.find(text=re.compile("Download complete PDF")):
		print("Ok")
		file.writerow([url, "Download complete PDF"])
	else:
		print("No PDF")
		file.writerow([url,"No PDF"])


#that's for searching into nested elements

for url in start_urls:
	r = requests.get(url)
	soup = BeautifulSoup(r.text, "lxml")
	url_pdf = soup.find("p", class_="downloadPDF").a["href"]
	print(url_pdf)
	file.writerow([url, url_pdf])

'''
