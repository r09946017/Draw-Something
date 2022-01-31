from PIL import Image

COLORS = [
	("black", (0, 0, 0)),
	("white", (255, 255, 255)),
	("red", (255, 0, 0)),
	("orange", (255, 127, 0)),
	("yellow", (255, 255, 0)),
	("green", (0, 255, 0)),
	("blue", (0, 0, 255)),
	("indigo", (75, 0, 130)),
	("violet", (148, 0, 211))
] 

for name, color in COLORS:
	im = Image.new("RGB", (25, 25), color)
	im.save(f"{name}.gif")
