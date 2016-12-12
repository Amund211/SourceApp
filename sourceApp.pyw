# This project is licensed under the terms of the GNU General Public License v3.0.
from sourceFormat import Formatter
import winsound
import pickle
import os
import math

import tkinter
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog

borderstyles = ["flat", "sunken", "raised", "groove", "ridge"]
borderstyle = borderstyles[4]
borderwidth = 2

class SourceList(tkinter.Frame):
	def __init__(self, parent):
		tkinter.Frame.__init__(self, parent)
		# Backend source management
		self.allSources = []
		# Backup of allSources at every save
		self.allSources_bak = []
		# Frontend shortened source list
		self.displaySources = []
		self.parent = parent
		self.initialize()
	
	def initialize(self):
		self.grid()
		self.config(borderwidth = borderwidth, relief = borderstyle)
		
		self.columnconfigure(0, weight = 1)
		self.columnconfigure(7, weight = 1)
		
		self.rowconfigure(0, weight = 1)
		self.rowconfigure(3, weight = 1)
		
		self.scrollbar = tkinter.Scrollbar(self)
		self.scrollbar.grid(row = 1, column = 6, sticky = "NS")
		
		self.listbox = tkinter.Listbox(self, yscrollcommand=self.scrollbar.set, height = 10, width = 100)
		self.listbox.grid(row = 1, column = 1, columnspan = 5, padx = (10, 10), pady = (10, 10))
		self.listbox.bind("<<ListboxSelect>>", self.onSelect)
		self.listbox.bind("<Double-1>", self.editEntry)
		
		self.scrollbar.config(command = self.listbox.yview)
		
		self.copyButton = tkinter.Button(self, text = "Copy", command = self.copyEntries)
		self.copyButton.grid(column = 2, row = 2, padx = (5, 5), pady = (2, 10), sticky = "E")
		
		self.editButton = tkinter.Button(self, text = "Edit", command = self.editEntry)
		self.editButton.grid(column = 3, row = 2, padx = (5, 5), pady = (2, 10), sticky = "")
		
		self.deleteButton = tkinter.Button(self, text = "Delete", command = self.deleteEntry)
		self.deleteButton.grid(column = 4, row = 2, padx = (5, 5), pady = (2, 10), sticky = "W")
	
	def copyEntries(self):
		"""Copy entire sourcelist to clipboard"""
		tmpSourceList = []
		sourceListOutput = ""
		if len(self.allSources) == 0:
			ErrorWindow(app, msg = "List is empty")
			return
		
		# Get and format sources
		for source in self.allSources:
			tmpSourceList.append(MainFormatter.formatSource(**source)["full"])
		
		# Alphabetize and concatenate to output
		for source in sorted(tmpSourceList):
			sourceListOutput += source + "\n"
		
		self.clipboard_clear()
		self.clipboard_append(sourceListOutput)
	
	def editEntry(self, *args):
		"""Remove entry from sourcelist and bring datapoints back into the entry fields to edit"""
		try:
			listIndex = self.listbox.curselection()[0]
			for key in self.parent.sourceInput.vars:
				try:
					if key == "fetchedDay":
						self.parent.sourceInput.vars[key].set(self.allSources[listIndex]["fetchedDate"][0])
					elif key == "fetchedMonth":
						self.parent.sourceInput.vars[key].set(self.allSources[listIndex]["fetchedDate"][1])
					elif key == "fetchedYear":
						self.parent.sourceInput.vars[key].set(self.allSources[listIndex]["fetchedDate"][2])
					elif key == "publicationType":
						self.parent.sourceInput.vars[key].set(self.allSources[listIndex][key].capitalize())
					elif key == "authorNames":
						for itr in range(0, len(self.parent.sourceInput.vars[key])*2):
							self.parent.sourceInput.vars[key][itr].set(self.allSources[listIndex][key][math.floor(itr/2)][itr%2])
					else:
						self.parent.sourceInput.vars[key].set(self.allSources[listIndex][key])
				except (IndexError, KeyError):
					pass
			del self.allSources[listIndex]
			self.updateList()
		except IndexError:
			ErrorWindow(app, msg = "No entry selected")
	
	def deleteEntry(self):
		"""Remove entry from sourcelist"""
		try:
			listIndex = self.listbox.curselection()[0]
			del self.allSources[listIndex]
			self.updateList()
		except IndexError:
			ErrorWindow(app, msg = "No entry selected")
		
	
	def onSelect(self, event):
		"""Passes the selected source to the sourceDisplay instance to display it"""
		sender = event.widget
		try:
			listIndex = sender.curselection()[0]
			value = self.allSources[listIndex]
			self.parent.sourceDisplay.setSource(value)
		except IndexError:
			pass
	
	def updateList(self):
		"""Updates the displaySources list to reflect the allSources list based on edits or a new formatter"""
		self.displaySources = []
		# Converting dictionary allSources to list displaySources
		for dictnum, dict in enumerate(self.allSources[:]):
			self.displaySources.append([])
			for kwnum, kw in enumerate(self.allSources[dictnum]):
				if self.allSources[dictnum][kw] != "":
					if type(self.allSources[dictnum][kw]) == list:
						# authorNames list
						tmpAuthorNames = []
						for nameTuple in self.allSources[dictnum][kw]:
							if nameTuple != ("", ""):
								# Nametuple contains data -> display in list
								tmpAuthorNames.append(nameTuple)
						self.displaySources[dictnum].append(tmpAuthorNames)
					else:
						self.displaySources[dictnum].append(self.allSources[dictnum][kw])

		for dictnum in range(len(self.allSources[:])-1):
			# Deleting duplicate entries
			if self.allSources[dictnum]==self.allSources[-1]:
				del(self.allSources[-1])
				del(self.displaySources[-1])
				break
			# Deleting empty entries
			if len(self.allSources[dictnum]) == 0:
				del(self.allSources[dictnum])
				del(self.displaySources[dictnum])
		
		# Populating the listbox
		self.listbox.delete(0, tkinter.END)
		for item in self.displaySources:
			self.listbox.insert(tkinter.END, item)


