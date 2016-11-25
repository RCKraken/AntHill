import math
import random

#calculate sigmoid function for x
def sigmoid(x):
	return 1 / ( 1 + math.pow(math.e, -5 * (x - 2.65)))


class Neuron:
	
	def __init__(self, pN):
		self.weights = []

		for i in range(pN):
			self.weights.append(random.random())
		self.currentVal = 0
	
	def process(self, lastLayer):
		if len(lastLayer) != len(self.weights):
			print("Layer order mismatch")
			exit(-1)
		
		#sum all previous neuron values with weights
		sum = 0
		for i in range(0, len(self.weights)):
			sum += (self.weights[i] * lastLayer[i].currentVal)

		self.currentVal = sigmoid(sum)
