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
	tmpHarvardFull["book"] = [a1LastName + ", ", a1FirstName[:1] + ". ", publishedYear + ", ", publicationName, ",", " ", publisherName + ", ", publisherLocation]
	pass
	tmpSwitchHarvardFull["book"] = [(a1LastName != ""), (a1FirstName != ""), (publishedYear != "" and (a1FirstName != "" or a1LastName != "")), (publicationName != ""), (a1FirstName != "" or a1LastName != ""), (publicationName != ""),  (publisherName != ""), publisherLocation != ""]
	#tmpHarvardFull["film"] = 
	#tmpHarvardFull["journal"] = 
	#tmpHarvardFull["newspaper"] = 
	#tmpHarvardFull["webpage"] = 
	
	tmpHarvardShort = {}
	tmpSwitchHarvardShort = {}
	#Filling in the formats
	formats = {"harvard" : {"full" : tmpHarvardFull, "short" : tmpHarvardShort}}
	switches = {"harvard" : {"full" : tmpSwitchHarvardFull, "short" : tmpSwitchHarvardShort}}
	
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


