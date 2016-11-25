
import dir
import sfml as sf
import net
import numpy as np
class Ant:

	def __init__(self, position, identity):
		self.hunger = 0
		self.proxAnt = 0
		self.memory = 0
		self.proxFood = [0, 0, 0, 0]
		self.proxWall = [0, 0, 0, 0]
		self.dirOut = 0
		self.direction = 0

		self.pos = position
		self.id = id
		#tells if previous action caused this ant to be inactive this time
		self.holding = 0
		self.age = 0
		self.offspring = []
		self.genScore = np.size(self.offspring)
		self.lifeSpan = 4

		#neural net
		self.neuralNet = net.Net()

		#rendering
		self.antShape = sf.RectangleShape((10, 10))
		
		self.antShape.position = (self.pos[0] * 10, self.pos[1] * 10)  

	def color(self):

		if self.age > self.lifeSpan / 2:
			self.antShape.fill_color = sf.Color.BLACK

		elif self.age > self.lifeSpan / 4:
			self.antShape.fill_color = sf.Color(50, 50, 50)

		else:
			self.antShape.fill_color = sf.Color(100, 100, 100)

	def simulate(self, map, ants, food):
		self.hunger += 0.01
		self.age += 0.01
	
		if self.hunger >= self.lifeSpan:
			return False

		#find prox to ants
		nearest = 10000000
		for a in ants:
			if a != self:
				dist = dir.getDist(self.pos, a.pos)
				if dist < nearest:
					nearest = dist

		self.proxAnt = net.convertToNet(nearest)

		#find prox to food
		for i in range(4):
			dist = 0
			while True:

				for j in range(20, 30):

					if i == 0 or i == 2:

						if map[(j, dir.getPosDir(self.pos, i, dist)[1])] == 5:
							break

					if i == 1 or i == 3:

						if map[(dir.getPosDir(self.pos, i, dist)[1], j)] == 5:
							break
				
				if dir.getPosDir(self.pos, i, dist)[1] == 49:
					break
				if dir.getPosDir(self.pos, i, dist)[0] == 0:
					break
				if dir.getPosDir(self.pos, i, dist)[0] == 49:
					break
				if dir.getPosDir(self.pos, i, dist)[1] == 0:
					break
				
				dist += 1
			
			self.proxFood[i] = net.convertToNet(dist)

		#find distances to walls
		for i in range(4):
			dist = 0
			while True:
			
				if dir.getPosDir(self.pos, i, dist)[1] == 49:
					break
				if dir.getPosDir(self.pos, i, dist)[0] == 0:
					break
				if dir.getPosDir(self.pos, i, dist)[0] == 49:
					break
				if dir.getPosDir(self.pos, i, dist)[1] == 0:
					break
				if map[(dir.getPosDir(self.pos, i, dist))] != 0:
					break
				dist += 1

			self.proxWall[i] = net.convertToNet(dist)

		#process with neural net
		output = self.neuralNet.compute([self.memory, self.hunger, self.proxFood[0],  self.proxFood[1], self.proxFood[2], self.proxFood[3], self.proxWall[0], self.proxWall[1], self.proxWall[2], self.proxWall[3]])

		if output[0] > self.dirOut:
			self.dirOut = output[0]
			self.direction = 0
		if output[1] > self.dirOut:
			self.dirOut = output[1]
			self.direction = 1
		if output[2] > self.dirOut:
			self.dirOut = output[2]
			self.direction = 2
		if output[3] > self.dirOut:
			self.dirOut = output[3]
			self.direction = 3
		if output[0] > self.dirOut:
			self.dirOut = output[4]
			self.direction = 4
		self.memory = output[5]

		#move accordingly

		if self.holding > 0:

			self.holding -= 1

		else:
			if self.direction != 0:
				self.move(map,self. direction)
				self.eat(food, map)
				self.proCreate(ants)
		self.color()

	def move(self, map, move):
		newPos = dir.getPosAdjacent(self.pos, move - 1)

		#check for moving into air
		if newPos[1] > 26:
			return False

		if newPos[1] < 0:
			return False

		if newPos[0] < 0 or newPos[0] > 49:
			return False
	
		#check if digging or not
		if map[newPos[0]][newPos[1]] != 0:
			self.holding = 5
			map[newPos[0]][newPos[1]] = 0
			self.hunger += 0.05

		self.pos = newPos

		self.antShape.position = (self.pos[0] * 10, self.pos[1] * 10)  			

	def eat(self, food, map):

		if self.hunger < self.lifeSpan / 4:

			return False	

		removed = -1

		for i in range(len(food)):

			if self.pos == food[i].pos:

				removed = i

		if removed != -1:
			
			self.hunger -= 0.5

			if self.hunger < 0:

				self.hunger = 0

			food.remove(food[removed])
			map[(self.pos)] = 0
			
	
	def proCreate(self, a):

		for i in a:

			if self.pos == i.pos and self.age > self.lifeSpan / 2 and i.age > self.lifeSpan / 2 and i != self and len(a) < 50:

				self.hunger += self.lifeSpan / 8

				i.hunger += self.lifeSpan / 8
				
				p = Ant(self.pos, 0)
				
				p.neuralNetwork = self.neuralNet.makeMutant(1)

				a.append(p)	

				self.offspring.append(p)

				i.offspring.append(p)
