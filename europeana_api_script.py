import csv
import requests
import urllib


cursor = '*'
baseUrl = 'https://www.europeana.eu/api/v2/search.json?wskey=YOUR_KEY&query=YOUR_QUERY-AND_OTHER_PARAMS*&rows=100&cursor=' #create a search api with things needed

f = csv.writer(open("europeana_output.csv", "w"))
f.writerow(["title", "id", "type", "subject", "contributor", "description", "publisher", "date", "pages", "source", "language", "coverage", "rights", "ifffUrl", "immagine", "issue", "dataset"]) #scrive gli header

file_log = open("log", "w") #open file to log temporary links

record_list = []

while True:
	url = baseUrl+urllib.parse.quote(cursor) #why are you using urllib instead of requests? Because I don't know how to use requests here
	print(url) #print url to check
	file_log.write(url)
	file_log.write("\n")
	response = requests.get(url) #get the url
	data = response.json() #pass the url to the json reader
	if data["success"] == True: #if the api call success
		for i in data["items"]: #for each item in page
			link = i["link"] #take the url of the record-based json
			record_list.append(link) #and append it to the list
			file_log.write(link) 
			file_log.write("\n")
		cursor = data["nextCursor"] #also, get the "nexCursor" value
	else: #if the api call fail
		print(data["error"]) #print the error message
		file_log.write("In" + url + "I had this error: " + error) #log error into file
		pass #then pass to the next
print("I've done! Now I'll start with records")
file_log.close()

'''Now we have searched every items we want with a search-type api (https://pro.europeana.eu/resources/apis/search), but lots of metadata are in the record-type api(https://pro.europeana.eu/resources/apis/record), so we have to move into the record-based search'''

for l in record_list: #this list has all the record-based json of each item searched
	print(l) #now print the link to check it
	r = requests.get(l) 
	page = r.json()
  #from here it is possible to change the values wanted
	title = page["object"]["title"]
	language = page["object"]["language"]
	for proxies in page["object"]["proxies"]: #those elements are inside "proxies" which has two subset
		contributor = proxies.get("dcContributor")
		print(contributor)
		description = proxies.get("dcDescription")
		print(description)
		subject = proxies.get("dcSubject")
		print(subject)
		date = proxies.get("dctermsIssued")
		print(date)
		source = proxies.get("dcPublisher")
		print(source)
		pages = proxies.get("dctermsExtent")
		print(pages)
		coverage = proxies.get("dctermsSpatial")
		print(coverage)
		issue = proxies.get("dctermsIssued")
		print(issue)
		print("stop with proxies")
		break #quit from the loop (there are two subset in proxies and I want just the first) not so elegant
	for aggregations in page["object"]["aggregations"]:
		publisher = aggregations.get("edmDataProvider")
		print(publisher)
		rights = aggregations.get("edmRights")
		print(rights)
		immagine = aggregations.get("edmIsShownBy")
		print(immagine)
		for item in aggregations["webResources"]: #iiif url is inside a more nested dict
			iiifUrl = item.get("dctermsIsReferencedBy")
		print(iiifUrl) #that's outside the loop cause it will gets the same element more than once
	dataset = page["object"]["edmDatasetName"]
	print(dataset)
	type_ = page["object"]["type"]
	id_ = page["object"]["about"]
	print(id_)
	print(type_)
	print(title)
	print(language)

	f.writerow([title, id_, type_, subject, contributor, description, publisher, date, pages, source, language, coverage, rights, ifffUrl, immagine, issue, dataset])
print("YEY I'VE DONE! :)")
# https://www.europeana.eu/portal/it/search?page=80&q=edm_datasetName%3A92%2Aewspapers%2A&qf%5B%5D=berliner+borsenzeitung
