#This project is licensed under the terms of the GNU General Public License v3.0.
from sourceFormat import Formatter

import tkinter
import tkinter.ttk as ttk

class SourceList(tkinter.Frame):
	def __init__(self, parent):
		tkinter.Frame.__init__(self, parent)
		self.allSources = []
		self.displaySources = []
		self.parent = parent
		self.parent.parent.bind("<<ListboxSelect>>", self.onSelect)
		self.initialize()
	
	def initialize(self):
		self.grid()
		
		self.columnconfigure(0, weight = 1)
		self.columnconfigure(1, weight = 0)
		self.columnconfigure(2, weight = 0)
		self.columnconfigure(3, weight = 1)
		
		self.rowconfigure(0, weight = 1)
		self.rowconfigure(1, weight = 0)
		self.rowconfigure(2, weight = 1)
		
		self.scrollbar = tkinter.Scrollbar(self)
		self.scrollbar.grid(row = 1, column = 2, sticky = "NS")
		self.listbox = tkinter.Listbox(self, yscrollcommand=self.scrollbar.set, height = 10, width = 100)#, selectmode = tkinter.SINGLE #idk
		self.listbox.grid(row = 1, column = 1, padx = (10, 10,), pady = (10, 10,))
		
		self.scrollbar.config(command = self.listbox.yview)
	
	def onSelect(self, event):
		#Send selected source from list to sourceDisplay
		sender = event.widget
		listIndex = sender.curselection()
		value = sender.get(listIndex)
		self.parent.sourceDisplay.setSource(value)
	
	def updateList(self):
		self.displaySources = []
		#Converting dictionary allSources to list displaySources
		for dictnum, dict in enumerate(self.allSources):
			self.displaySources.append([])
			for kwnum, kw in enumerate(self.allSources[dictnum]):
				if self.allSources[dictnum][kw] != "":
					self.displaySources[dictnum].append(self.allSources[dictnum][kw])
		#Deleting empty entries
		if len(self.allSources[dictnum]) == 0:
			del(self.allSources[dictnum])
			del(self.displaySources[dictnum])
		#Deleting duplicate entries
		for dictnum in range(len(self.allSources)-1):
			if self.allSources[dictnum]==self.allSources[-1]:
				del(self.allSources[-1])
				del(self.displaySources[-1])
				break
		
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
		
		self.columnconfigure(0, weight = 1)
		self.rowconfigure(0, weight = 1)
		self.rowconfigure(5, weight = 1)
		
		self.label1 = tkinter.Label(self, text="In text citation:")
		self.label1.grid(column = 0, row = 1, padx = (10, 10), pady = (10, 0))
		
		self.source1 = tkinter.Text(self, height = 1, width = 50)
		self.source1.insert("insert", "(a1LastName, a2LastName & a3LastName publishedYear)")
		self.source1.config(state = "disabled")
		self.source1.grid(column = 0, row = 2, padx = (10, 10), pady = (0, 10))
		
		self.label2 = tkinter.Label(self, text="Citation list entry:")
		self.label2.grid(column= 0, row=3, padx = (10, 10), pady = (10, 0))
		
		self.source2 = tkinter.Text(self, height = 4, width = 75)
		self.source2.insert("insert", "a1LastName, FN. a2LastName, FN. & a3LastName, FN. publishedYear, publicationName, publisherName, publisherLocation")
		self.source2.config(state = "disabled")
		self.source2.grid(column = 0, row = 4, padx = (10, 10), pady = (0, 10))
	
	def setSource(self, source):
		#Create temporary formatter object, and format given source
		#Lower inputs for formatter, as they are capitalized in the combobox
		pass


