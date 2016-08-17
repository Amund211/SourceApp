#This project is licensed under the terms of the GNU General Public License v3.0.
def test():
	pass
pass

def getInitials(name):
	initials = ""
	for char in name:
		if str(char).isupper():
			initials += char
	return initials


def formatDate(rawDate, language):
	"""Takes tuple (int day, int month, int year) and str language and formats it to a verbose format in the selected language"""
	formattedDate = "{0} {1} {2}".format(str(rawDate[0]), (languages[language]["monthNames"][rawDate[1]-1], str(rawDate[2])))


def formatSources(formatStyle, language, publicationType, a1FirstName="", a1LastName="", a2FirstName="", a2LastName="", a3FirstName="", a3LastName="", pageNumberRange="", publishedYear="", publicationName="", publisherName="", publisherLocation="", publicationURL="", fetchedDate=""):
	"""Formats source citations"""
	#Certain inputs are locked to certain values, and will error if they differ
	#language, formatStyle, publicationType
	languages = {}
	languages["norwegian"] = {"pageShort" : "s.", "availableFrom" : "Hentet fra: "}
	languages["english"] = {"pageShort" : "p.", "availableFrom" : "Available from: "}
	languages["norwegian"]["monthNames"] = ["januar", "februar", "mars", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "desember"]
	languages["english"]["monthNames"] = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
	
	#Setting up the formats
	tmpHarvardFull = {}
	tmpHarvardFull["book"] = [((a1LastName + ", "), (a1LastName != "")), ((getInitials(a1FirstName) + ". "), (a1FirstName != "")), (("& "), ((a2FirstName != "" or a2LastName != "") and (a3FirstName == "" and a3LastName == ""))), ((a2LastName + ", "), (a2LastName != "")), ((getInitials(a2FirstName) + ". "), (a2FirstName != "")), (("& "), (a3FirstName != "" or a3LastName != "")), ((a3LastName + ", "), (a3LastName != "")), ((getInitials(a3FirstName) + ". "), (a3FirstName != "")), ((publishedYear + ", "), (publishedYear != "" and (a1FirstName != "" or a1LastName != ""))), ((publicationName), (publicationName != "")), ((","), (a1FirstName != "" or a1LastName != "")), ((" "), (publicationName != "")), ((publisherName + ", "), (publisherName != "")), ((publisherLocation), (publisherLocation != ""))]
	#tmpHarvardFull["film"] = 
	#tmpHarvardFull["journal"] = 
	#tmpHarvardFull["newspaper"] = 
	tmpHarvardFull["webpage"] = [*tmpHarvardFull["book"][0:10], ((". "), (publicationName != "")), ((languages[language]["availableFrom"] + publicationURL + ". "), (publicationURL != "")), (("[{}]".format(formatDate(fetchedDate, language))), (fetchedDate != ""))]
	
	tmpHarvardShort = {}
	#Filling in the formats
	formats = {"harvard" : {"full" : tmpHarvardFull, "short" : tmpHarvardShort}}
	fullSrc = ""
	#print(formats[formatStyle]["full"])
	for key, val in enumerate(formats[formatStyle]["full"][publicationType]):
		if formats[formatStyle]["full"][publicationType][key][1] == True:
			fullSrc += str(val[0])
		
	#To omit an input set it to an empty string
	#
	return fullSrc

if __name__ == "__main__":
	allArgs = ["formatStyle", "language", "publicationType", "a1FirstName", "a1LastName", "a2FirstName", "a2LastName", "a3FirstName", "a3LastName", "pageNumberRange", "publishedYear", "publicationName", "publisherName", "publisherLocation", "publicationURL", "fetchedDate"]
	givenArgs = ["harvard", "english", "book", "a1FirstName", "a1LastName", "a2FirstName", "a2LastName", "a3FirstName", "a3LastName", "pageNumberRange", "publishedYear", "publicationName", "publisherName", "publisherLocation", "publicationURL", "fetchedDate"]
	givenArgs = ["harvard", "english", "webpage", "a1FirstName", "a1LastName", "a2FirstName", "a2LastName", "a3FirstName", "a3LastName", "pageNumberRange", "publishedYear", "publicationName", "publisherName", "publisherLocation", "publicationURL", "fetchedDate"]
	"""
	for key, val in enumerate(allArgs):
		argIn = input(str(val) + ": ")
		#argIn = "h"
		givenArgs.append(argIn)
	"""
	#print(formatSources(a1FirstName=givenArgs[0], a1LastName=givenArgs[1], a2FirstName=givenArgs[2], a2LastName=givenArgs[3], a3FirstName=givenArgs[4], a3LastName=givenArgs[5], pageNumberRange=givenArgs[6], publishedYear=givenArgs[7], publicationName=givenArgs[8], publicationType=givenArgs[9], publisherName=givenArgs[10], publisherLocation=givenArgs[11], language, formatStyle=givenArgs[12]))
	print(formatSources(*givenArgs))
	#print(getInitials("Amund Eggen Svandal"))


