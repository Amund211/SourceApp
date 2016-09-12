#This project is licensed under the terms of the GNU General Public License v3.0.
from sourceFormat import Formatter
import winsound

import tkinter
import tkinter.ttk as ttk

borderstyles = ["flat", "sunken", "raised", "groove", "ridge"]
borderstyle = borderstyles[4]
borderwidth = 2

class SourceList(tkinter.Frame):
	def __init__(self, parent):
		tkinter.Frame.__init__(self, parent)
		self.allSources = []
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
		
		self.listbox = tkinter.Listbox(self, yscrollcommand=self.scrollbar.set, height = 10, width = 100)#, selectmode = tkinter.SINGLE #idk
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
		sourceListOutput = ""
		if len(self.allSources) == 0:
			ErrorWindow(tkinter.Tk(), msg = "List is empty")
			return
		for source in self.allSources:
			sourceListOutput += MainFormatter.formatSource(**source)["full"] + "\n"
		self.clipboard_clear()
		self.clipboard_append(sourceListOutput)
	
	def editEntry(self, *args):
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
					else:
						self.parent.sourceInput.vars[key].set(self.allSources[listIndex][key])
				except (IndexError, KeyError):
					pass
			del self.allSources[listIndex]
			self.updateList()
		except IndexError:
			ErrorWindow(tkinter.Tk(), msg = "No entry selected")
	
	def deleteEntry(self):
		try:
			listIndex = self.listbox.curselection()[0]
			del self.allSources[listIndex]
			self.updateList()
		except IndexError:
			ErrorWindow(tkinter.Tk(), msg = "No entry selected")
		
	
	def onSelect(self, event):
		#Send selected source from list to sourceDisplay
		sender = event.widget
		try:
			listIndex = sender.curselection()[0]
			value = self.allSources[listIndex]
			self.parent.sourceDisplay.setSource(value)
		except IndexError:
			pass
	
	def updateList(self):
		self.displaySources = []
		#Converting dictionary allSources to list displaySources
		for dictnum, dict in enumerate(self.allSources[:]):
			self.displaySources.append([])
			for kwnum, kw in enumerate(self.allSources[dictnum]):
				if self.allSources[dictnum][kw] != "":
					self.displaySources[dictnum].append(self.allSources[dictnum][kw])

		for dictnum in range(len(self.allSources[:])-1):
			#Deleting duplicate entries
			if self.allSources[dictnum]==self.allSources[-1]:
				del(self.allSources[-1])
				del(self.displaySources[-1])
				break
			#Deleting empty entries
			if len(self.allSources[dictnum]) == 0:
				del(self.allSources[dictnum])
				del(self.displaySources[dictnum])
		
		#Populating the listbox
		self.listbox.delete(0, tkinter.END)
		for item in self.displaySources:
			self.listbox.insert(tkinter.END, item)
		
		

class SourceDisplay(tkinter.Frame):
	def __init__(self, parent):
		tkinter.Frame.__init__(self, parent)
		self.parent = parent
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
		#self.source1.insert("insert", "(a1LastName, a2LastName & a3LastName publishedYear)")
		self.source1.config(state = "disabled")
		self.source1.grid(column = 0, row = 2, padx = (10, 10), pady = (0, 10))
		
		self.copyButton = tkinter.Button(self, text = "Copy", command = self.copyShort)
		self.copyButton.grid(column = 0, row = 3)
		
		self.label2 = tkinter.Label(self, text="Citation list entry:")
		self.label2.grid(column= 0, row=4, padx = (10, 10), pady = (10, 0))
		
		self.source2 = tkinter.Text(self, height = 4, width = 75)
		#self.source2.insert("insert", "a1LastName, FN. a2LastName, FN. & a3LastName, FN. publishedYear, publicationName, publisherName, publisherLocation")
		self.source2.config(state = "disabled")
		self.source2.grid(column = 0, row = 5, padx = (10, 10), pady = (0, 10))
	
	def copyShort(self):
		self.clipboard_clear()
		self.clipboard_append(self.source1.get("1.0", "end")[:-1])
	
	def setSource(self, source):
		#Format given source and display
		formattedSource = MainFormatter.formatSource(**source)
		self.source1.config(state = "normal")
		self.source1.delete(1.0, tkinter.END)
		self.source1.insert("insert", formattedSource["short"])
		self.source1.config(state = "disabled")
		
		self.source2.config(state = "normal")
		self.source2.delete(1.0, tkinter.END)
		self.source2.insert("insert", formattedSource["full"])
		self.source2.config(state = "disabled")


