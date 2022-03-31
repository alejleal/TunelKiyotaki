from multiprocessing import Process, Lock, Condition, Value
import random, time

NCARS = 10
NORTH = 0
SOUTH = 1

class Monitor():
	def __init__(self):
		self.mutex = Lock()
		self.actual_direction = Value('i',0)
		self.north_semaphore = Condition(self.mutex)
		self.south_semaphore = Condition(self.mutex)
		self.waiting_north = Value('i',0)
		self.waiting_south = Value('i',0)
		self.traffic_north = Value('i',0)
		self.traffic_south = Value('i',0)
		
	def wants_enter(self, direction):
		self.mutex.acquire()
		
		if direction == NORTH:
			self.waiting_north.value += 1
			self.north_semaphore.wait_for(lambda: self.actual_direction.value == NORTH or self.traffic_south == 0)
			self.actual_direction.value = NORTH
			self.waiting_north.value -= 1
			self.traffic_north.value += 1
			
		else:
			self.waiting_south.value += 1
			self.south_semaphore.wait_for(lambda: self.actual_direction.value == SOUTH or self.traffic_north == 0)
			self.actual_direction.value = SOUTH
			self.waiting_south.value -= 1
			self.traffic_south.value += 1
			
		if self.actual_direction == NORTH:
			self.south_semaphore.notify()
			self.north_semaphore.notify()
		
		else:
			self.north_semaphore.notify()
			self.south_semaphore.notify()
		
		self.mutex.release()
				
	def leaves_tunnel(self, direction):
		self.mutex.acquire()
		
		if direction == NORTH:
			self.traffic_north.value -= 1
		else:
			self.traffic_south.value -= 1
			
		if (self.traffic_north.value + self.traffic_south.value == 0):
			if direction == NORTH:
				if self.waiting_south.value > 0: #self.waiting_north.value:
					self.actual_direction.value = SOUTH
				else:
					self.actual_direction.value = NORTH
					
			else:
				if self.waiting_north.value > 0: #self.waiting_south.value:
					self.actual_direction = NORTH
				else:
					self.actual_direction = SOUTH
		if self.actual_direction == NORTH:
			self.south_semaphore.notify()
			self.north_semaphore.notify()
		
		else:
			self.north_semaphore.notify()
			self.south_semaphore.notify()
		
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
		direction = NORTH if random.randint(0,1)==1	else SOUTH
		cid += 1
		p = Process(target=car, args=(cid, direction, monitor))
		p.start()
		time.sleep(random.expovariate(1/0.5)) # a new car enters each 0.5s


if __name__ == "__main__":
	main()
