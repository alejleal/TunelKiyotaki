"""
Solution to the one-way tunnel
"""
import time
import random
from multiprocessing import Lock, Condition, Manager, Process
from multiprocessing import Value

SOUTH = 1
NORTH = 0

NCARS = 10

class Monitor():
  def __init__(self):
  	self.mutex = Lock()
  	self.manager = Manager()
  	self.actual_direction = Value('i',0) # direccion
  	self.waiting_north = Value('i',0) # coches esperando a entrar 
  	self.waiting_south = Value('i',0)
  	self.cars_north = Value('i',0) # coches dentro
  	self.cars_south = Value('i',0)
  	self.open_north = Condition(self.mutex) # condiciones
  	self.open_south = Condition(self.mutex)
  	
  def wants_enter(self, direction):
  	self.mutex.acquire()
  	if direction == NORTH:
  		self.waiting_north.value += 1
  		self.open_north.wait_for(lambda: self.cars_south.value == 0 and self.waiting_north.value >= self.waiting_south.value)
  		self.actual_direction = NORTH
  		self.waiting_north.value -= 1
  		self.cars_north.value += 1
  	else:
  		self.waiting_south.value += 1
  		self.open_south.wait_for(lambda: self.cars_north.value == 0 and self.waiting_north.value < self.waiting_south.value)
  		self.actual_direction = SOUTH
  		self.waiting_south.value -= 1
  		self.cars_south.value += 1
  	self.mutex.release()
  
  def leaves_tunnel(self, direction):
  	self.mutex.acquire()
  	if direction == NORTH:
  		self.cars_north.value -=1
  		if self.cars_north.value == 0:
  			
  			for _ in range(self.waiting_south.value):
  				self.open_south.notify()
  			
  	else:
  		self.cars_south.value -=1
  		if self.cars_south.value == 0:
  			
  			for _ in range(self.waiting_north.value):
  				self.open_north.notify()
  			
  	self.mutex.release()


def delay(n=3):
	time.sleep(random.random()*n)

def car(cid, direction, monitor):
	print(f"car {cid} direction {direction} created")
	delay(6)
	print(f"car {cid} heading {direction} wants to enter")
	monitor.wants_enter(direction)
	print(f"car {cid} heading {direction} enters the tunnel")
	delay(3)
	print(f"car {cid} heading {direction} leaving the tunnel")
	monitor.leaves_tunnel(direction)
	print(f"car {cid} heading {direction} out of the tunnel")

def main():
	monitor = Monitor()
	cid = 0
	for _ in range(NCARS):
		direction = NORTH if random.randint(0,1)==1  else SOUTH
		cid += 1
		p = Process(target=car, args=(cid, direction, monitor))
		p.start()
		time.sleep(random.expovariate(1/0.5)) # a new car enters each 0.5s


if __name__ == "__main__":
	main()