class SourceDisplay(tkinter.Frame):
	def __init__(self, parent):
		tkinter.Frame.__init__(self, parent)
		self.parent = parent
		self.currSource = {}
		self.initialize()
	
	def initialize(self):
		self.grid()
		self.config(borderwidth = borderwidth, relief = borderstyle)
		
		self.columnconfigure(0, weight = 1)
		self.rowconfigure(0, weight = 1)
		self.rowconfigure(6, weight = 1)
		
		self.label1 = tkinter.Label(self, text="In text citation:")
		self.label1.grid(column = 0, row = 1, padx = (10, 10), pady = (10, 0))
		
		self.source1 = tkinter.Text(self, height = 1, width = 50)
		self.source1.config(state = "disabled")
		self.source1.grid(column = 0, row = 2, padx = (10, 10), pady = (0, 10))
		
		self.copyButton = tkinter.Button(self, text = "Copy", command = self.copyShort)
		self.copyButton.grid(column = 0, row = 3)
		
		self.label2 = tkinter.Label(self, text="Citation list entry:")
		self.label2.grid(column= 0, row=4, padx = (10, 10), pady = (10, 0))
		
		self.source2 = tkinter.Text(self, height = 4, width = 75)
		self.source2.config(state = "disabled")
		self.source2.grid(column = 0, row = 5, padx = (10, 10), pady = (0, 10))
	
	def copyShort(self):
		"""Copies short form source format to clipboard"""
		self.clipboard_clear()
		self.clipboard_append(self.source1.get("1.0", "end")[:-1])
	
	def setSource(self, source):
		"""Formats given source and displays it"""
		# Activated by SourceList.onSelect method
		
		if not "publicationType" in source:
			# Invalid source
			return
		
		formattedSource = MainFormatter.formatSource(**source)
		self.source1.config(state = "normal")
		self.source1.delete(1.0, tkinter.END)
		self.source1.insert("insert", formattedSource["short"])
		self.source1.config(state = "disabled")
		
		self.source2.config(state = "normal")
		self.source2.delete(1.0, tkinter.END)
		self.source2.insert("insert", formattedSource["full"])
		self.source2.config(state = "disabled")
		self.currSource = source


