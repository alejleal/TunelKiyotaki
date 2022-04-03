"""
Solution to the one-way tunnel
"""
import time
import random
from multiprocessing import Lock, Condition, Process
from multiprocessing import Value

SOUTH = 1
NORTH = 0
NONE = -1

NCARS = 10

class Monitor():
    def __init__(self):
        self.mutex = Lock()
        
        self.north_cars = Value('i', 0) #Numero de coches dentro del tunel (north)
        self.south_cars = Value('i', 0) #Numero de coches dentro del tunel (south)

        self.north_waiting = Value('i', 0) #Numero de coches esperando (north)
        self.south_waiting = Value('i', 0) #Numero de coches esperando (south)
        
        self.direction = Value('i', NONE) # Direccion en la que circulan o pueden circular los coches dentro del tunel
        self.north_entry = Condition(self.mutex)         # open_* es el semaforo que deja pasar al tunel
        self.south_entry = Condition(self.mutex)
        self.north_queue = Condition(self.mutex)        # queue_* es el semaforo que deja pasar a la cola del tunel
        self.south_queue = Condition(self.mutex)

    def wants_enter(self, direction):
        self.mutex.acquire()

        if direction == SOUTH:
            self.north_queue.wait_for(lambda: self.direction.value == NORTH or self.direction.value == NONE)
            
            self.north_waiting.value += 1
            
            self.north_entry.wait_for(lambda: self.south_cars.value == 0 and (self.direction.value == SOUTH or self.direction.value == NONE))
            
            self.north_cars.value += 1
            self.direction.value = SOUTH
            self.south_queue.notify_all()
            
            self.north_waiting.value -= 1
        else:
            self.south_queue.wait_for(lambda: self.direction.value == SOUTH or self.direction.value == NONE)
            
            self.south_waiting.value += 1
            
            self.south_entry.wait_for(lambda: self.north_cars.value == 0 and (self.direction.value == NORTH or self.direction.value == NONE))
            
            self.south_cars.value += 1
            self.direction.value = NORTH
            self.north_queue.notify_all()
            
            self.south_waiting.value -= 1
        self.mutex.release()

    def leaves_tunnel(self, direction):
        self.mutex.acquire()
        if direction == SOUTH:
            self.north_cars.value -= 1
            if self.north_cars.value == 0: # No hay coches
                if self.north_waiting.value == 0: #No hay más coches esperando, se cambia la direccion 
                    self.direction.value = NORTH
                    self.north_queue.notify_all()
                    print("Abre sur - ", self.south_waiting.value)
                self.south_entry.notify_all()
                if self.south_waiting.value == 0: #No hay coches en la otra direccion esperando
                    self.direction.value = NONE 
                    self.north_entry.notify_all() #Se devuelve el turno a la direccion actual(primero)
                    self.south_queue.notify_all() #Y despues a la cola de la otra direccion(segundo)
        else:
            self.south_cars.value -= 1
            if self.south_cars.value == 0:
                if self.south_waiting.value == 0:
                    self.direction.value = SOUTH
                    self.south_queue.notify_all()
                    print("Abre norte - ", self.north_waiting.value)
                self.north_entry.notify_all()
                if self.north_waiting.value == 0:
                    self.direction.value = NONE
                    self.south_entry.notify_all()
                    self.north_queue.notify_all()
        self.mutex.release()

def pdir(dir):
    return 'S' if dir else 'N'

def delay(n=3):
    time.sleep(random.random()*n)

def car(cid, direction, monitor):
    print(f"car {cid} direction {pdir(direction)} created")
    delay(1)
    print(f"car {cid} heading {pdir(direction)} wants to enter")
    monitor.wants_enter(direction)
    print(f"car {cid} heading {pdir(direction)} enters the tunnel")
    delay(3)
    print(f"car {cid} heading {pdir(direction)} leaving the tunnel")
    monitor.leaves_tunnel(direction)
    print(f"car {cid} heading {pdir(direction)} out of the tunnel")

def main():
    monitor = Monitor()	
    cid = 0
    for _ in range(NCARS):
        direction = NORTH if random.randint(0,1) == 1 else SOUTH
        cid += 1
        p = Process(target=car, args=(cid, direction, monitor))
        p.start()
        time.sleep(random.expovariate(1/0.5)) # a new car enters each 0.5s


if __name__ == "__main__":
    main()
