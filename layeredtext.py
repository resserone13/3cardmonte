


def layered_text(self, text, font, size, x, y, x_offset, y_offset, *colors, **kwargs):
	
	
	colors = [*colors]
	for color in colors:
		name = LabelNode(
			text, 
			font = (font, size), 
			position = (x, y), 
			color = color, 
			parent=self, 
			)
			
		x += x_offset
		y += y_offset


#
