#!/Library/Frameworks/Python.framework/Versions/3.3/bin/python3.3

import httplib2
import xml.etree.ElementTree as ET
import re

filename = "word.txt"
flashcardfilename = filename[:filename.find(".")] + " flash card.txt"
errorfilename = "error.txt"

fp = open(filename, 'r')
flashcardfile = open(flashcardfilename, 'w')
words = fp.readlines()
errorfile = open(errorfilename, 'w')

learnersdicturlbase = "http://www.dictionaryapi.com/api/v1/references/learners/xml/";
h = httplib2.Http(".cache")

key = "031e48e5-3b15-4bfd-bc33-16fdc78ae909"

for word in words:
	strBack = ""
	url = learnersdicturlbase + word.lower().rstrip().replace(" ", "%20") + "?key=" + key;
	resp, content = h.request(url, "GET")
	strContent = content.decode(encoding='UTF-8')
	strContent = strContent.replace("<it>", "").replace("</it>", "")
	try:	
		root = ET.fromstring(strContent)
		#print(strContent)
	except:
		# no parse-able result
		errorfile.write(word)
		print("{} is not found".format(word.rstrip()))
		continue
	found = False
	for entry in root.findall("entry"):
		if entry is not None:
			phrase = None
			strFront = entry.get("id")

			# entry has to match "word[" or "word$"
			valid = None
			pattern = "^" + word.lower().rstrip() +"\["
			result = re.match(pattern, strFront.lower().rstrip())
			if result is not None:
				valid = True

			pattern = word.lower().rstrip() + "$"
			result = re.match(pattern, strFront.lower().rstrip())
			if result is not None:
				valid = True

			phrase = None	
			if not valid:
				
				for in_ in entry.findall("in"):
					if in_ is not None:
						for if_ in in_.findall("if"):
							if if_.text.replace("*", "") == word.lower().rstrip():
								#print(strFront + " matches for " + word.lower().rstrip())
								valid = True
				for uro in entry.findall("uro"):
					if uro is not None:
						for ure in uro.findall("ure"):
							if ure.text.replace("*", "") == word.lower().rstrip():
								#print(strFront + " matches for " + word.lower().rstrip())
								valid = True
				for dro in entry.findall("dro"):
					if dro is not None:
						for dre in dro.findall("dre"):
							if dre.text.replace("*", "") == word.lower().rstrip():
								#print(strFront + " matches for " + word.lower().rstrip())
								valid = True
								phrase = dro

				if not valid:
					#print("skipping [" + strFront + "] for " + word.rstrip())
					continue

			# process result to generate the output	
			if phrase is not None:
				for dre in phrase.findall("dre"):
					strBack = strBack + dre.text + "<br>"
				for def_ in phrase.findall("def"):
					for phrasev in def_.findall("phrasev"):
						for pva in phrasev.findall("pva"):
							strBack = strBack + " " + pva.text + "<br>"
					for dt in def_.findall("dt"):
						if dt is not None:
							if dt.text is not None:
								strBack = strBack + dt.text + "<br>"
							# show one example
							vi = dt.find("vi")
							if vi is not None:
								if vi.text is not None:
									strBack = strBack + "[e.g.]" + vi.text + "<br><br>"
			else:					
				strBack = strFront + "<br>"
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
					
			# append the result to the output file					
			flashcardfile.write(word.rstrip().lower() + "\t" + strBack + "\n")
			found = True

	if not found:
		errorfile.write(word)
		print("{} is not found".format(word.rstrip()))
	
	