class SourceInput(tkinter.Frame):
	def __init__(self, parent, *args, **kw):
		tkinter.Frame.__init__(self, parent, *args, **kw)			
		self.parent = parent
		self.initialize()
	
	def initialize(self):
		self.grid()
		self.config(borderwidth = borderwidth, relief = borderstyle)
		
		# create a canvas object and a vertical scrollbar for scrolling it
		self.vscrollbar = tkinter.Scrollbar(self)
		self.vscrollbar.grid(sticky = "NS", column = 1, row = 0)
		self.canvas = tkinter.Canvas(self, bd = 0, highlightthickness = 0, yscrollcommand = self.vscrollbar.set)
		self.canvas.grid(column = 0, row = 0, sticky = "NSEW")
		self.columnconfigure(0, weight = 1)
		self.rowconfigure(0, weight = 1)
		self.vscrollbar.config(command = self.canvas.yview)

		# reset the view
		self.canvas.xview_moveto(0)
		self.canvas.yview_moveto(0)

		# create a frame inside the canvas which will be scrolled with it
		self.interior = interior = tkinter.Frame(self.canvas)
		self.interior.grid(sticky = "NSEW")
		self.interior_id = self.canvas.create_window(0, 0, window = interior, anchor = tkinter.NW)
		
		# Bind windowconfigure to object method to handle resizing properly
		# Allow mousewheel to scroll the scrollbar
		self.interior.bind('<Configure>', self._configure_interior)
		self.canvas.bind('<Configure>', self._configure_canvas)
		self.interior.bind("<MouseWheel>", self._on_mousewheel)
		
		self.populate()
	
	def populate(self):
		"""Adds widgets and defines vars"""
		self.varNames = ["formatStyle", "language", "publicationType", "authorNames",
						"pageNumberRange", "publishedYear", "publicationName", "publisherName",
						"publisherLocation", "publicationURL", "fetchedDate"]
		
		self.textNames = ["Format style:", "Language:", "Publication type:", "Author names:",
						"Page number/range:", "Published year:", "Publication name:", "Publisher name:",
						"Publisher location:", "Publication URL:", "Date fetched:"]
		
		self.comboboxValues = {"formatStyle" : [value.capitalize() for value in Formatter.validInputs["formatStyle"]],
								"language" : [value.capitalize() for value in Formatter.validInputs["language"]],
								"publicationType" : [value.capitalize() for value in Formatter.validInputs["publicationType"]],
								"fetchedDay" : list(range(32)),
								"fetchedMonth" : list(range(13)),
								"fetchedYear" : [0, *list(range(2016, 2031, 1))]}
		
		if len(self.varNames) != len(self.textNames):
			raise UserWarning("varNames and textNames table pair was not equally long. (SourceInput.varNames, {0} long; SourceInput.textNames, {1} long.)".format(len(self.varNames), len(self.textNames)))
		
		# Organize widgets into a dictionary to avoid cluttering the namespace
		self.texts = {}
		self.vars = {}
		self.formatterOptions = {}
		self.widgets = {"labels" : {}, "entries" : {}, "comboboxes" : {}}
		for k, v in enumerate(self.varNames):
			if v == "authorNames":
				self.authorFrame = tkinter.Frame(self.interior)
				self.authorFrame.grid(column = 0, columnspan = 5, row = k+1, padx = (0, 0), pady = (0, 0), sticky = "NSEW")
				self.authorFrame.columnconfigure(1, weight = 1)
				self.authorFrame.bind("<MouseWheel>", self._on_mousewheel)
				self.authorLabels = []
				self.authorEntries = []
				self.vars["authorNames"] = []
				self.populateAuthors()
				
			elif v == "fetchedDate":
				self.vars["fetchedDay"] = tkinter.IntVar(self)
				self.vars["fetchedMonth"] = tkinter.IntVar(self)
				self.vars["fetchedYear"] = tkinter.IntVar(self)
				self.texts[v] = self.textNames[k]
				self.widgets["entries"][v] = tkinter.Label(self.interior, text = self.texts[v])
				self.widgets["entries"][v].grid(column = 0, row = k+1, padx = (10, 0), pady = (10, 10))
				self.widgets["comboboxes"]["fetchedDay"] = ttk.Combobox(self.interior, textvar = self.vars["fetchedDay"], values = self.comboboxValues["fetchedDay"], width = 2)
				self.widgets["comboboxes"]["fetchedDay"].grid(column = 1, row = k+1, padx = (0, 1), pady = (10, 10), sticky = "E")
				self.widgets["comboboxes"]["fetchedMonth"] = ttk.Combobox(self.interior, textvar = self.vars["fetchedMonth"], values = self.comboboxValues["fetchedMonth"], width = 2)
				self.widgets["comboboxes"]["fetchedMonth"].grid(column = 2, row = k+1, padx = (1, 1), pady = (10, 10), sticky = "W")
				self.widgets["comboboxes"]["fetchedYear"] = ttk.Combobox(self.interior, textvar = self.vars["fetchedYear"], values = self.comboboxValues["fetchedYear"], width = 4)
				self.widgets["comboboxes"]["fetchedYear"].grid(column = 3, row = k+1, padx = (1, 10), pady = (10, 10), sticky = "W")
			
			else:
				self.texts[v] = self.textNames[k]
				self.widgets["labels"][v] = tkinter.Label(self.interior, text = self.texts[v])
				self.widgets["labels"][v].grid(column = 0, row = k+1, padx = (10, 10), pady = (10, 10))
				self.widgets["labels"][v].bind("<MouseWheel>", self._on_mousewheel)
				# Do not add entry widget for the formatter options (added later)
				if k >= 3:
					self.vars[v] = tkinter.StringVar(self)
					self.widgets["entries"][v] = tkinter.Entry(self.interior, textvar = self.vars[v])
					self.widgets["entries"][v].grid(column = 1, columnspan = 4, row = k+1, padx = (10, 10), pady = (10, 10), sticky = "EW")
					self.widgets["entries"][v].bind("<MouseWheel>", self._on_mousewheel)
				elif k == 2:
					self.vars[v] = tkinter.StringVar(self)
					self.widgets["comboboxes"][v] = ttk.Combobox(self.interior, state = "readonly", textvar = self.vars[v], values = self.comboboxValues[v], width = 15)
					self.widgets["comboboxes"][v].grid(column = 1, row = k+1, padx = (10, 10), pady = (10, 10))

				else:
					self.formatterOptions[v] = tkinter.StringVar(self)
					self.widgets["comboboxes"][v] = ttk.Combobox(self.interior, state = "readonly", textvar = self.formatterOptions[v], values = self.comboboxValues[v], width = 15)
					self.widgets["comboboxes"][v].grid(column = 1, row = k+1, padx = (10, 10), pady = (10, 10))
		
					
		self.button = tkinter.Button(self.interior, text = "Add source", command = self.addSource)
		self.button.grid(column = 1, row = len(self.widgets["labels"]) + 5, padx = (10, 10), pady = (10, 10))
		self.interior.columnconfigure(4, weight = 1)
		self.interior.rowconfigure(0, weight = 1)
		self.interior.rowconfigure(len(self.widgets["labels"]) + 6, weight = 1)
		
		# Default values for the formatter
		self.formatterOptions["language"].set("Norwegian")
		self.formatterOptions["formatStyle"].set("Harvard")
		# Set trace
		self.formatterOptions["language"].trace("w", updateFormatter)
		self.formatterOptions["formatStyle"].trace("w", updateFormatter)
	
	def populateAuthors(self):
		pass
		for itr in range(0, 3-len(self.vars["authorNames"])):
			for nameType in ["first", "last"]:
				self.vars["authorNames"].append(tkinter.StringVar())
				self.authorLabels.append(tkinter.Label(self.authorFrame, text="A. {} {} name:".format(math.floor((1+len(self.vars["authorNames"]))/2), nameType.capitalize())))
				self.authorLabels[-1].bind("<MouseWheel>", self._on_mousewheel)
				self.authorLabels[-1].grid(column = 0, row = len(self.vars["authorNames"]), padx = (10, 10), pady = (10, 10))
				
				self.authorEntries.append(tkinter.Entry(self.authorFrame, textvar=self.vars["authorNames"][-1]))
				self.authorEntries[-1].grid(column = 1, row = len(self.vars["authorNames"]), padx = (10, 10), pady = (10, 10), sticky = "EW")
				self.authorEntries[-1].bind("<MouseWheel>", self._on_mousewheel)
				
		#self.authorEntries
		#self.authorFrame
		#self.authorLabels
		#self.vars["authorNames"]
	
	def addSource(self, *args):
		"""Gets data from vars stored on instance and adds them as new source to SourceList.allSources and updates list"""
		# Bound to <Return>, and to button in SourceInput
		
		# Get data from the stringvars, and remove empty inputs
		outputVars = {}
		tmpDateFetched = [0, 0, 0]
		try:
			for k, v in enumerate(self.vars):
				if type(self.vars[v]) == list:
					outputVars[v] = []
					for itr in range(0, len(self.vars[v]), 2):
						tmpTuple = (self.vars[v][itr].get(), self.vars[v][itr+1].get())
						outputVars[v].append((tmpTuple))
				else:
					if self.vars[v].get() != "":
						if v == "fetchedDay":
							tmpDateFetched[0] = self.vars[v].get()
						elif v == "fetchedMonth":
							tmpDateFetched[1] = self.vars[v].get()
						elif v == "fetchedYear":
							tmpDateFetched[2] = self.vars[v].get()
						elif v == "publicationType":
							outputVars[v] = self.vars[v].get().lower()
						else:
							outputVars[v] = self.vars[v].get()
		except tkinter.TclError:
			ErrorWindow(app, msg = "Input for {} was invalid".format(v))
			return
		if 0 < tmpDateFetched[0] < 32:
			if 0 < tmpDateFetched[1] < 13:
				if tmpDateFetched[2] != 0:
					outputVars["fetchedDate"] = tuple(tmpDateFetched)
				elif tmpDateFetched[2] != 0:
					ErrorWindow(app, msg = "Input for fetched year must be type int")
					return
			elif tmpDateFetched[1] != 0:
				ErrorWindow(app, msg = "Input for fetched month must be 1-12")
				return
		elif tmpDateFetched[0] != 0:
			ErrorWindow(app, msg = "Input for fetched day must be 1-31")
			return
		
		# Throw error if publicationType not defined
		if not "publicationType" in outputVars:
			self.canvas.yview_moveto(0)
			self.widgets["comboboxes"]["publicationType"].focus()
			ErrorWindow(app, msg = "No input given for publication type")
			return
		
		# Clear input fields
		for k, v in enumerate(self.vars):
			if type(self.vars[v]) == tkinter.StringVar:
				self.vars[v].set("")
			elif type(self.vars[v]) == tkinter.IntVar:
				self.vars[v].set(0)
			elif type(self.vars[v]) == list:
				for itr in range(0, len(self.vars[v])):
					self.vars[v][itr].set("")
		# Add source to backend list, and update the frontend
		self.parent.sourceList.allSources.append(outputVars)
		self.parent.sourceList.updateList()
		

	def _configure_interior(self, event):
		# update the scrollbars to match the size of the inner frame
		self.size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
		self.canvas.config(scrollregion="0 0 {0} {1}".format(self.size[0], self.size[1]))
		if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
			# update the canvas's width to fit the inner frame
			self.canvas.config(width=self.interior.winfo_reqwidth())


	def _configure_canvas(self, event):
		if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
			# update the inner frame's width to fill the canvas
			self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())
		
	def _on_mousewheel(self, event):
		self.canvas.yview_scroll(int(-1*(event.delta/60)), "units")


