"""Formatter to format source citations"""
# This project is licensed under the terms of the GNU General Public License v3.0.


class Formatter():
	languages = {}
	languages["norwegian"] = {"pageShort": "s.", "availableFrom": "Hentet fra: ", "noDate": "i. d."}
	languages["english"] = {"pageShort": "p.", "availableFrom": "Available from: ", "noDate": "n. d."}
	languages["norwegian"]["monthNames"] = [
		"januar", "februar", "mars", "april", "mai", "juni",
		"juli", "august", "september", "oktober", "november", "desember"]
	languages["english"]["monthNames"] = [
		"January", "February", "March", "April", "May", "June",
		"July", "August", "September", "October", "November", "December"]

	# Valid inputs for the Formatter instance and source input.
	validInputs = {}
	validInputs["language"] = sorted([item for item in languages])		# Gets info from the dictionary defined above
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
			if not 0 < int(rawDate[0]) < 32:
				raise ValueError("Given value for day ({0}) was not valid. (Must be 1->31)".format(rawDate[0]))
			if not 0 < int(rawDate[1]) < 13:
				raise ValueError("Given value for day ({0}) was not valid. (Must be 1->12)".format(rawDate[1]))
			try:
				int(rawDate[2])
			except ValueError:
				raise TypeError("Given value for year ({0}) was not valid. (Must be type int)".format(rawDate[2]))
			formattedDate = "{0} {1} {2}".format(str(rawDate[0]), self.languages[self.language]["monthNames"][rawDate[1] - 1], str(rawDate[2]))
		else:
			formattedDate = ""
		return formattedDate

	def __init__(self, formatStyle="harvard", language="english"):
		"""Saves the attributes for the formatter to the instance for referance later"""
		if formatStyle not in self.validInputs["formatStyle"]:
			raise ValueError("Input for formatStyle was invalid ({})".format(formatStyle))

		if language not in self.validInputs["language"]:
			raise ValueError("Input for language was invalid ({})".format(language))

		self.formatStyle = formatStyle
		self.language = language

	def formatSource(
		self, authorNames="", pageNumberRange="", publishedYear="",
		publicationName="", publicationType="", publisherName="",
		publisherLocation="", publicationURL="", fetchedDate=""):
		"""Formats a source to the instance's standards, based on the inputs to this method"""
		if publicationType not in self.validInputs["publicationType"]:
			raise ValueError("Input for publicationType was invalid ({})".format(publicationType))

		# Setting up the formats
		#
		# The formats are defined by a list of tuples. The first element in each tuple will be a string,
		# and the second element will be a boolean. The first element of each tuple will be concatenated
		# onto an output string if, and only if, the second element of the tuple has a value of True.
		# The tuples should be given in the format: (("string"), (condition))
		#
		# NB: The default value of any input is an empty string. Thereby checking if an input is defined by
		# the user can be done as follows: (input != "")
		#
		# Example: ((publisherName), (publisherName != ""))
		# Will add the name of the publisher if it was given as an input

		templates = {}
		# Templates are a way of shortening the otherwise excrutiatingly long format definitions.
		# They work by defining smaller subsections of the formats which are used in multiple places.
		# These could be global across all formats, or could only apply for some subsets. For example:
		# the way that the authors' names are given in the harvard style for webpages and books are the
		# same for the source list, and the in text citation individually. Therefore I have, in the
		# formatStyle == "harvard" block defined the templates "AuthorNames" and "AuthorLastNames".
		#
		# Templates are given in the same way that the regular formats are, and are referenced by unpacking
		# the list in the place where it should be referenced
		# Templates can be generated through some algorithm, or created the same way the formats normally are
		# Example: fullFormat = [*templates["Template"], (("text"), (True))]
		#
		if self.formatStyle == "harvard":
			templates["AuthorNames"] = [("", False)]
			if authorNames != "":
				tmpAuthorNames = ""
				for number, name in enumerate(authorNames):
					if name[1] != "":
						tmpAuthorNames += name[1] + ", "
					if name[0] != "":
						tmpAuthorNames += self._getInitials(name[0]) + ". "
					if number == len(authorNames) - 2:
						tmpAuthorNames += "& "
				templates["AuthorNames"] = [(tmpAuthorNames, authorNames != "")]

			templates["AuthorLastNames"] = [("", False)]
			if authorNames != "":
				tmpAuthorLastNames = ""
				if len(authorNames) >= 4:
					for name in authorNames:
						if name[1] != "":
							# Find earliest author with last name
							tmpAuthorLastNames = name[1] + " et al."
							break
					if tmpAuthorLastNames == "":
						# No last names - use first name of first author
						tmpAuthorLastNames = authorNames[0][0] + " et al."
				else:
					for number, name in enumerate(authorNames):
						if name[1] != "":
							tmpAuthorLastNames += name[1] + ", "
						if number == len(authorNames) - 2:
							tmpAuthorLastNames += "& "
					tmpAuthorLastNames = tmpAuthorLastNames[:-2]
				templates["AuthorLastNames"] = [(tmpAuthorLastNames, authorNames != "")]

			if authorNames == "":
				# Ease of use onwards
				authorNames = [("", "")]
			templates["pubYear_pubName"] = [
				((publishedYear + ", "), (publishedYear != "" and (authorNames[0][0] != "" or authorNames[0][1] != ""))),
				((publicationName), (publicationName != ""))]

			if publicationType == "book":
				fullFormat = [
					*templates["AuthorNames"], *templates["pubYear_pubName"],
					((","), (authorNames[0][0] != "" or authorNames[0][1] != "") and (publisherLocation != "" or publisherName != "")),
					((" "), (publicationName != "") and (publisherLocation != "" or publisherName != "")),
					((publisherName), (publisherName != "")),
					((", " + publisherLocation), (publisherLocation != ""))]

				shortFormat = [
					(("("), (True)), *templates["AuthorLastNames"],
					((publicationName), (authorNames[0][1] == "")),
					((" " + publishedYear), (publishedYear != "")),
					((")"), (True))]

			elif publicationType == "webpage":
				fullFormat = [
					*templates["AuthorNames"], *templates["pubYear_pubName"],
					((". "), (publicationName != "")),
					((self.languages[self.language]["availableFrom"] + publicationURL + ". "), (publicationURL != "")),
					(("[{}]".format(self._formatDate(fetchedDate))), (fetchedDate != ""))]

				shortFormat = [
					(("("), (True)), *templates["AuthorLastNames"],
					((publicationName), (authorNames[0][1] == "")),
					((" " + publishedYear), (publishedYear != "")),
					(" " + (self.languages[self.language]["noDate"]), (publishedYear == "")),
					((")"), (True))]

		# Concat all enabled strings to an output string
		fullSrc = ""
		for key, val in enumerate(fullFormat):
			if fullFormat[key][1]:
				fullSrc += str(val[0])

		shortSrc = ""
		for key, val in enumerate(shortFormat):
			if shortFormat[key][1]:
				shortSrc += str(val[0])

		# Return dictionary for full and in text citation
		return {"full": fullSrc, "short": shortSrc}


