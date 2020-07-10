from plants_game.classes import Position, Imageposition


# патрон к оружию
class Patron:
	def __init__(self, img_id):
		self.pos = Position(15, 115)
		self.get_image = Imageposition(18, 19)
		self.img_patron = img_id	
		self.size_x = 4
		self.size_y = 5
		self.color_tr = 6

	def update(self, x, y):
		self.pos.x = x
		self.pos.y = y

# обрез
class Shotgun:
	def __init__(self, img_id):
		self.pos = Position(x=3, y=112)
		self.get_image = Imageposition(16, 27)
		self.img_shotgun = img_id	
		self.size_x = 15
		self.size_y = 5
		self.color_tr = 6

	def update(self, x, y):
		self.pos.x = x
		self.pos.y = y

# параметры стены
class Wall:
	def __init__(self, x, y):
		self.pos = Position(x, y)
		self.size_x = 135
		self.size_y = 15

# параметры патрона (в нашем случае шара)
class Ball:
	def __init__(self):
		self.pos = Position(0, 0)
		self.size = 2
		self.speed = 3
		self.color = 11

	def update(self, x, y, size, color):
		self.pos.x = x
		self.pos.y = y
		self.size = size
		self.color = color