class Application(tkinter.Frame):
	def __init__(self, parent):
		tkinter.Frame.__init__(self, parent)
		self.parent = parent
		self.initialize()
		
	def initialize(self):
		self.grid()
		for r in range(6):
			self.rowconfigure(r, weight=1)	
		for c in range(5):
			self.columnconfigure(c, weight=1)

		self.sourceList = SourceList(self)
		self.sourceList.grid(row = 0, column = 0, rowspan = 3, columnspan = 2, sticky = "WENS")
		
		self.sourceDisplay = SourceDisplay(self)
		self.sourceDisplay.grid(row = 3, column = 0, rowspan = 3, columnspan = 2, sticky = "WENS")
		
		self.sourceInput = SourceInput(self)
		self.sourceInput.grid(row = 0, column = 2, rowspan = 6, columnspan = 3, sticky = "WENS")


class ErrorWindow(tkinter.Toplevel):
	# Created with: ErrorWindow(app, msg="Message"[, title="Title"[, sound=1]])
	def __init__(self, parent, msg="An unknown error occurred", title="Error", sound=1):
		tkinter.Toplevel.__init__(self, parent)
		self.parent = parent
		self.msg = msg
		self.titleText = title
		self.sound = sound
		globalbinds(0)
		self.protocol("WM_DELETE_WINDOW", self.close)
		self.escapeFuncID = self.bind_all("<Escape>", self.close)
		self.returnFuncID = self.bind_all("<Return>", self.close)
		self.initialize()
		
	def initialize(self):
		self.columnconfigure(0, weight = 1)
		self.rowconfigure(0, weight = 1)
		self.grid()
		self.errormsg = tkinter.Label(self, text = self.msg)
		self.errormsg.grid(column = 0, row = 0, padx = (10, 10), pady = (10, 10))
		
		self.okButton = tkinter.Button(self, text = "Ok", command = self.close, width = 10)
		self.okButton.grid(column = 0, row = 1, padx = (10, 10), pady = (10, 10))
		self.okButton.focus()
		
		self.title(self.titleText)
		self.minsize(200, 0)
		self.resizable(False, False)
		self.update()
		
		# Play error sound
		if self.sound == 1:
			winsound.MessageBeep()

		self.transient(self.parent) #set to be on top of the main window
		self.grab_set() #hijack all commands from the parent (clicks on the main window are ignored)
		self.parent.wait_window(self) #pause anything on the main window until this one closes (optional)
		
	def close(self, *args):
		self.unbind("<Escape>", self.escapeFuncID)
		self.unbind("<Return>", self.returnFuncID)
		globalbinds(1)
		self.destroy()

