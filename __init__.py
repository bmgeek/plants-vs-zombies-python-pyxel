import pyxel, random

# используем во всех классах в качестве определения позиции
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# используем tilemap, вытаскиваем картинку по позиции x,y (пиксели)
class Imageposition:
    def __init__(self, x, y):
        self.pos = Position(x, y)

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

# параметры противника (у нас зомбаки)
class Zombie:
	def __init__(self, img_id):
		self.pos = Position(0, 0)
		self.size_y = 10
		self.size_x = 7
		self.speed = -0.2
		self.img_plant = img_id		
		self.get_image = Imageposition(0, 16)
		self.color_tr = 2
 
	def update(self, x, y):
		self.pos.x = x
		self.pos.y = y
 
# параметры игрока (у нас растение)
class Plant:
	def __init__(self, img_id):
		self.pos = Position(0, 0)
		self.size_y = 8
		self.size_x = 12
		self.img_plant = img_id	
		self.get_image = Imageposition(0, 0)
		self.color_tr = 7
 
	def update(self, x, y):
		self.pos.x = x
		self.pos.y = y

# главный класс игры
class App:
	def __init__(self):
		self.IMG_ID0 = 0		# ID картинки (требуется по документации)
		self.WINDOW_W = 160		# ширина окна
		self.WINDOW_H = 120		# высота окна

		# инициализируем окно и выставляем заголовок
		pyxel.init(self.WINDOW_W, self.WINDOW_H, caption="BmGeek, Youtube!")
		pyxel.load("my_resource.pyxres")		# загружаем tilemap
		pyxel.image(1).load(0, 0, "arena.png")	# загружаем бэкграунд

		self.plant = Plant(self.IMG_ID0)	# определяем игрока из класса
		self.plant.pos.x = 8				# позиция игрока по Х координате
		self.plant.pos.y = 52				# позиция игрока по У координате
		
		self.Balls = []		# список с шарами, которые должны быть отображены на экране
		self.Walls = [		# список со стенками на арене
			Wall(20, 15),
			Wall(20, 39),
			Wall(20, 63),
			Wall(20, 87)
		]
		self.Zombies = []	# список с зомбаками

		#  запускаем отрисовку игрульки
		pyxel.run(self.update, self.draw)

	# функция отвечает за определение координат всего, что есть и движется на экране
	def update(self):
		if pyxel.btnp(pyxel.KEY_Q):			# если кнопка Q нажата, то выходим из игры
			pyxel.quit()

		# изменение позиций игрока при нажатии кнопок W или S, т.е ходим вверх или вниз
		if self.plant.pos.y-4 > 0 and pyxel.btn(pyxel.KEY_W):
			self.plant.update(self.plant.pos.x, self.plant.pos.y-3)	
		if self.plant.pos.y+16 < self.WINDOW_H and pyxel.btn(pyxel.KEY_S):
			self.plant.update(self.plant.pos.x, self.plant.pos.y+3)

		ball_count = len(self.Balls)		# кол-во шаров на экране
		zombie_count = len(self.Zombies)	# кол-во зомби на экране

		# создаем противника Зомби. Должно быть на экране не больше трех штук в один момент времени
		if zombie_count < 3:
			# рандомно генерируем зомби на карте
			# создание нового объекта Зомби
			new_zombie = Zombie(self.IMG_ID0)
			# устанавливаем позицию нового объекта зомби
			new_zombie.update(self.WINDOW_W+random.choice(range(0, 10)), random.choice(self.Walls).pos.y-random.choice(range(8, 13)))
			# добавляем новый объект зомби в список всех зомбаков
			self.Zombies.append(new_zombie)
		
		# заставляем ходить зомби по экрану
		for zombie in range(zombie_count):
			self.Zombies[zombie].update(self.Zombies[zombie].pos.x + self.Zombies[zombie].speed, self.Zombies[zombie].pos.y)

		# при нажатии кнопки D вылетает шар, всего на экране не должно быть больше 3 шаров
		if pyxel.btnp(pyxel.KEY_D) and ball_count < 3:
			new_ball = Ball()	# создаем новый экзмепляр класса шара
			# определяем начальную позицию шара
			new_ball.update(self.plant.pos.x + self.plant.size_x/2 + 6, self.plant.pos.y + self.plant.size_y/2, new_ball.size, new_ball.color)
			# добавляем шар в список шаров
			self.Balls.append(new_ball)

		# проверяем положение шара на экране. Шар должен исчезнуть при столкновении с объектом
		for i in range(ball_count):
			# если позиция шара не в начале и конце экрана, то пусть летит
			if self.Balls[i].pos.x > 0 and self.Balls[i].pos.x < self.WINDOW_W:
				# заставляем шар лететь по экрану
				self.Balls[i].update(self.Balls[i].pos.x + self.Balls[i].speed, self.Balls[i].pos.y, self.Balls[i].size, self.Balls[i].color)
				try:
					if self.kill_wall(i):	# если шар столкнулся со стеной, то удалить шар и прервать цикл
						break
				except:
					pass
				try:
					if self.kill_zombie(i):	# если шар столкнулся с зомби, то удалить зомби и шар и прервать цикл
						break
				except:
					pass
			else:
				del self.Balls[i]
				break

	# отрисовка всех объектов на экране
	def draw(self):
		pyxel.cls(0) # очищаем экран, выставляем ему черный цвет (цвет можно поменять)
		pyxel.blt(0, 0, 1, 0, 0, 160, 120, 0)	# отрисовываем бэкграунд (само поле)
		# отрисовка игрока
		pyxel.blt(self.plant.pos.x, self.plant.pos.y, self.plant.img_plant, self.plant.get_image.pos.x, self.plant.get_image.pos.y, self.plant.size_x, self.plant.size_y, self.plant.color_tr)
		
		# отрисовка всех зомби
		for zombie in self.Zombies:
			pyxel.blt(zombie.pos.x, zombie.pos.y, zombie.img_plant, zombie.get_image.pos.x, zombie.get_image.pos.y, zombie.size_x, zombie.size_y, zombie.color_tr)

		# отрисовка всех шаров
		for ball in self.Balls:
			pyxel.circ(ball.pos.x, ball.pos.y, ball.size, ball.color)

	# при столконовении шара с зомби, удаляем шар и зомби
	def kill_zombie(self, ball_index):
		for zombie in range(len(self.Zombies)):
			if (self.Balls[ball_index].pos.x in range(int(self.Zombies[zombie].pos.x), int(self.Zombies[zombie].pos.x) + self.Zombies[zombie].size_x)
			and self.Balls[ball_index].pos.y in range(int(self.Zombies[zombie].pos.y), int(self.Zombies[zombie].pos.y) + self.Zombies[zombie].size_y)):
				del self.Balls[ball_index]
				del self.Zombies[zombie]
				return True
		return False

	# при столкновении шара с границей стены, шар нужно удалить
	def kill_wall(self, ball_index):
		for wall in range(len(self.Walls)):
			if self.Balls[ball_index].pos.y in range(self.Walls[wall].pos.y, self.Walls[wall].pos.y + self.Walls[wall].size_y):
				del self.Balls[ball_index]
				return True
		return False

App()