import sfml as sf

class Food:

	def __init__(self, x, array):

		self.pos = (x, 26)

		self.foodShape = sf.RectangleShape((10, 10))

		self.foodShape.fill_color = sf.Color(195, 132, 163)

		self.foodShape.position = (self.pos[0] * 10, self.pos[1] * 10) 
		
		array[x][26] = 5