class SaveChangesPrompt(tkinter.Toplevel):
	def __init__(self, parent):
		tkinter.Toplevel.__init__(self, parent)
		self.parent = parent
		self.cancelFuncID = self.bind_all("<Escape>", self.cancel)
		self.yesFuncID = self.bind_all("<Return>", self.yes)
		globalbinds(0)
		self.initialize()
	
	def initialize(self):
		self.columnconfigure(0, weight = 1)
		self.columnconfigure(1, weight = 1)
		self.rowconfigure(0, weight = 1)
		
		self.msg = tkinter.Label(self, text = "Do you wish to save the current changes?")
		self.msg.grid(column = 0, row = 0, columnspan=2, padx = (10, 10), pady = (10, 10))

		self.yesButton = tkinter.Button(self, text = "Yes", command = self.yes, width = 10)
		self.yesButton.grid(column = 0, row = 1, padx = (10, 10), pady = (10, 10))
		self.yesButton.focus()
		
		self.noButton = tkinter.Button(self, text = "No", command = self.no, width = 10)
		self.noButton.grid(column = 1, row = 1, padx = (10, 10), pady = (10, 10))
		
		self.title("Unsaved changes")
		self.minsize(200, 0)
		self.resizable(False, False)
		self.update()
		
		self.protocol("WM_DELETE_WINDOW", self.cancel)
		
		# Play alert sound
		winsound.MessageBeep()

		self.transient(self.parent) #set to be on top of the main window
		self.grab_set() #hijack all commands from the parent (clicks on the main window are ignored)
		self.parent.wait_window(self) #pause anything on the main window until this one closes (optional)
	
	def yes(self, *args):
		global saveExitCode
		saveExitCode = 1
		self.terminate()
	
	def no(self, *args):
		global saveExitCode
		saveExitCode = -1
		self.terminate()
	
	def cancel(self, *args):
		global saveExitCode
		saveExitCode = 0
		self.terminate()
	
	def terminate(self):
		self.unbind("<Escape>", self.cancelFuncID)
		self.unbind("<Return>", self.yesFuncID)
		globalbinds(1)
		self.destroy()


