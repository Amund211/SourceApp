#This project is licensed under the terms of the GNU General Public License v3.0.
from sourceFormat import Formatter

import tkinter
import tkinter.ttk as ttk

class SourceList(tkinter.Frame):
	def __init__(self, parent):
		tkinter.Frame.__init__(self, parent)
		self.allSources = []
		self.parent = parent
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
		
		
		self.listbox = tkinter.Listbox(self, yscrollcommand=self.scrollbar.set, height = 10, width = 100)
		self.listbox.grid(row = 1, column = 1, padx = (10, 10,), pady = (10, 10,))
		
		for i in range(100):
			self.listbox.insert(tkinter.END, "Entry nr. " + str(i))
		
		self.scrollbar.config(command = self.listbox.yview)
		
		

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


class SourceInput(tkinter.Frame):
	"""A pure Tkinter scrollable frame that actually works!

	* Use the 'interior' attribute to place widgets inside the scrollable frame
	* Construct and pack/place/grid normally
	* This frame only allows vertical scrolling
	
	"""
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
		self.label1 = tkinter.Label(self.interior, text = "Label 1:")
		self.label2 = tkinter.Label(self.interior, text = "Label 2:")
		self.label3 = tkinter.Label(self.interior, text = "Label 3:")
		self.label4 = tkinter.Label(self.interior, text = "Label 4:")
		self.label1.grid(column = 1, row = 0, padx = (10, 10), pady = (10, 10))
		self.label2.grid(column = 1, row = 1, padx = (10, 10), pady = (10, 10))
		self.label3.grid(column = 1, row = 2, padx = (10, 10), pady = (10, 10))
		self.label4.grid(column = 1, row = 3, padx = (10, 10), pady = (10, 10))
		
		self.entryVar1 = tkinter.StringVar()
		self.entry1 = tkinter.Entry(self.interior, textvar = self.entryVar1)
		self.entry1.grid(column = 2, row = 3, padx = (10, 10), pady = (10, 10), sticky = "EW")
		#for i in range(5, 100):
		#	tkinter.Entry(self.interior, width = 20).grid(column = 0, row = i, sticky = "EW")
		

		
		self.interior.columnconfigure(0, weight = 1)
		self.interior.columnconfigure(2, weight = 4)
		self.interior.columnconfigure(3, weight = 1)
		self.interior.rowconfigure(0, weight = 1)
		self.interior.rowconfigure(1, weight = 1)
		self.interior.rowconfigure(0, weight = 1)
		self.interior.rowconfigure(100, weight = 1)
		

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
			self.parent.rowconfigure(r, weight=1)	
		for c in range(5):
			self.parent.columnconfigure(c, weight=1)

		#self.Frame1 = tkinter.Frame(self.parent, bg="red")
		self.Frame1 = SourceList(self.parent)
		self.Frame1.grid(row = 0, column = 0, rowspan = 3, columnspan = 2, sticky = "WENS")
		
		#self.Frame2 = tkinter.Frame(self.parent, bg="blue")
		self.Frame2 = SourceDisplay(self.parent)
		self.Frame2.grid(row = 3, column = 0, rowspan = 3, columnspan = 2, sticky = "WENS")
		
		#self.Frame3 = tkinter.Frame(self.parent, bg="green")
		self.Frame3 = SourceInput(self.parent)
		self.Frame3.grid(row = 0, column = 2, rowspan = 6, columnspan = 3, sticky = "WENS")

if __name__ == "__main__":
	root = tkinter.Tk()
	app = Application(root)
	root.title("Test layout")
	#root.geometry(root.geometry())
	root.update()
	root.minsize(root.winfo_width(), root.winfo_height())
	root.mainloop()