if __name__ == "__main__":
	# """
	formatStyle = {"formatStyle": "harvard", "language": "english"}
	formatter = Formatter(**formatStyle)

	import inspect
	allArgs = list(inspect.getargspec(formatter.formatSource)[0])
	allArgs.remove("self")

	bookDict = {key: key for key in allArgs}
	webpageDict = dict(bookDict)

	bookDict["publicationType"] = "book"
	bookDict["fetchedDate"] = ""
	bookDict["authorNames"] = [
		("a1FirstName", "a1LastName"), ("a2FirstName", "a2LastName"),
		("a3FirstName", "a3LastName"), ("a4FirstName", "a4LastName")]
	webpageDict["publicationType"] = "webpage"
	webpageDict["fetchedDate"] = (1, 2, 2003)
	webpageDict["authorNames"] = [
		("a1FirstName", "a1LastName"), ("a2FirstName", "a2LastName"),
		("a3FirstName", "a3LastName"), ("a4FirstName", "a4LastName")]

	bookFormatted = formatter.formatSource(**bookDict)
	print("Book: ")
	print(bookFormatted["full"])
	print(bookFormatted["short"] + "\n")

	webpageFormatted = formatter.formatSource(**webpageDict)
	print("Webpage: ")
	print(webpageFormatted["full"])
	print(webpageFormatted["short"])
	"""
	import inspect

	print("Formatting a source:")
	print("Formatter options:")
	formatterArgList = list(inspect.getargspec(Formatter.__init__)[0])
	formatterArgList.remove("self")
	formatterKwargs = {}
	for item in formatterArgList:
		formatterKwargs[item] = input(item + ": ")

	print("\nSource input:")
	sourceArgList = list(inspect.getargspec(Formatter.formatSource)[0])
	sourceArgList.remove("self")
	sourceKwargs = {}
	for item in sourceArgList:
		sourceKwargs[item] = input(item + ": ")

	formatter = Formatter(**formatterKwargs)
	source = formatter.formatSource(**sourceKwargs)

	print("\n\n" + source["full"])
	print("\n" + source["short"])
	print(sourceKwargs)
	"""