class TopMenu(tkinter.Menu):
	def __init__(self, parent):
		tkinter.Menu.__init__(self, parent)
		self.parent = parent
		self.initialize(parent)
	
	def initialize(self, parent):
		self.filemenu = tkinter.Menu(self, tearoff=0)
		self.filemenu.add_command(label="Open           Ctrl+o", command=openFile)
		self.filemenu.add_command(label="Save as        Ctrl+s", command=saveFile)
		self.filemenu.add_separator()
		self.filemenu.add_command(label="Exit", command=self.exit)
		self.add_cascade(label="File", menu=self.filemenu)
		
		self.helpmenu = tkinter.Menu(self, tearoff=0)
		self.helpmenu.add_command(label="About", command=about)
		self.add_cascade(label="Help", menu=self.helpmenu)
	
	def exit(self):
		closeWindows()


def about():
	#ErrorWindow(app, msg="Remember to write the title of the publication in italic\nand to indent subsequent lines of a single source in the source list.", title="Help", sound=0)
	
	ErrorWindow(app, msg="""Remember to write the title of the publication in italic
and to indent subsequent lines of a single source in the source list.""", title="Help", sound=0)

def openFile(*args):
	"""Import pickle file to allSources"""
	# Ask to save current sources
	if saveChanges() == 0:
		return
	
	sourceLoc = os.path.dirname(os.path.realpath(__file__)) + "\\sources"
	if os.path.isdir(sourceLoc) == False:
		os.mkdir(sourceLoc)
	options = {}
	options["defaultextension"] = "*.pkl" #Is this doing anything?
	options["filetypes"] = [("Pickle files", "*.p"), ("Pickle files", "*.pkl")]
	options["multiple"] = False
	options["initialdir"] = sourceLoc
	options["parent"] = root
	options["title"] = "Open source file"
	
	filepath = filedialog.askopenfilename(**options)
	if filepath == "":
		return
	importSource = pickle.load(open(filepath, "rb"))
	
	# Check if valid list:
	# Test for a dictionary key in source
	try:
		if not "publicationType" in importSource[0]:
			ErrorWindow(app, msg="Invalid sourcefile")
			return
	except (IndexError, TypeError, KeyError, EOFError):
		ErrorWindow(app, msg="Invalid sourcefile")
		return
	
	app.sourceList.allSources = importSource
	app.sourceList.allSources_bak = app.sourceList.allSources[:]
	app.sourceList.updateList()

