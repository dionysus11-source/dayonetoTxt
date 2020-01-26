import json

with open("AllEntries.json", encoding = 'UTF8') as st_json:
	st_python = json.load(st_json)

obj = st_python.get('entries')
obj.reverse()
filename = '2020-01'
f = open(filename + '.txt', 'w')
for journal in obj:
	Date = str(journal['creationDate'])
	seoulTime = int(str(journal['creationDate'])[11:13]) + 9
	if seoulTime >= 24:
		seoulTime -= 24
		changeDate = int(journal['creationDate'][8:10]) + 1
		if changeDate < 10:
			changeDate = '0' + str(changeDate)
		else:
			changeDate = str(changeDate)
	else:
		changeDate = journal['creationDate'][8:10]
	if seoulTime < 10:
		seoulTime = '0' + str(seoulTime)
	Date = Date[:8]+str(changeDate) + ' ' + str(seoulTime) + Date[13:19]
	Date = '### ' + Date + '\n'
	if filename == Date[4:11]:
		Text = journal['text']
		removeImage = Text.split('\n\n')
		tt = removeImage[0] + '\n'
		# print(tt)
		latitude = str(journal['location']['latitude'])
		longitude = ',%20' + str(journal['location']['longitude']) + '\n\n'
		googleUrl = 'https://maps.google.com/?q=' + latitude + longitude
		# print(googleUrl)
		Data = Date + tt + googleUrl
		# print(Data)
		f.write(Data)
f.close()