class SourceInput(tkinter.Frame):
	def __init__(self, parent, *args, **kw):
		tkinter.Frame.__init__(self, parent, *args, **kw)			
		self.parent = parent
		self.initialize()
	
	def initialize(self):
		self.grid()
		self.config(borderwidth = borderwidth, relief = borderstyle)
		
		#Bind enter to add source
		self.bind_all("<Return>", self.addSource)
		
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
		
		#Bind windowconfigure to object method to handle resizing properly
		#Allow mousewheel to scroll the scrollbar
		self.interior.bind('<Configure>', self._configure_interior)
		self.canvas.bind('<Configure>', self._configure_canvas)
		self.interior.bind("<MouseWheel>", self._on_mousewheel)
		
		
		self.populate()
	
	def populate(self):
		self.varNames = ["formatStyle", "language", "publicationType", "a1FirstName", "a1LastName", "a2FirstName", "a2LastName", "a3FirstName", "a3LastName", "pageNumberRange", "publishedYear", "publicationName", "publisherName", "publisherLocation", "publicationURL", "fetchedDate"]
		self.textNames = ["Format style:", "Language:", "Publication type:", "A. 1 First name:", "A. 1 Last name:", "A. 2 First name:", "A. 2 Last name:", "A. 3 First name:", "A. 3 Last name:", "Page number/range:", "Published year:", "Publication name:", "Publisher name:", "Publisher location:", "Publication URL:", "Date fetched:"]
		#Temporary formatter to extract data
		tmpFormatter = Formatter()
		tmpFormatter.formatSource(publicationType = "book")
		###################
		self.comboboxValues = {"formatStyle" : sorted(list(item.capitalize() for item in tmpFormatter.formats)), "language" : sorted(list(item.capitalize() for item in tmpFormatter.languages)), "publicationType" : sorted(list(item.capitalize() for item in tmpFormatter.formats["harvard"]["full"])), "fetchedDay" : list(range(32)), "fetchedMonth" : list(range(13)), "fetchedYear" : [0, *list(range(2016, 2031, 1))]}
		del(tmpFormatter)
		
		if len(self.varNames) != len(self.textNames):
			raise UserWarning("varNames and textNames table pair was not equally long. (SourceInput.varNames, {0} long; SourceInput.textNames, {1} long.)".format(len(self.varNames), len(self.textNames)))
		
		#Organize widgets into a dictionary to avoid cluttering the namespace
		self.texts = {}
		self.vars = {}
		self.formatterOptions = {}
		self.widgets = {"labels" : {}, "entries" : {}, "comboboxes" : {}}
		for k, v in enumerate(self.varNames):
			if v != "fetchedDate":
				self.texts[v] = self.textNames[k]
				self.widgets["labels"][v] = tkinter.Label(self.interior, text = self.texts[v])
				self.widgets["labels"][v].grid(column = 0, row = k+1, padx = (10, 10), pady = (10, 10))
				self.widgets["labels"][v].bind("<MouseWheel>", self._on_mousewheel)
				#Do not add entry widget for the formatter options (added later)
				if k >= 3:
					self.vars[v] = tkinter.StringVar(self)
					#Debugging
					#self.vars[v].set(v)
					##########
					self.widgets["entries"][v] = tkinter.Entry(self.interior, textvar = self.vars[v])
					self.widgets["entries"][v].grid(column = 1, columnspan = 4, row = k+1, padx = (10, 10), pady = (10, 10), sticky = "EW")
					self.widgets["entries"][v].bind("<MouseWheel>", self._on_mousewheel)
				elif k == 2:
					self.vars[v] = tkinter.StringVar(self)
					#Debugging
					#self.vars[v].set(self.comboboxValues[v][0])
					##########
					self.widgets["comboboxes"][v] = ttk.Combobox(self.interior, state = "readonly", textvar = self.vars[v], values = self.comboboxValues[v], width = 15)
					self.widgets["comboboxes"][v].grid(column = 1, row = k+1, padx = (10, 10), pady = (10, 10))

				else:
					self.formatterOptions[v] = tkinter.StringVar(self)
					#Debugging
					#self.formatterOptions[v].set(self.comboboxValues[v][0])
					##########
					self.widgets["comboboxes"][v] = ttk.Combobox(self.interior, state = "readonly", textvar = self.formatterOptions[v], values = self.comboboxValues[v], width = 15)
					self.widgets["comboboxes"][v].grid(column = 1, row = k+1, padx = (10, 10), pady = (10, 10))
					
			else:
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
		
		self.button = tkinter.Button(self.interior, text = "Add source", command = self.addSource)
		self.button.grid(column = 1, row = len(self.widgets["labels"]) + 5, padx = (10, 10), pady = (10, 10))
		self.interior.columnconfigure(4, weight = 1)
		self.interior.rowconfigure(0, weight = 1)
		self.interior.rowconfigure(len(self.widgets["labels"]) + 6, weight = 1)
		
		#Default values for the formatter
		self.formatterOptions["language"].set("Norwegian")
		self.formatterOptions["formatStyle"].set("Harvard")
		#Set trace
		self.formatterOptions["language"].trace("w", updateFormatter)
		self.formatterOptions["formatStyle"].trace("w", updateFormatter)
	
	def addSource(self, *args):
		#Get data from the stringvars, and remove empty inputs
		outputVars = {}
		tmpDateFetched = [0, 0, 0]
		try:
			for k, v in enumerate(self.vars):
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
			ErrorWindow(tkinter.Tk(), msg = "Input for {} was invalid".format(v))
			return
		if 0 < tmpDateFetched[0] < 32:
			if 0 < tmpDateFetched[1] < 13:
				if tmpDateFetched[2] != 0:
					outputVars["fetchedDate"] = tuple(tmpDateFetched)
				elif tmpDateFetched[2] != 0:
					ErrorWindow(tkinter.Tk(), msg = "Input for fetched year must be type int")
					return
			elif tmpDateFetched[1] != 0:
				ErrorWindow(tkinter.Tk(), msg = "Input for fetched month must be 1-12")
				return
		elif tmpDateFetched[0] != 0:
			ErrorWindow(tkinter.Tk(), msg = "Input for fetched day must be 1-31")
			return
		
		if not "publicationType" in outputVars:
			self.canvas.yview_moveto(0)
			self.widgets["comboboxes"]["publicationType"].focus()
			ErrorWindow(tkinter.Tk(), msg = "No input given for publication type")
			return
		
		#Clear input fields
		for k, v in enumerate(self.vars):
			if type(self.vars[v]) == type(tkinter.StringVar(self)):
				self.vars[v].set("")
			elif type(self.vars[v]) == type(tkinter.IntVar(self)):
				self.vars[v].set(0)
		#Add source to backend list, and update the frontend
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

