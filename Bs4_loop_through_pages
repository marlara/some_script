from bs4 import BeautifulSoup

import requests
import re
import csv

r  = requests.get("https://www.yoururl.net/").text #general page with thematic sections to loop through

soup = BeautifulSoup(r, "lxml")

f = csv.writer(open("output.csv", "w"))
f.writerow(["title", "type", "url", "cce", "readingage", "schoolgrade", "subject", "creator", "viafid", "viafname", "wikidataid", "contributor", "description", "publisher", "date", "format", "source", "language", "relation", "coverage", "rights", "rights2", "immagine", "altri utili"]) #write headers

lista_link = [] #create a list

themes_sections = soup.find_all("div", class_="class_with_links_of_pages_inside_themes_sections") #soup finds all links with pages inside

for i in themes_sections:
	page = i.find("a")
	link_to_scrap = page.get("href") #take the url
	if i.find(text=re.compile("Drammatico")) or i.find(text=re.compile("Commedia")) or i.find(text=re.compile("Azione")) or i.find(text=re.compile("Thriller")) or i.find(text=re.compile("Western")) or i.find(text=re.compile("Horror")) or i.find(text=re.compile("Comico")) or i.find(text=re.compile("Fantascienza")) or i.find(text=re.compile("Sentimentale")) or i.find(text=re.compile("Musicale")) or i.find(text=re.compile("Animazione")) or i.find(text=re.compile("Film in lingua originale")): #if the url has one of this genre
	genere = i.find("p", class_="itemTitle").get_text() #takes the genre
		print(genere) #print genre
		print(link_to_scrap) #print link to crawl
		r2  = requests.get("https://www.yoururl.net"+link_da_scrapare).text #compose link
		soup2 = BeautifulSoup(r2, "lxml")
		subject = soup2.find("h2", class_="title-border-bottom").get_text() #takes subject on top of the page

		for d in soup2.find_all("a", class_ = "articolo"): #soup finds all the articles
			link = d.get("href") #takes the specific article's url
			print(link)
			#print(subject)
						
			for tit in d.find_all("div", class_ = "titolo"):
				titolo = tit.text #extract just the text
				print(titolo) 

			for i in d.find_all("img", class_ = "landscape"):
				img = i.get("data-interchange") #gets the image's url
				print(img)
						
			r3  = requests.get("https://www.yoururl.net"+link)
			html_content = r3.text #We can actually access the content of the site using the text property of the completed request
			soup3 = BeautifulSoup(html_content, "lxml")

			url = r3.request.url

			description = soup3.find("div", class_="description").get_text()
			print(description)

			regia_interpreti = soup3.find("ul", class_="info").get_text("|")
			print(regia_interpreti)
			try:
				altri_utili = soup3.find("ul", class_='movie-info').get_text("|")
			except AttributeError:
				altri_utili = "No metadata" 		

			f.writerow([titolo, "Video", url, subject, "", "", "", regia_interpreti, "", "", "", "", description, "Rai", "", "", "", "italiano", "", "", "Tutti i diritti riservati", "Tutti i diritti riservati", img, altri_utili])


	else: #else for the first if
		pass


r3.close()
#csv_file.close()
r2.close()
r.close()
