#This project is licensed under the terms of the GNU General Public License v3.0.
from sourceFormat import Formatter

import tkinter
import tkinter.ttk as ttk

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
		
		self.source1 = tkinter.Text(self, height = 1, width = 75)
		self.source1.insert("insert", "(a1LastName, a2LastName & a3LastName publishedYear)")
		self.source1.config(state = "disabled")
		self.source1.grid(column = 0, row = 2, padx = (10, 10), pady = (0, 10))
		
		self.label2 = tkinter.Label(self, text="Citation list entry:")
		self.label2.grid(column= 0, row=3, padx = (10, 10), pady = (10, 0))
		
		self.source2 = tkinter.Text(self, height = 4, width = 75)
		self.source2.insert("insert", "a1LastName, FN. a2LastName, FN. & a3LastName, FN. publishedYear, publicationName, publisherName, publisherLocation")
		self.source2.config(state = "disabled")
		self.source2.grid(column = 0, row = 4, padx = (10, 10), pady = (0, 10))
		

class Application(tkinter.Frame):
	def __init__(self, parent):
		tkinter.Frame.__init__(self, parent)
		self.parent = parent
		self.initialize()
		
	def initialize(self):
		self.grid()
		for r in range(6):
			self.parent.rowconfigure(r, weight=1)	
		for c in range(5):
			self.parent.columnconfigure(c, weight=1)

		self.Frame1 = tkinter.Frame(self.parent, bg="red")
		self.Frame1.grid(row = 0, column = 0, rowspan = 3, columnspan = 2, sticky = "WENS")
		
		#self.Frame2 = tkinter.Frame(self.parent, bg="blue")
		self.Frame2 = SourceDisplay(self.parent)
		self.Frame2.grid(row = 3, column = 0, rowspan = 3, columnspan = 2, sticky = "WENS")
		
		self.Frame3 = tkinter.Frame(self.parent, bg="green")
		self.Frame3.grid(row = 0, column = 2, rowspan = 6, columnspan = 3, sticky = "WENS")

if __name__ == "__main__":
	root = tkinter.Tk()
	app = Application(root)
	root.title("Test layout")
	#root.geometry(root.geometry())
	root.minsize(root.winfo_width(), root.winfo_height())
	root.mainloop()