from plants_game.classes import Position, Imageposition

# параметры игрока (у нас растение)
class Plant:
	def __init__(self, img_id):
		self.pos = Position(0, 0)
		self.size_y = 8
		self.size_x = 7
		self.img_plant = img_id	
		self.get_image_front = Imageposition(25, 8)
		self.get_image_back = Imageposition(17, 8)
		self.get_image_run = Imageposition(25, 0)
		self.get_image_right = Imageposition(17, 0)
		self.get_image = self.get_image_front
		self.color_tr = 6
 
	def update(self, x, y):
		self.pos.x = x
		self.pos.y = y