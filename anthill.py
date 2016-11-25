import time
import random
import numpy as np
import sfml as sf
import food
import ant
import dir
import net

def mapgen():

	for i in range(0, arraysize):

		for j in range(0,arraysize):
	
			if j < arraysize / 2:
			
				array[i][j] = 1

			elif j == arraysize / 2:

				array[i][j] = 2

def startup():

	mapgen()		

	for i in range(9):

		antList.append(ant.Ant((random.randint(0, 49), 23), 0))

		for j in range(2):
			
			foodList.append(food.Food(random.randint(0,49), array))		

def restart():

	print("restarted")

	mapgen()

	#new units

	for i in range(2):

		antList.append(ant.Ant((random.randint(0, 49), 23), 0))

	#mutated units

	for i in range(5):

		am = ant.Ant((random.randint(0, 49), 23), 0)

		am.neuralNet = winner.neuralNet.makeMutant(1)
	
		antList.append(am)

	#original unit

	for i in range(2):

		ao = ant.Ant((random.randint(0, 49), 23), 0)
		
		ao.neuralNet = winner.neuralNet.makeCopy()

		antList.append(ao)

	foodList.clear()

	for i in range(18):

		foodList.append(food.Food(random.randint(0,49), array))

def simulate():

	deadList = []

	global globalTime

	global winner

	global extinct

	global show

	globalTime += 1

	if globalTime == 30:

		globalTime = 0

		foodList.append(food.Food(random.randint(0,49), array))
	
	for a in range(len(antList)):
		
		if antList[a].simulate(array, antList, foodList) == False:

			deadList.append(antList[a])

	for d in deadList:

		if winner == None or d.age > winner.age:
 
			winner = d

			print(d.age)

			show = input("Display? ")

		antList.remove(d)

	deadlist = []

	#check for extinction

	if len(antList) == 0:

		extinct = True

def render():

	window.clear()
	
	for i in range(0, arraysize):

		for j in range(0, arraysize):

			if array[i][j] == 0 and j > 25:

				shape.fill_color = sf.Color(50, 50, 225)

			if array[i][j] == 5:

				shape.fill_color = sf.Color(50, 50, 225)
				
			if array[i][j] == 1:

				shape.fill_color = sf.Color(130, 72, 42)
			
			if array[i][j] == 2:

				shape.fill_color = sf.Color(0, 200, 0)

			if array[i][j] == 0 and j < 25:

				shape.fill_color = sf.Color(65, 36, 21)			

			if array[i][j] == 0 and j == 25:

				shape.fill_color = sf.Color(0, 75, 0)			

			shape.position = (i * 10,j * 10)

			window.draw(shape)	
	
	for f in foodList:

		window.draw(f.foodShape)	

	for a in antList:

		window.draw(a.antShape)
	
	window.display()

#START OF PROGRAM

globalTime = 0

winner = None

extinct = False

array = np.zeros((50,50))

foodList = []

antList = []

window = sf.RenderWindow(sf.VideoMode(500, 500), "anthill")

window.view = sf.View(sf.Rectangle((0, 0), (500, -500)))

window.view.center = (250, 250)

running = True

arraysize = int(array.size ** 0.5)

shape = sf.RectangleShape((10, 10))

startup()

show = input("Display? ")

while running:

	simulate()

	if show == "yes":

		render()

	if extinct == True:
		extinct = False
		restart()
	
		#time.sleep(0.1)
