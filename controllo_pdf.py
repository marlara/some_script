import requests
import csv

f = open('lista_url', 'r')

start_urls = [url.strip() for url in f.readlines()]

with open('url_controllati.csv', 'w') as f:
	fieldnames = ['url', 'estensione']
	writer = csv.DictWriter(f, fieldnames=fieldnames)

	writer.writeheader()

	for url in start_urls:
		r = requests.get(url)
		content_type = r.headers.get('content-type')

		if 'application/pdf' in content_type:
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

		writer.writerow({'url': url, 'estensione': ext})
		
f.close()