class SourceInput(tkinter.Frame):
	def __init__(self, parent, *args, **kw):
		tkinter.Frame.__init__(self, parent, *args, **kw)			
		self.parent = parent
		self.initialize()
	
	def initialize(self):
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
		#self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
		self.bind("<MouseWheel>", self._on_mousewheel)
		self.canvas.bind("<MouseWheel>", self._on_mousewheel)
		self.interior.bind("<MouseWheel>", self._on_mousewheel)
		
		
		self.populate()
	
	def populate(self):
		self.varNames = ["a1FirstName", "a1LastName", "a2FirstName", "a2LastName", "a3FirstName", "a3LastName", "pageNumberRange", "publishedYear", "publicationName", "publisherName", "publisherLocation", "publicationURL", "fetchedDate"]
		self.textNames = ["A. 1 First name:", "A. 1 Last name:", "A. 2 First name:", "A. 2 Last name:", "A. 3 First name:", "A. 3 Last name:", "Page number/range:", "Published year:", "Publication name:", "Publisher name:", "Publisher location:", "Publication URL:", "Date fetched:"]
		self.comboboxValues = {"formatStyle" : ["Harvard"], "language" : ["Norwegian", "English"], "publicationType" : ["Book", "Webpage"], "fetchedDay" : list(range(32)), "fetchedMonth" : list(range(13)), "fetchedYear" : [0, *list(range(2016, 2031, 1))]}
		
		self.formatterOptions = {}
		self.formatterOptions["formatStyle"] = tkinter.StringVar()
		self.formatterOptions["language"] = tkinter.StringVar()
		self.formatterOptions["publicationType"] = tkinter.StringVar()

		if len(self.varNames) != len(self.textNames):
			raise UserWarning("varNames and textNames table pair was not equally long. (SourceInput.varNames, {0} long; SourceInput.textNames, {1} long.)".format(len(self.varNames), len(self.textNames)))
		
		#Organize widgets into a dictionary to avoid cluttering the namespace
		self.texts = {}
		self.vars = {}
		self.widgets = {"labels" : {}, "entries" : {}, "comboboxes" : {}, "labels2" : {}}
		for k, v in enumerate(self.varNames):
			if v != "fetchedDate":
				self.vars[v] = tkinter.StringVar(self)
				self.texts[v] = self.textNames[k]
				self.widgets["labels"][v] = tkinter.Label(self.interior, text = self.texts[v]).grid(column = 0, row = k+4, padx = (10, 10), pady = (10, 10))
				#if k<=2: dont add entry, k+1 instead of k+4
				#Also add 0,2 label text in texts
				self.widgets["entries"][v] = tkinter.Entry(self.interior, textvar = self.vars[v]).grid(column = 1, columnspan = 4, row = k+4, padx = (10, 10), pady = (10, 10), sticky = "EW")
			else:
				self.vars["fetchedDay"] = tkinter.IntVar(self)
				self.vars["fetchedMonth"] = tkinter.IntVar(self)
				self.vars["fetchedYear"] = tkinter.IntVar(self)
				self.texts[v] = self.textNames[k]
				self.widgets["entries"][v] = tkinter.Label(self.interior, text = self.texts[v]).grid(column = 0, row = k+4, padx = (10, 0), pady = (10, 10))
				self.widgets["comboboxes"]["fetchedDay"] = ttk.Combobox(self.interior, textvar = self.vars["fetchedDay"], values = self.comboboxValues["fetchedDay"], width = 2).grid(column = 1, row = k+4, padx = (0, 1), pady = (10, 10), sticky = "E")
				self.widgets["comboboxes"]["fetchedMonth"] = ttk.Combobox(self.interior, textvar = self.vars["fetchedMonth"], values = self.comboboxValues["fetchedMonth"], width = 2).grid(column = 2, row = k+4, padx = (1, 1), pady = (10, 10), sticky = "W")
				self.widgets["comboboxes"]["fetchedYear"] = ttk.Combobox(self.interior, textvar = self.vars["fetchedYear"], values = self.comboboxValues["fetchedYear"], width = 4).grid(column = 3, row = k+4, padx = (1, 10), pady = (10, 10), sticky = "W")
		
		#for k, v in enumerate(self.formatterOptions):
			self.widgets["labels2"]["formatStyle"] = tkinter.Label(self.interior, text = "Format style:").grid(column = 0, row = 1, padx = (10, 10), pady = (10, 10))
			self.widgets["comboboxes"]["formatStyle"] = ttk.Combobox(self.interior, textvar = self.formatterOptions["formatStyle"], values = self.comboboxValues["formatStyle"], width = 15).grid(column = 1, row = 1, padx = (10, 10), pady = (10, 10))
			self.widgets["labels2"]["language"] = tkinter.Label(self.interior, text = "Language:").grid(column = 0, row = 2, padx = (10, 10), pady = (10, 10))
			self.widgets["comboboxes"]["language"] = ttk.Combobox(self.interior, textvar = self.formatterOptions["language"], values = self.comboboxValues["language"], width = 15).grid(column = 1, row = 2, padx = (10, 10), pady = (10, 10))
			self.widgets["labels2"]["publicationType"] = tkinter.Label(self.interior, text = "Publication type:").grid(column = 0, row = 3, padx = (10, 10), pady = (10, 10))
			self.widgets["comboboxes"]["publicationType"] = ttk.Combobox(self.interior, textvar = self.formatterOptions["publicationType"], values = self.comboboxValues["publicationType"], width = 15).grid(column = 1, row = 3, padx = (10, 10), pady = (10, 10))

		self.button = tkinter.Button(self.interior, text = "Add source", command = self.addSource)
		self.button.grid(column = 1, row = len(self.widgets["labels"]) + 5, padx = (10, 10), pady = (10, 10))
		#self.interior.columnconfigure(0, weight = 1)
		#self.interior.columnconfigure(1, weight = 1)
		self.interior.columnconfigure(4, weight = 1)
		#self.interior.columnconfigure(3, weight = 1)
		self.interior.rowconfigure(0, weight = 1)
		self.interior.rowconfigure(len(self.widgets["labels"]) + 6, weight = 1)
	
	def addSource(self):
		#Get data from the stringvars, and remove empty inputs
		outputVars = {}
		tmpDateFetched = [0, 0, 0]
		for k, v in enumerate(self.vars):
			if self.vars[v].get() != "":
				if v == "fetchedDay":
					tmpDateFetched[0] = self.vars[v].get()
				elif v == "fetchedMonth":
					tmpDateFetched[1] = self.vars[v].get()
				elif v == "fetchedYear":
					tmpDateFetched[2] = self.vars[v].get()
				else:
					outputVars[v] = self.vars[v].get()
		if tmpDateFetched != [0, 0, 0]:
			outputVars["fetchedDate"] = tuple(tmpDateFetched)
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

if __name__ == "__main__":
	root = tkinter.Tk()
	root.columnconfigure(0, weight = 1)
	root.rowconfigure(0, weight = 1)
	app = Application(root)
	app.grid(sticky = "NSEW")
	root.title("Test layout")
	#root.geometry(root.geometry())
	root.update()
	root.minsize(root.winfo_width(), root.winfo_height())
	root.mainloop()
		