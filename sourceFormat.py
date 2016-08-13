#This project is licensed under the terms of the GNU General Public License v3.0.
def test():
	pass
pass
def formatSources(formatStyle, language, publicationType, a1FirstName="", a1LastName="", a2FirstName="", a2LastName="", a3FirstName="", a3LastName="", pageNumberRange="", publishedYear="", publicationName="", publisherName="", publisherLocation=""):
	"""Formats source citations"""
	#Certain inputs are locked to certain values, and will error if they differ
	#language, formatStyle, publicationType
	languages = {}
	languages["norwegian"] = {"pageShort" : "s."}
	languages["english"] = {"pageShort" : "p."}
	
	#Setting up the formats
	tmpHarvardFull = {}
	tmpSwitchHarvardFull = {}
	tmpHarvardFull["book"] = [a1LastName + ", ", a1FirstName[:1] + ". ", "& ", a2LastName + ", ", a2FirstName[:1] + ". ", "& ", a3LastName + ", ", a3FirstName[:1] + ". ", publishedYear + ", ", publicationName, ",", " ", publisherName + ", ", publisherLocation]
	pass
	tmpSwitchHarvardFull["book"] = [(a1LastName != ""), (a1FirstName != ""), ((a2FirstName != "" or a2LastName != "") and (a3FirstName == "" and a3LastName == "")), (a2LastName != ""), (a2FirstName != ""), (a3FirstName != "" or a3LastName != ""), (a3LastName != ""), (a3FirstName != ""), (publishedYear != "" and (a1FirstName != "" or a1LastName != "")), (publicationName != ""), (a1FirstName != "" or a1LastName != ""), (publicationName != ""),  (publisherName != ""), (publisherLocation != "")]
	#tmpHarvardFull["film"] = 
	#tmpHarvardFull["journal"] = 
	#tmpHarvardFull["newspaper"] = 
	#tmpHarvardFull["webpage"] = 
	
	tmpHarvardShort = {}
	tmpSwitchHarvardShort = {}
	#Filling in the formats
	formats = {"harvard" : {"full" : tmpHarvardFull, "short" : tmpHarvardShort}}
	switches = {"harvard" : {"full" : tmpSwitchHarvardFull, "short" : tmpSwitchHarvardShort}}
	for k, v in formats.items():
		for ke, va in formats[k].items():
			for key, val in formats[k][ke].items():
				print("assesing formats[{}][{}][{}]".format(k, ke, key))
				if len(formats[k][ke][key]) != len(switches[k][ke][key]):
					raise UserWarning("A format and switch table pair was not equally long. (formats[{0}][{1}][{2}], {3} long; switches[{0}][{1}], {4} long.)".format(k, ke, key, len(formats[k][ke][key]), len(switches[k][ke][key])))
	
	fullSrc = ""
	#print(formats[formatStyle]["full"])
	print(tmpSwitchHarvardFull)
	for key, val in enumerate(formats[formatStyle]["full"][publicationType]):
		if switches[formatStyle]["full"][publicationType][key] == True:
			fullSrc += str(val)
		
	#To omit an input set it to an empty string
	#
	return fullSrc
	
allArgs = ["formatStyle", "language", "publicationType", "a1FirstName", "a1LastName", "a2FirstName", "a2LastName", "a3FirstName", "a3LastName", "pageNumberRange", "publishedYear", "publicationName", "publisherName", "publisherLocation"]
givenArgs = ["harvard", "english", "book", "a1FirstName", "a1LastName", "a2FirstName", "a2LastName", "a3FirstName", "a3LastName", "pageNumberRange", "publishedYear", "publicationName", "publisherName", "publisherLocation"]
"""
for key, val in enumerate(allArgs):
	argIn = input(str(val) + ": ")
	#argIn = "h"
	givenArgs.append(argIn)
"""
#print(formatSources(a1FirstName=givenArgs[0], a1LastName=givenArgs[1], a2FirstName=givenArgs[2], a2LastName=givenArgs[3], a3FirstName=givenArgs[4], a3LastName=givenArgs[5], pageNumberRange=givenArgs[6], publishedYear=givenArgs[7], publicationName=givenArgs[8], publicationType=givenArgs[9], publisherName=givenArgs[10], publisherLocation=givenArgs[11], language, formatStyle=givenArgs[12]))
print(formatSources(*givenArgs))


