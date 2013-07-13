#!/usr/bin/python3.3

import httplib2
import xml.etree.ElementTree as ET


filename = "word.txt"
flashcardfilename = filename[:filename.find(".")] + " flash card.txt"
errorfilename = "error.txt"

fp = open(filename, 'r')
flashcardfile = open(flashcardfilename, 'w')
words = fp.readlines()
errorfile = open(errorfilename, 'w')

learnersdicturlbase = "http://www.dictionaryapi.com/api/v1/references/learners/xml/";
h = httplib2.Http(".cache")

for word in words:
	strFront = word.rstrip();
	strBack = ""
	#print('[' + strFront + ']')
	url = learnersdicturlbase + word.rstrip() + "?key=" + key;
	resp, content = h.request(url, "GET")
	strContent = content.decode(encoding='UTF-8')
	strContent = strContent.replace("<it>", "").replace("</it>", "")
	try:	
		root = ET.fromstring(strContent)
	except:
		# no parse-able result
		errorfile.write(word)
		print("{} is not found".format(strFront))
		continue
	for entry in root.findall("entry"):
		if entry is not None:
			strBack = entry.get("id")
			for fl in entry.findall("fl"):
				strBack = strBack + " " + fl.text
			for pr in entry.findall("pr"):
				strBack = strBack + " |" + pr.text + "|<br>"
			for definition in entry.findall("def"):
				for dt in definition.findall("dt"):
					if dt is not None:
						if dt.text is not None:
							strBack = strBack + dt.text + "<br>"
						# show one example
						vi = dt.find("vi")
						if vi is not None:
							if vi.text is not None:
								strBack = strBack + "[e.g.]" + vi.text + "<br><br>"
	#print(strBack)
	flashcardfile.write(strFront + "\t" + strBack + "\n")		

	#flashcardfile.write(strContent)
	


