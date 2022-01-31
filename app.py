from tkinter import *
import tkinter.messagebox
from PIL import ImageGrab
import random

LINE, RECTANGLE, OVAL, PENCIL, BRUSH, ERASER = list(range(6))

class Board:

	def __init__(self, canvas):
		self._canvas = canvas
		self._canvas.bind("<Button-1>", self.click)
		self._canvas.bind("<B1-Motion>", self.draw)
		
		self._tool, self._color, self._fill, self._width = None, None, None, None
		self._last_x, self._last_y = None, None
		self._obj = None

	def select(self, type, selection):
		if type == "Tool":
			self._tool = selection
		elif type == "Color":
			self._color = selection
		elif type == "Fill":
			self._fill = selection
		else:
			self._width = selection

	def click(self, event):
		if self._tool is None:
			return

		if self._color is None:
			self._color = "#000000"

		if self._width is None:
			self._width = 5

		x, y = event.x, event.y
		if self._tool == LINE:
			self._obj = self._canvas.create_line((x, y, x, y), fill = self._color, width = self._width)
		elif self._tool == RECTANGLE:
			if self._fill == True:
				self._obj = self._canvas.create_rectangle((x, y, x, y), outline = self._color, fill = self._color, width = self._width)
			else:
				self._obj = self._canvas.create_rectangle((x, y, x, y), outline = self._color, width = self._width)
		elif self._tool == OVAL:
			if self._fill == True:
				self._obj = self._canvas.create_oval((x, y, x, y), outline = self._color, fill = self._color, width = self._width)
			else:
				self._obj = self._canvas.create_oval((x, y, x, y), outline = self._color, width = self._width)

		self._last_x, self._last_y = x, y
		return

	def draw(self, event):
		if self._tool is None:
			return

		if self._color is None:
			self._color = "#000000"

		if self._width is None:
			self._width = 5

		x, y = self._last_x, self._last_y
		if self._tool in (LINE, RECTANGLE, OVAL):
			self._canvas.coords(self._obj, (x, y, event.x, event.y))
		elif self._tool == PENCIL:
			self._canvas.create_line(x, y, event.x, event.y, fill = self._color, width = self._width)
			self._last_x, self._last_y = event.x, event.y
		elif self._tool == BRUSH:
			if self._width is None:
				x1, y1 = (event.x - 5), (event.y - 5)
				x2, y2 = (event.x + 5), (event.y + 5)
			else:
				x1, y1 = (event.x - self._width), (event.y - self._width)
				x2, y2 = (event.x + self._width), (event.y + self._width)
			self._canvas.create_rectangle(x1, y1, x2, y2, outline = self._color, fill = self._color)
			self._last_x, self._last_y = event.x, event.y
		else:
			if self._width is None:
				x1, y1 = (event.x - 5), (event.y - 5)
				x2, y2 = (event.x + 5), (event.y + 5)
			else:
				x1, y1 = (event.x - self._width), (event.y - self._width)
				x2, y2 = (event.x + self._width), (event.y + self._width)
			self._canvas.create_rectangle(x1, y1, x2, y2, outline = "#ffffff", fill = "#ffffff")
			self._last_x, self._last_y = event.x, event.y
		return

