#This project is licensed under the terms of the GNU General Public License v3.0.
class Formatter():
	#The inputs for the formatter are based on preprogrammed formats, and the formatter will not function if they do not exist
	languages = {}
	languages["norwegian"] = {"pageShort" : "s.", "availableFrom" : "Hentet fra: ", "noDate" : "i. d."}
	languages["english"] = {"pageShort" : "p.", "availableFrom" : "Available from: ", "noDate" : "n. d."}
	languages["norwegian"]["monthNames"] = ["januar", "februar", "mars", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "desember"]
	languages["english"]["monthNames"] = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
	
	#Dictionary of lists of valid inputs for the formatter instance and the source
	validInputs = {}
	#Gets info from the dictionary defined above
	validInputs["language"] = sorted([item for item in languages])
	validInputs["publicationType"] = sorted(["book", "webpage"])
	validInputs["formatStyle"] = sorted(["harvard"])
	
	
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
	
	def __init__(self, formatStyle="harvard", language="english"):
		"""Saves the attributes for the formatter to the instance for referance later"""
		self.formatStyle = formatStyle
		self.language = language
	
	def formatSource(self, a1FirstName="", a1LastName="", a2FirstName="", a2LastName="", a3FirstName="", a3LastName="", pageNumberRange="", publishedYear="", publicationName="", publicationType="", publisherName="", publisherLocation="", publicationURL="", fetchedDate=""):
		"""Formats a source to the instance's standards, based on the inputs to this method"""
		#Setting up the formats
		templates = {}
		if self.formatStyle == "harvard":
			templates["AuthorNames"] = [
			((a1LastName + ", "), (a1LastName != "")), ((self._getInitials(a1FirstName) + ". "), (a1FirstName != "")),
			(("& "), ((a2FirstName != "" or a2LastName != "") and (a3FirstName == "" and a3LastName == ""))),
			((a2LastName + ", "), (a2LastName != "")), ((self._getInitials(a2FirstName) + ". "), (a2FirstName != "")),
			(("& "), (a3FirstName != "" or a3LastName != "")),
			((a3LastName + ", "), (a3LastName != "")), ((self._getInitials(a3FirstName) + ". "), (a3FirstName != ""))]
			
			templates["AuthorLastNames"] = [
			((a1LastName), (a1LastName != "")), ((", "), (a3LastName != "")),
			((" & "), (a2LastName != "" and a3LastName == "")), ((a2LastName), (a2LastName != "")),
			((" & "), (a3LastName != "")), ((a3LastName), (a3LastName != ""))]
			
			templates["pubYear_pubName"] = ((publishedYear + ", "), (publishedYear != "" and (a1FirstName != "" or a1LastName != ""))), ((publicationName), (publicationName != ""))
			
			if publicationType == "book":
				fullFormat = [*templates["AuthorNames"], *templates["pubYear_pubName"], ((","), (a1FirstName != "" or a1LastName != "") and (publisherLocation != "" or publisherName != "")), ((" "), (publicationName != "") and (publisherLocation != "" or publisherName != "")), ((publisherName), (publisherName != "")), ((", " + publisherLocation), (publisherLocation != ""))]
				shortFormat = [(("("), (True)), *templates["AuthorLastNames"],((publicationName), (a1LastName == "")), ((" " + publishedYear), (publishedYear != "")), ((")"), (True))]
			elif publicationType == "webpage":
				fullFormat = [*templates["AuthorNames"], *templates["pubYear_pubName"], ((". "), (publicationName != "")), ((self.languages[self.language]["availableFrom"] + publicationURL + ". "), (publicationURL != "")), (("[{}]".format(self._formatDate(fetchedDate))), (fetchedDate != ""))]
				shortFormat = [(("("), (True)), *templates["AuthorLastNames"],((publicationName), (a1LastName == "")), ((" " + publishedYear), (publishedYear != "")), (" " + (self.languages[self.language]["noDate"]), (publishedYear == "")), ((")"), (True))]

		#Concat all enabled strings to an output string
		fullSrc = ""
		for key, val in enumerate(fullFormat):
			if fullFormat[key][1] == True:
				fullSrc += str(val[0])
		
		shortSrc = ""
		for key, val in enumerate(shortFormat):
			if shortFormat[key][1] == True:
				shortSrc += str(val[0])
		#return dictionary for full and in text citation
		return {"full" : fullSrc, "short" : shortSrc}

if __name__ == "__main__":
	formatStyle = {"formatStyle" : "harvard", "language" : "english"}
	formatter = Formatter(**formatStyle)
	
	import inspect
	allArgs = list(inspect.getargspec(formatter.formatSource)[0])
	allArgs.remove("self")
	#print(allArgs, len(allArgs))
	
	bookDict = {key:key for key in allArgs}
	webpageDict = dict(bookDict)
	
	bookDict["publicationType"] = "book"
	bookDict["fetchedDate"] = ""
	webpageDict["publicationType"] = "webpage"
	webpageDict["fetchedDate"] = (1,2,2003)
	#bookDict = {"a1FirstName" : "a1FirstName", "a1LastName" : "a1LastName", "a2FirstName" : "a2FirstName", "a2LastName" : "a2LastName", "a3FirstName" : "a3FirstName", "a3LastName" : "a3LastName", "pageNumberRange" : "pageNumberRange", "publishedYear" : "publishedYear", "publicationName" : "publicationName", "publicationType" : "book", "publisherName" : "publisherName", "publisherLocation" : "publisherLocation", "publicationURL" : "publicationURL", "fetchedDate" : (1, 2, 2003)}
	#webpageDict = {"a1FirstName" : "a1FirstName", "a1LastName" : "a1LastName", "a2FirstName" : "a2FirstName", "a2LastName" : "a2LastName", "a3FirstName" : "a3FirstName", "a3LastName" : "a3LastName", "pageNumberRange" : "pageNumberRange", "publishedYear" : "publishedYear", "publicationName" : "publicationName", "publicationType" : "webpage", "publisherName" : "publisherName", "publisherLocation" : "publisherLocation", "publicationURL" : "publicationURL", "fetchedDate" : (1, 2, 2003)}
	
	bookFormatted = formatter.formatSource(**bookDict)
	print("Book: ")
	print(bookFormatted["full"])
	print(bookFormatted["short"] + "\n")
	
	webpageFormatted = formatter.formatSource(**webpageDict)
	print("Webpage: ")
	print(webpageFormatted["full"])
	print(webpageFormatted["short"])
