import pyxel, random

from plants_game.draw import *
 
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
		self.Zombie_balls = []	
		self.Patrons_display = []
		self.Walls = [		# список со стенками на арене
			Wall(20, 15),
			Wall(20, 39),
			Wall(20, 63),
			Wall(20, 87)
		]
		self.Zombies = []	# список с зомбаками
		self.Score = 0		# очки игрока
		self.Weapon = Shotgun(img_id=self.IMG_ID0) 	# рисуем обрез снизу экрана
		self.Game_status = True		# если игра не закочена

		#  запускаем отрисовку игрульки
		pyxel.run(self.update, self.draw)

	# функция отвечает за определение координат всего, что есть и движется на экране
	def update(self):
		if pyxel.btnp(pyxel.KEY_Q):			# если кнопка Q нажата, то выходим из игры
			pyxel.quit()

		if not self.Game_status:
			if pyxel.btnp(pyxel.KEY_SPACE):			# если кнопка Q нажата, то выходим из игры
				self.new_game()
				self.Score = 0
				self.Game_status = True	

		if self.Game_status:
			self.Weapon
			self.plant.get_image = self.plant.get_image_right
			# изменение позиций игрока при нажатии кнопок W или S, т.е ходим вверх или вниз
			if self.plant.pos.y-4 > 0 and pyxel.btn(pyxel.KEY_W):
				self.plant.update(self.plant.pos.x, self.plant.pos.y-3)
				self.plant.get_image = self.plant.get_image_run
			if self.plant.pos.y+16 < self.WINDOW_H and pyxel.btn(pyxel.KEY_S):
				self.plant.update(self.plant.pos.x, self.plant.pos.y+3)
				self.plant.get_image = self.plant.get_image_run

			ball_count = len(self.Balls)		# кол-во шаров на экране
			zombie_count = len(self.Zombies)	# кол-во зомби на экране
			patron_count = len(self.Patrons_display)
			zombie_balls_count = len(self.Zombie_balls)

			# создаем противника Зомби. Должно быть на экране не больше трех штук в один момент времени
			if zombie_count < 6:
				#### рандомно генерируем зомби на карте ####
				new_zombie = Zombie(self.IMG_ID0) # создание нового объекта Зомби
				# устанавливаем позицию нового объекта зомби
				new_zombie.update(
					health_x = new_zombie.health_index_pos_x,
					x=self.WINDOW_W+random.choice(range(0, 10)),
					y=random.choice(self.Walls).pos.y-random.choice(range(8, 13)),
					health=new_zombie.current_health
				)
				# добавляем новый объект зомби в список всех зомбаков
				self.Zombies.append(new_zombie)

			if patron_count < 3:
				new_patron = Patron(self.IMG_ID0) # новый экземпляр класса патрона
				new_patron.update(x=(new_patron.pos.x*(patron_count+1)/2), y=new_patron.pos.y)
				self.Patrons_display.append(new_patron)

			# заставляем ходить зомби по экрану
			for zombie in range(zombie_count):
				if self.Zombies[zombie].archer:
					zombie_push = random.choice(range(0, 50))
					if zombie_push in range(1, 5):
						push_end_choise = random.choice(range(0, 100))
						if push_end_choise in range(90, 100):
							zombie_ball = Ball()
							zombie_ball.update(
								self.Zombies[zombie].pos.x + round(self.Zombies[zombie].size_x/2) - 6,
								self.Zombies[zombie].pos.y + self.Zombies[zombie].size_y/2,
								2,
								8
							)
							self.Zombie_balls.append(zombie_ball)

				self.Zombies[zombie].update(
					health_x = self.Zombies[zombie].health_index_pos_x,
					x=self.Zombies[zombie].pos.x + self.Zombies[zombie].speed,
					y=self.Zombies[zombie].pos.y,
					health=self.Zombies[zombie].current_health
				)
			# при нажатии кнопки D вылетает шар, всего на экране не должно быть больше 3 шаров
			if pyxel.btnp(pyxel.KEY_D) and ball_count < 3:
				self.plant.get_image = self.plant.get_image_run
				new_ball = Ball()	# создаем новый экзмепляр класса шара
				# определяем начальную позицию шара
				new_ball.update(
					self.plant.pos.x + round(self.plant.size_x/2) + 6,
					self.plant.pos.y + self.plant.size_y/2,
					new_ball.size,
					new_ball.color
				)
				# добавляем шар в список шаров
				self.Balls.append(new_ball)

			self.kill_heart()

			# проверяем положение шара на экране. Шар должен исчезнуть при столкновении с объектом
			for i in range(ball_count):
				# при выстреле нужно убрать патрон снизу экрана
				self.Patrons_display = self.Patrons_display[:3-ball_count]
				# если позиция шара не в начале и конце экрана, то пусть летит
				if self.Balls[i].pos.x > 0 and self.Balls[i].pos.x < self.WINDOW_W:
					# заставляем шар лететь по экрану
					self.Balls[i].update(
						self.Balls[i].pos.x + self.Balls[i].speed,
						self.Balls[i].pos.y,
						self.Balls[i].size,
						self.Balls[i].color
					)
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

			for i in range(zombie_balls_count):
				# проверяем, чтобы шар от зомби находился в рамках игрового поля
				if self.Zombie_balls[i].pos.x < self.WINDOW_W and self.Zombie_balls[i].pos.x > 0:
					# если все ОК, то рисуем движение шара от зомби
					self.Zombie_balls[i].update(
						self.Zombie_balls[i].pos.x - self.Zombie_balls[i].speed,
						self.Zombie_balls[i].pos.y,
						self.Zombie_balls[i].size,
						self.Zombie_balls[i].color
					)
					try:
						if self.kill_gamer(i):
							break
					except:
						pass
				else:
					del self.Zombie_balls[i]
					break

	# отрисовка всех объектов на экране
	def draw(self):
		if not self.Game_status:
			pyxel.cls(0)
			pyxel.text(self.WINDOW_W/2-18, self.WINDOW_H/2-5, "Game Over", 8)
			return

		pyxel.cls(0) # очищаем экран, выставляем ему черный цвет (цвет можно поменять)
		pyxel.blt(0, 0, 1, 0, 0, 160, 120, 0)	# отрисовываем бэкграунд (само поле)
		# отрисовка игрока
		pyxel.blt(self.plant.pos.x, self.plant.pos.y, self.plant.img_plant, self.plant.get_image.pos.x, self.plant.get_image.pos.y, self.plant.size_x, self.plant.size_y, self.plant.color_tr)
		
		# вывод набранных очков
		pyxel.text(35, 114, "Score: {score}".format(score=self.Score), 0)

		# рисуем пушку снизу экрана
		pyxel.blt(self.Weapon.pos.x, self.Weapon.pos.y, self.Weapon.img_shotgun, self.Weapon.get_image.pos.x, self.Weapon.get_image.pos.y, self.Weapon.size_x, self.Weapon.size_y, self.Weapon.color_tr)

		# выстрел зомби (пульки от зомби)
		for zombie_push in self.Zombie_balls:
			pyxel.circ(zombie_push.pos.x, zombie_push.pos.y, zombie_push.size, zombie_push.color)

		for patron in self.Patrons_display:
			pyxel.blt(patron.pos.x, patron.pos.y, patron.img_patron, patron.get_image.pos.x, patron.get_image.pos.y, patron.size_x, patron.size_y, patron.color_tr)
		# отрисовка всех зомби
		for zombie in self.Zombies:
			pyxel.line(zombie.health.pos.x, zombie.health.pos.y, zombie.health.to_pos.x, zombie.health.to_pos.y, zombie.health.color)
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
				if self.Zombies[zombie].current_health != 0:
					self.Zombies[zombie].update(
						health_x = self.Zombies[zombie].health_index_pos_x,
						x=self.Zombies[zombie].pos.x,
						y=self.Zombies[zombie].pos.y,
						health=self.Zombies[zombie].current_health - 1)
					return True
				self.Score += self.Zombies[zombie].points
				del self.Zombies[zombie]
				return True
		return False

	# если пуля от зомби попала в игрока
	def kill_gamer(self, ball_index):
		# print("ballx: {ballx}, bally: {bally}, plantx: {plantx}, planty: {planty}, plantx_size: {plantx_size}, planty_size: {planty_size}".format(
		# 	ballx = int(self.Zombie_balls[ball_index].pos.x),
		# 	bally = int(self.Zombie_balls[ball_index].pos.y),
		# 	plantx = self.plant.pos.x,
		# 	planty = self.plant.pos.y,
		# 	plantx_size = self.plant.pos.x + self.plant.size_x,
		# 	planty_size = self.plant.pos.y + self.plant.size_y
		# ))
		if (int(self.Zombie_balls[ball_index].pos.x) in range(int(self.plant.pos.x), int(self.plant.pos.x) + self.plant.size_x)
		and int(self.Zombie_balls[ball_index].pos.y) in range(int(self.plant.pos.y), int(self.plant.pos.y) + self.plant.size_y)):
			del self.Zombie_balls[ball_index]
			self.Game_status = False
			return True
		return False

	# если зомби дошел до линии, по которой ходит игрок
	def kill_heart(self):
		for zombie in range(len(self.Zombies)):
			if int(self.Zombies[zombie].pos.x) < (int(self.plant.pos.x) + self.plant.size_x):
				self.Game_status = False
				return

	# при столкновении шара с границей стены, шар нужно удалить
	def kill_wall(self, ball_index):
		for wall in range(len(self.Walls)):
			if self.Balls[ball_index].pos.y in range(self.Walls[wall].pos.y, self.Walls[wall].pos.y + self.Walls[wall].size_y):
				del self.Balls[ball_index]
				return True
		return False

	# конец игры - очищаем все списки, которые рисуются на экране (шары, противники)
	def new_game(self):
		self.Balls.clear()
		self.Zombie_balls.clear()
		self.Zombies.clear()
		self.Patrons_display.clear()

App()