class ErrorWindow(tkinter.Frame):
	#Create errormsg by instanciating this as a child of a Tk instance
	#ErrorWindow(tkinter.Tk(), msg = "Something went wrong")
	ErrorWindows = []
	def __init__(self, parent, msg):
		tkinter.Frame.__init__(self, parent)
		self.parent = parent
		self.msg = msg
		for window in self.ErrorWindows:
			window.destroy()
			self.ErrorWindows.remove(window)
		self.ErrorWindows.append(self.parent)
		self.parent.protocol("WM_DELETE_WINDOW", self.close)
		#Prevents an errorchain when closing application after opening errormessages too quickly
		try:
			self.initialize()
		except tkinter.TclError:
			pass
	
	def initialize(self):
		self.parent.columnconfigure(0, weight = 1)
		self.parent.rowconfigure(0, weight = 1)
		self.grid()
		self.errormsg = tkinter.Label(self, text = self.msg)
		self.errormsg.grid(column = 0, row = 0, padx = (10, 10), pady = (10, 10))
		
		self.okButton = tkinter.Button(self, text = "Ok", command = self.close, width = 10)
		self.okButton.grid(column = 0, row = 1, padx = (10, 10), pady = (10, 10))
		self.parent.wm_attributes("-topmost", True)
		
		self.parent.title("Error")
		self.parent.minsize(200, 0)
		self.parent.update()
		self.parent.resizable(False, False)
		self.parent.grab_set()
		
		#Play error sound
		winsound.MessageBeep()
		
		#root.wait_window(self.parent)
		self.parent.mainloop()
	
	def close(self):
		self.ErrorWindows.remove(self.parent)
		self.parent.destroy()

def updateFormatter(*args):
	formatterKwargs = {}
	for k, v in enumerate(app.sourceInput.formatterOptions):
		formatterKwargs[v] = app.sourceInput.formatterOptions[v].get().lower()
	global MainFormatter
	MainFormatter = Formatter(**formatterKwargs)
	app.sourceList.updateList()

def closeWindows():
	for window in ErrorWindow.ErrorWindows:
		window.destroy()
		ErrorWindow.ErrorWindows.remove(window)
	root.destroy()

if __name__ == "__main__":
	root = tkinter.Tk()
	root.columnconfigure(0, weight = 1)
	root.rowconfigure(0, weight = 1)
	app = Application(root)
	app.grid(sticky = "NSEW")
	root.title("Source Formatting")
	root.protocol("WM_DELETE_WINDOW", closeWindows)
	root.update()
	updateFormatter()
	root.minsize(root.winfo_width(), root.winfo_height())
	#root.iconify()
	root.mainloop()
