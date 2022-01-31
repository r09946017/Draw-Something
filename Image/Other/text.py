from PIL import Image, ImageDraw

TEXT = [
	("word", "word"),
	("save", "save"),
]

for name, text in TEXT:
	im = Image.new("RGB", (25, 25), (255, 255, 255))
	draw = ImageDraw.Draw(im)
	w, h = draw.textsize(text)
	draw.text(((25 - w) / 2, (25 - h) / 2), text, fill = "black")
	im.save(f"{name}.gif")