def saveFile(*args):
	"""Dump allSources as pickle file"""
	if app.sourceList.allSources == []: # Nothing to save
		ErrorWindow(app, msg="Nothing to save")
		return
	sourceLoc = os.path.dirname(os.path.realpath(__file__)) + "\\sources"
	if os.path.isdir(sourceLoc) == False:
		os.mkdir(sourceLoc)
	
	options = {}
	options["defaultextension"] = "*.pkl" #Is this doing anything?
	options["filetypes"] = [("Pickle files", "*.p"), ("Pickle files", "*.pkl")]
	options["initialfile"] = "source.pkl"
	options["confirmoverwrite"] = True
	options["initialdir"] = sourceLoc
	options["parent"] = root
	options["title"] = "Save source file"
	
	filepath = filedialog.asksaveasfilename(**options)
	if filepath == "":
		return
	pickle.dump(app.sourceList.allSources, open(filepath, "wb"))
	app.sourceList.allSources_bak = app.sourceList.allSources[:]

def saveChanges():
	"""Ask if user wants to save current sources"""
	if app.sourceList.allSources == []:
		return
	if app.sourceList.allSources_bak == app.sourceList.allSources:
		# Nothing has changed since last save - do not promt to save
		return
	SaveChangesPrompt(app)
	
	# This variable is set by the SaveChangesPrompt window
	# 1=save, 0=cancel, -1=don't save
	if saveExitCode == 1:
		saveFile()
	
	return saveExitCode #1=yes, 0=cancel, -1=no

def updateFormatter(*args):
	formatterKwargs = {}
	for k, v in enumerate(app.sourceInput.formatterOptions):
		formatterKwargs[v] = app.sourceInput.formatterOptions[v].get().lower()
	global MainFormatter
	MainFormatter = Formatter(**formatterKwargs)
	app.sourceDisplay.setSource(app.sourceDisplay.currSource)

def closeWindows():
	# Ask to save current sources
	if saveChanges() == 0:
		return
	root.destroy()

def globalbinds(state):
	"""Sets global keybinds active or deactive based on input"""
	global bindIDs
	if state == 1:
		bindIDs = {}
		bindIDs["save"] = root.bind_all("<Control-s>", saveFile)
		bindIDs["open"] = root.bind_all("<Control-o>", openFile)
		bindIDs["addSource"] = root.bind_all("<Return>", app.sourceInput.addSource)
	else:
		root.unbind("<Control-s>", bindIDs["save"])
		root.unbind("<Control-o>", bindIDs["open"])
		root.unbind("<Return>", bindIDs["addSource"])

if __name__ == "__main__":
	root = tkinter.Tk()
	root.columnconfigure(0, weight = 1)
	root.rowconfigure(0, weight = 1)
	menubar = TopMenu(root)
	root.config(menu=menubar)
	app = Application(root)
	app.grid(sticky = "NSEW")
	globalbinds(1)
	root.title("Source Formatting")
	root.protocol("WM_DELETE_WINDOW", closeWindows)
	root.update()
	updateFormatter()
	root.minsize(root.winfo_width(), root.winfo_height())
	root.mainloop()
