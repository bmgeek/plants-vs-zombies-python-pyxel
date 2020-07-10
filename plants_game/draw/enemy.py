import random

from plants_game.classes import Position, Imageposition

# параметры противника (у нас зомбаки)
class Zombie:
	def __init__(self, img_id):
		zombie_view = random.choice(ZOMBIES_PARAMS)
		self.pos = Position(0, 0)
		self.size_y = zombie_view["size_y"]
		self.size_x = zombie_view["size_x"]
		self.speed = -0.2
		self.img_plant = img_id		
		self.get_image = Imageposition(zombie_view["x"], zombie_view["y"])
		self.color_tr = 2
		self.health = Health()
		self.current_health = zombie_view["health"]
		self.points = self.current_health
		self.archer = zombie_view["archer"]
		self.health_index_pos_x = (zombie_view["size_x"] - zombie_view["health"]) / 2
 
	def update(self, x, y, health_x, health):
		self.pos.x = x
		self.pos.y = y
		self.current_health = health
		self.health.update(from_x=x+health_x, from_y=y-2, to_x=x+health+health_x, to_y=y-2)

class Health:
	def __init__(self):
		self.pos = Position(0, 0)
		self.to_pos = Position(0, 0)
		self.color = 8

	def update(self, from_x, from_y, to_x, to_y):
		self.pos.x = from_x
		self.pos.y = from_y
		self.to_pos.x = to_x
		self.to_pos.y = to_y

ZOMBIES_PARAMS = [
	{
		"x": 0,
		"y": 16,
		"size_y": 10,
		"size_x": 7,
		"health": random.choice([3,4,5]),
		"archer": False
	},
	{
		"x": 10,
		"y": 16,
		"size_y": 10,
		"size_x": 6,
		"health": 2,
		"archer": False
	},
	{
		"x": 0,
		"y": 32,
		"size_y": 10,
		"size_x": 6,
		"health": random.choice([1,2]),
		"archer": False
	},
	{
		"x": 8,
		"y": 32,
		"size_y": 10,
		"size_x": 8,
		"health": random.choice([1,2]),
		"archer": True
	}
]