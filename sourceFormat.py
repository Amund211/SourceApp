#This project is licensed under the terms of the GNU General Public License v3.0.
class Formatter():
	#The inputs for the formatter are based on preprogrammed formats, and the formatter will not function if they do not exist
	languages = {}
	languages["norwegian"] = {"pageShort" : "s.", "availableFrom" : "Hentet fra: ", "noDate" : "i. d."}
	languages["english"] = {"pageShort" : "p.", "availableFrom" : "Available from: ", "noDate" : "n. d."}
	languages["norwegian"]["monthNames"] = ["januar", "februar", "mars", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "desember"]
	languages["english"]["monthNames"] = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
	
	def _getInitials(self, name):
		"""Gets all capital letters in a string, this is to avoid special names/titles like "van" to be able to interfere."""
		initials = ""
		for char in name:
			if str(char).isupper():
				initials += char
		return initials
	
	def _formatDate(self, rawDate):
		"""Takes tuple (int day, int month, int year) and formats it to a verbose format in the instance's language"""
		if rawDate != "":
			if not 0 < rawDate[0] < 32:
				raise UserWarning("Given value for day ({0}) was not valid. (Must be 1->31)".format(rawDate[0]))
			if not 0 < rawDate[1] < 13:
				raise UserWarning("Given value for day ({0}) was not valid. (Must be 1->12)".format(rawDate[1]))
			if not type(rawDate[0]) == type(0):
				raise UserWarning("Given value for year ({0}) was not valid. (Must be type int)".format(rawDate[2]))
			formattedDate = "{0} {1} {2}".format(str(rawDate[0]), self.languages[self.language]["monthNames"][rawDate[1]-1], str(rawDate[2]))
		else:
			formattedDate = ""
		return formattedDate
	
	def __init__(self, formatStyle, language, publicationType):
		"""Saves the attributes for the formatter to the instance for referance later"""
		self.formatStyle = formatStyle
		self.language = language
		self.publicationType = publicationType
	
	def formatSource(self, a1FirstName="", a1LastName="", a2FirstName="", a2LastName="", a3FirstName="", a3LastName="", pageNumberRange="", publishedYear="", publicationName="", publisherName="", publisherLocation="", publicationURL="", fetchedDate=""):
		"""Formats a source to the instance's standards, based on the inputs to this method"""
		#Setting up the formats
		self.formats = {}
		self.formats["harvard"] = {"full" : {}, "short" : {}}
		self.formats["harvard"]["full"]["book"] = [((a1LastName + ", "), (a1LastName != "")), ((self._getInitials(a1FirstName) + ". "), (a1FirstName != "")), (("& "), ((a2FirstName != "" or a2LastName != "") and (a3FirstName == "" and a3LastName == ""))), ((a2LastName + ", "), (a2LastName != "")), ((self._getInitials(a2FirstName) + ". "), (a2FirstName != "")), (("& "), (a3FirstName != "" or a3LastName != "")), ((a3LastName + ", "), (a3LastName != "")), ((self._getInitials(a3FirstName) + ". "), (a3FirstName != "")), ((publishedYear + ", "), (publishedYear != "" and (a1FirstName != "" or a1LastName != ""))), ((publicationName), (publicationName != "")), ((","), (a1FirstName != "" or a1LastName != "")), ((" "), (publicationName != "")), ((publisherName + ", "), (publisherName != "")), ((publisherLocation), (publisherLocation != ""))]
		self.formats["harvard"]["full"]["webpage"] = [*self.formats["harvard"]["full"]["book"][0:10], ((". "), (publicationName != "")), ((self.languages[self.language]["availableFrom"] + publicationURL + ". "), (publicationURL != "")), (("[{}]".format(self._formatDate(fetchedDate))), (fetchedDate != ""))]
		
		self.formats["harvard"]["short"]["book"] = [(("("), (True)), ((a1LastName), (a1LastName != "")), ((", "), (a3LastName != "")), ((" & "), (a2LastName != "" and a3LastName == "")), ((a2LastName), (a2LastName != "")), ((" & "), (a3LastName != "")), ((a3LastName), (a3LastName != "")), ((publicationName), (a1LastName == "")), ((" " + publishedYear), (publishedYear != "")), ((")"), (True))]
		self.formats["harvard"]["short"]["webpage"] = [*self.formats["harvard"]["short"]["book"][0:9], (" " + (self.languages[self.language]["noDate"]), (publishedYear == "")), ((")"), (True))]
		
		#Concat all enabled strings to an output string
		self.fullSrc = ""
		for key, val in enumerate(self.formats[self.formatStyle]["full"][self.publicationType]):
			if self.formats[self.formatStyle]["full"][self.publicationType][key][1] == True:
				self.fullSrc += str(val[0])
		
		self.shortSrc = ""
		for key, val in enumerate(self.formats[self.formatStyle]["short"][self.publicationType]):
			if self.formats[self.formatStyle]["short"][self.publicationType][key][1] == True:
				self.shortSrc += str(val[0])
		
		#return dictionary for full and in text citation
		return {"full" : self.fullSrc, "short" : self.shortSrc}

if __name__ == "__main__":
	bookStyle = {"formatStyle" : "harvard", "language" : "english", "publicationType" : "book"}
	webpageStyle = {"formatStyle" : "harvard", "language" : "english", "publicationType" : "webpage"}
	argDict = {"a1FirstName" : "a1FirstName", "a1LastName" : "a1LastName", "a2FirstName" : "a2FirstName", "a2LastName" : "a2LastName", "a3FirstName" : "a3FirstName", "a3LastName" : "a3LastName", "pageNumberRange" : "pageNumberRange", "publishedYear" : "publishedYear", "publicationName" : "publicationName", "publisherName" : "publisherName", "publisherLocation" : "publisherLocation", "publicationURL" : "publicationURL", "fetchedDate" : (1, 2, 2003)}
	
	bookFormatter = Formatter(**bookStyle)
	bookFormatted = bookFormatter.formatSource(**argDict)
	print("Book: ")
	print(bookFormatted["full"])
	print(bookFormatted["short"] + "\n")
	
	webpageFormatter = Formatter(**webpageStyle)
	webpageFormatted = webpageFormatter.formatSource(**argDict)
	print("Webpage: ")
	print(webpageFormatted["full"])
	print(webpageFormatted["short"])


