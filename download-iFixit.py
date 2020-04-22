#/usr/bin/env python3

import requests, sys, os, urllib.request

offset = 0  # Number of guides to skip from the beginning
limit = 200  # Number of guides to include in the response - 200 is the max allowed by the API
BAD_CHARS = '/\<>:"|?*'
DIR = "downloads"

files = []

if not os.path.isdir(DIR):
	os.mkdir(DIR)

while True:
	print(f"Request #{(offset//200)+1}")
	r = requests.get("https://www.ifixit.com/api/2.0/guides", params={"offset": offset, "limit": limit})
	if r.status_code != 200:
		print("API endpoint didn't return 200 OK.")
		sys.exit(1)
	data = r.json()
	if data == []:
		print("Finished.")
		break
	for guide in data:
		title = guide["title"]
		for c in BAD_CHARS:
			title = title.replace(c, "")
		title = title.strip()

		i = 2
		filename = title + ".pdf"
		while filename in files:
			filename =  title + " [" + str(i) + "].pdf"
			i += 1
		files.append(filename)
		if not os.path.isfile(DIR + '/' + filename):
			print("DOWNLOADING: " + filename)
			urllib.request.urlretrieve("https://www.ifixit.com/GuidePDF/link/" + str(guide["guideid"]) + "/en", DIR + '/' + filename)
	offset += 200