class Painter:

	def __init__(self, board):
		self._board = board

		### Load images for icons
		# --- TOOLS ---
		self.pencil = PhotoImage(file = "Image/Tool/pencil.gif")
		self.brush = PhotoImage(file = "Image/Tool/brush.gif")
		self.eraser = PhotoImage(file = "Image/Tool/eraser.gif")
		self.line = PhotoImage(file = "Image/Tool/line.gif")
		self.rectangle = PhotoImage(file = "Image/Tool/rectangle.gif")
		self.oval = PhotoImage(file = "Image/Tool/oval.gif")

		TOOLS = [
			(self.line, LINE),
			(self.rectangle, RECTANGLE),
			(self.oval, OVAL),
			(self.pencil, PENCIL),
			(self.brush, BRUSH),
			(self.eraser, ERASER)
		]

		# --- COLORS ---
		self.black = PhotoImage(file = "Image/Color/black.gif")
		self.white = PhotoImage(file = "Image/Color/white.gif")
		self.red = PhotoImage(file = "Image/Color/red.gif")
		self.orange = PhotoImage(file = "Image/Color/orange.gif")
		self.yellow = PhotoImage(file = "Image/Color/yellow.gif")
		self.green = PhotoImage(file = "Image/Color/green.gif")
		self.blue = PhotoImage(file = "Image/Color/blue.gif")
		self.indigo = PhotoImage(file = "Image/Color/indigo.gif")
		self.violet = PhotoImage(file = "Image/Color/violet.gif")

		COLORS = [
			(self.black, "#000000"),
			(self.white, "#FFFFFF"),
			(self.red, "#FF0000"),
			(self.orange, "#FF7F00"),
			(self.yellow, "#FFFF00"),
			(self.green, "#00FF00"),
			(self.blue, "#0000FF"),
			(self.indigo, "#4B0082"),
			(self.violet, "#9400D3")
		]

		# --- WIDTH ---
		self.one = PhotoImage(file = "Image/Width/1.gif")
		self.two = PhotoImage(file = "Image/Width/2.gif")
		self.three = PhotoImage(file = "Image/Width/3.gif")
		self.four = PhotoImage(file = "Image/Width/4.gif")
		self.five = PhotoImage(file = "Image/Width/5.gif")
		self.six = PhotoImage(file = "Image/Width/6.gif")

		WIDTH = [
			(self.one, 1),
			(self.two, 3),
			(self.three, 5),
			(self.four, 10),
			(self.five, 15),
			(self.six, 20)
		]

		# --- FILE ---
		self.open = PhotoImage(file = "Image/Other/word.gif")
		self.save = PhotoImage(file = "Image/Other/save.gif")

		self.word_list = open("words.txt", "r").read().strip().split(" ")
		self.word = None
	
		### Frames
		frame1 = Frame(None, width = 40)
		frame2 = Frame(None, width = 40)
		frame1.pack_propagate(False)
		frame2.pack_propagate(False)

		### Put icons
		for img, name in TOOLS:
			label = Label(frame1, image = img, relief = "raised")
			label._type = "Tool"
			label._selection = name
			label.bind("<Button-1>", self.update)
			label.pack(padx = 6, pady = 3)

		# Add spaces 
		space = Label(frame1, image = self.white)
		space.pack(padx = 6, pady = 3)

		for img, value in WIDTH:
			label = Label(frame1, image = img, relief = "raised")
			label._type = "Width"
			label._selection = value
			label.bind("<Button-1>", self.update)
			label.pack(padx = 6, pady = 3)

		# Add spaces 
		space = Label(frame1, image = self.white)
		space.pack(padx = 6, pady = 3)

		label = Label(frame1, image = self.open, relief = "raised")
		label.bind("<Button-1>", self.random_word)
		label.pack(padx = 6, pady = 3)

		label = Label(frame1, image = self.save, relief = "raised")
		label.bind("<Button-1>", self.save_image)
		label.pack(padx = 6, pady = 3)

		frame1.pack(pady = 6, side = "left", fill = "y", expand = True)		
		for img, code in COLORS:
			label = Label(frame2, image = img, relief = "raised")
			label._type = "Color"
			label._selection = code
			label.bind("<Button-1>", self.update)
			label.pack(padx = 6, pady = 3)

		frame2.pack(pady = 6, side = "left", fill = "y", expand = True)

	def update(self, event):
		label = event.widget
		self._board.select(label._type, label._selection)

	def random_word(self, event):
		### Message box looks weird on Mac M1
		self.word = random.choice(self.word_list)
		tkinter.messagebox.showinfo("Draw Something", f"Please draw {self.word}")

	def save_image(self, event):
		### PIL only work on specific resolution 
		x1 = self._board._canvas.winfo_rootx()
		y1 = self._board._canvas.winfo_rooty()
		x2 = x1 + (int)(self._board._canvas.winfo_width() * 2.15)
		y2 = y1 + (int)(self._board._canvas.winfo_height() * 2.15)
		im = ImageGrab.grab().crop((x1, y1, x2, y2))
		im.save(f"output/{self.word}.png")

_ = Tk()
_.title("Little Painter")
_.geometry("900x640+0+0")
_.resizable(width = False, height = False)
canvas = Canvas(highlightbackground = "black", width = 800, height = 600)
board = Board(canvas)
painter = Painter(board)
canvas.pack(padx = 6, pady = 6, fill = "both", expand = True)
_.mainloop()


