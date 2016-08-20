#This project is licensed under the terms of the GNU General Public License v3.0.
class Formatter():
	"""Formats source citations"""
	#The inputs for the formatter are based on preprogrammed formats, and will error if they do not exist
	languages = {}
	languages["norwegian"] = {"pageShort" : "s.", "availableFrom" : "Hentet fra: ", "noDate" : "i. d."}
	languages["english"] = {"pageShort" : "p.", "availableFrom" : "Available from: ", "noDate" : "n. d."}
	languages["norwegian"]["monthNames"] = ["januar", "februar", "mars", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "desember"]
	languages["english"]["monthNames"] = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
	
	def _getInitials(self, name):
		initials = ""
		for char in name:
			if str(char).isupper():
				initials += char
		return initials
	
	def _formatDate(self, rawDate):
		"""Takes tuple (int day, int month, int year) and str language and formats it to a verbose format in the selected language"""
		formattedDate = "{0} {1} {2}".format(str(rawDate[0]), self.languages[self.language]["monthNames"][rawDate[1]-1], str(rawDate[2]))
		return formattedDate
	
	def __init__(self, formatStyle, language, publicationType):
		self.formatStyle = formatStyle
		self.language = language
		self.publicationType = publicationType
	
	def formatSource(self, a1FirstName="", a1LastName="", a2FirstName="", a2LastName="", a3FirstName="", a3LastName="", pageNumberRange="", publishedYear="", publicationName="", publisherName="", publisherLocation="", publicationURL="", fetchedDate=""):
		#Setting up the formats
		#To omit an input set it to an empty string
		self.tmpHarvardFull = {}
		self.tmpHarvardFull["book"] = [((a1LastName + ", "), (a1LastName != "")), ((self._getInitials(a1FirstName) + ". "), (a1FirstName != "")), (("& "), ((a2FirstName != "" or a2LastName != "") and (a3FirstName == "" and a3LastName == ""))), ((a2LastName + ", "), (a2LastName != "")), ((self._getInitials(a2FirstName) + ". "), (a2FirstName != "")), (("& "), (a3FirstName != "" or a3LastName != "")), ((a3LastName + ", "), (a3LastName != "")), ((self._getInitials(a3FirstName) + ". "), (a3FirstName != "")), ((publishedYear + ", "), (publishedYear != "" and (a1FirstName != "" or a1LastName != ""))), ((publicationName), (publicationName != "")), ((","), (a1FirstName != "" or a1LastName != "")), ((" "), (publicationName != "")), ((publisherName + ", "), (publisherName != "")), ((publisherLocation), (publisherLocation != ""))]
		self.tmpHarvardFull["webpage"] = [*self.tmpHarvardFull["book"][0:10], ((". "), (publicationName != "")), ((self.languages[self.language]["availableFrom"] + publicationURL + ". "), (publicationURL != "")), (("[{}]".format(self._formatDate(fetchedDate))), (fetchedDate != ""))]
		
		self.tmpHarvardShort = {}
		self.tmpHarvardShort["book"] = [((a1LastName), (a1LastName != "")), ((", "), (a3LastName != "")), ((" & "), (a2LastName != "" and a3LastName == "")), ((a2LastName), (a2LastName != "")), ((" & "), (a3LastName != "")), ((a3LastName), (a3LastName != "")), ((publicationName), (a1LastName == "")), ((" " + publishedYear), (publishedYear != ""))]
		self.tmpHarvardShort["webpage"] = [*self.tmpHarvardShort["book"][0:8], (" " + (self.languages[self.language]["noDate"]), (publishedYear == ""))]
		#Filling in the formats
		self.formats = {"harvard" : {"full" : self.tmpHarvardFull, "short" : self.tmpHarvardShort}}
		#print(formats[formatStyle]["full"])
		self.fullSrc = ""
		for key, val in enumerate(self.formats[self.formatStyle]["full"][self.publicationType]):
			if self.formats[self.formatStyle]["full"][self.publicationType][key][1] == True:
				self.fullSrc += str(val[0])
		
		self.shortSrc = ""
		for key, val in enumerate(self.formats[self.formatStyle]["short"][self.publicationType]):
			if self.formats[self.formatStyle]["short"][self.publicationType][key][1] == True:
				self.shortSrc += str(val[0])
			
		#
		return (self.fullSrc, self.shortSrc)

if __name__ == "__main__":
	allArgs = ["formatStyle", "language", "publicationType", "a1FirstName", "a1LastName", "a2FirstName", "a2LastName", "a3FirstName", "a3LastName", "pageNumberRange", "publishedYear", "publicationName", "publisherName", "publisherLocation", "publicationURL", "fetchedDate"]
	givenArgs = ["harvard", "english", "book", "a1FirstName", "a1LastName", "a2FirstName", "a2LastName", "a3FirstName", "a3LastName", "pageNumberRange", "publishedYear", "publicationName", "publisherName", "publisherLocation", "publicationURL", "fetchedDate"]
	givenArgs = ["harvard", "english", "webpage", "a1FirstName", "a1LastName", "a2FirstName", "a2LastName", "a3FirstName", "a3LastName", "pageNumberRange", "publishedYear", "publicationName", "publisherName", "publisherLocation", "publicationURL", "fetchedDate"]
	
	bookStyle = {"formatStyle" : "harvard", "language" : "english", "publicationType" : "book"}
	webpageStyle = {"formatStyle" : "harvard", "language" : "english", "publicationType" : "webpage"}
	argDict = {"a1FirstName" : "a1FirstName", "a1LastName" : "a1LastName", "a2FirstName" : "a2FirstName", "a2LastName" : "a2LastName", "a3FirstName" : "a3FirstName", "a3LastName" : "a3LastName", "pageNumberRange" : "pageNumberRange", "publishedYear" : "publishedYear", "publicationName" : "publicationName", "publisherName" : "publisherName", "publisherLocation" : "publisherLocation", "publicationURL" : "publicationURL", "fetchedDate" : (1, 2, 2003)}
	
	#print(formatSources(a1FirstName=givenArgs[0], a1LastName=givenArgs[1], a2FirstName=givenArgs[2], a2LastName=givenArgs[3], a3FirstName=givenArgs[4], a3LastName=givenArgs[5], pageNumberRange=givenArgs[6], publishedYear=givenArgs[7], publicationName=givenArgs[8], publicationType=givenArgs[9], publisherName=givenArgs[10], publisherLocation=givenArgs[11], language, formatStyle=givenArgs[12]))
	bookFormatter = Formatter(**bookStyle)
	formatted = bookFormatter.formatSource(**argDict)
	print("Book: ")
	print(formatted[0])
	print(formatted[1])
	
	webpageFormatter = Formatter(**webpageStyle)
	formatted = webpageFormatter.formatSource(**argDict)
	print("Webpage: ")
	print(formatted[0])
	print(formatted[1])
	#print(Formatter.formatSources(*givenArgs))
	#print(_getInitials("Amund Eggen Svandal"))


