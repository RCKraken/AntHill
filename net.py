import random
import neuron
import copy

def convertToNet(x):
	if x < 0.5:
		return 1
	else:
		return (1 / x)


class Net:

	def __init__(self):
		#initialize all layers
		self.sensorLayer = [neuron.Neuron(0) for i in range(10)]
		self.hiddenLayer = [neuron.Neuron(len(self.sensorLayer)) for i in range(10)]
		self.actionLayer = [neuron.Neuron(len(self.hiddenLayer)) for i in range(6)]
	
	#run each frame for each ant
	def compute(self, inputs):
		#apply sensor values to neurons
		for i in range(len(inputs)):
			self.sensorLayer[i].currentVal = inputs[i]
		
		#compute hidden layer
		for n in self.hiddenLayer:
			n.process(self.sensorLayer)

		#compute action layer
		for n in self.actionLayer:
			n.process(self.hiddenLayer)

		#put values into an array
		tempArray = []
		for n in self.actionLayer:
			tempArray.append(n.currentVal)

		return tempArray

	def makeCopy(self):
		#run when making non-mutated offspring
		return copy.deepcopy(self)	

	def makeMutant(self, potatoIndex):
		new = self.makeCopy()
		for i in range(potatoIndex):
			if random.randint(0, 1) == 0:
				#hidden layer
				n = random.randint(0, len(new.hiddenLayer) - 1)
				new.hiddenLayer[n] = neuron.Neuron(len(new.sensorLayer))
			else:
				#action layer
				n = random.randint(0, len(new.actionLayer) - 1)
				new.actionLayer[n] = neuron.Neuron(len(new.hiddenLayer))

		return new

