import requests
import csv

f = open('url_list', 'r')

start_urls = [url.strip() for url in f.readlines()] #strip possible whitespaces for every url

with open('url_checked.csv', 'w') as f: #open csv with fieldnames
	fieldnames = ['url', 'estensione']
	writer = csv.DictWriter(f, fieldnames=fieldnames)

	writer.writeheader()

	for url in start_urls: 
		r = requests.get(url)
		content_type = r.headers.get('content-type') #for every url in file get the header contetnt-type
		try: #eventually try
			if 'application/pdf' in content_type: #different content_type gives different answers
				ext = 'pdf'
				print('pdf')
			elif 'text/html' in content_type:
				ext = 'html'
				print('html')
			elif 'application/epub' in content_type:
				ext = 'epub'
				print('epub')
			else:
				ext = 'Unknown type: {}'.format(content_type)
				print('Unknown type: {}'.format(content_type))
		except (ValueError, AttributeError, TypeError): #managing errors
			ext = ('Error found')
			print('Ops! Found an error')
			pass

		writer.writerow({'url': url, 'estensione': ext}) #write rows in the new csv with the url checked and the extension
f.close()
r.close()
