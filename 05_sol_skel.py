"""
Solution to the one-way tunnel
"""
import time
import random
from multiprocessing import Lock, Condition, Manager, Process
from multiprocessing import Value

SOUTH = "north"
NORTH = "south"

NCARS = 10
K2 = 5
K1 = 5

class Monitor():
    def __init__(self):
        self.mutex = Lock()
        self.manager = Manager()
        self.north_cars = Value('i', 0)
        self.south_cars = Value('i', 0)
        
        self.north_cars_waiting = Value('i', 0)
        self.south_cars_waiting = Value('i', 0)
        
        self.open_north = Condition(self.mutex)
        self.open_south = Condition(self.mutex)
        
        self.too_many_north_cars = Condition(self.mutex)
        self.too_many_south_cars = Condition(self.mutex)

    def wants_enter(self, direction):
        self.mutex.acquire()

        if direction == 'north':
            self.too_many_south_cars.wait_for(lambda: self.south_cars_waiting.value <= K2)
            self.north_cars_waiting.value += 1
            
            self.open_north.wait_for(lambda: self.south_cars.value == 0)
            self.north_cars.value += 1
            self.north_cars_waiting.value -= 1
            
            self.too_many_north_cars.notify_all()
        else:
            self.too_many_north_cars.wait_for(lambda: self.north_cars_waiting.value <= K1)
            self.south_cars_waiting.value += 1
            
            self.open_south.wait_for(lambda: self.north_cars.value == 0)
            self.south_cars.value += 1
            self.south_cars_waiting.value -= 1
            
            self.too_many_south_cars.notify_all()
        self.mutex.release()

    def leaves_tunnel(self, direction):
        self.mutex.acquire()

        if direction == 'north':
            self.north_cars.value -= 1
            self.open_south.notify_all()
        else:
            self.south_cars.value -= 1
            self.open_north.notify_all()
        
        self.mutex.release()

def delay(n=3):
    time.sleep(random.random()*n)

def car(cid, direction, monitor):
    print(f"car {cid} direction {direction} created")
    delay(1)
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
        #irection = NORTH
        cid += 1
        p = Process(target=car, args=(cid, direction, monitor))
        p.start()
        time.sleep(random.expovariate(1/0.5)) # a new car enters each 0.5s


if __name__ == "__main__":
    main()
