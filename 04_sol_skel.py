"""
Solution to the one-way tunnel
"""
import time
import random
from multiprocessing import Lock, Condition, Process
from multiprocessing import Value

SOUTH = 1
NORTH = 0

NCARS = 10

class Monitor():
    def __init__(self):
        self.mutex = Lock()
        
        self.north_cars = Value('i', 0) #Numero de coches dentro del tunel (north)
        self.south_cars = Value('i', 0) #Numero de coches dentro del tunel (south)
        
        self.actual_direction = Value('i', 0) #Direccion en la que circulan o pueden circular los coches dentro del tunel

        self.open_north = Condition(self.mutex)         # open_* es el semaforo que deja pasar al tunel
        self.open_south = Condition(self.mutex)
        self.queue_north = Condition(self.mutex)        # queue_* es el semaforo que deja pasar a la cola del tunel
        self.queue_south = Condition(self.mutex)

    def wants_enter(self, direction):
        self.mutex.acquire()

        if direction == NORTH:
            self.queue_north.wait_for(lambda: self.actual_direction.value == SOUTH)     # Deja pasar a la cola para el grupo siguiente si vienen coches hacia esta direccion
            self.open_north.wait_for(lambda: self.south_cars.value == 0)                # Deja pasar cuando los de la otra direccion hayan salido
            self.actual_direction.value = NORTH
            self.north_cars.value += 1
        else:
            self.queue_south.wait_for(lambda: self.actual_direction.value == NORTH)
            self.open_south.wait_for(lambda: self.north_cars.value == 0)
            self.actual_direction.value = SOUTH
            self.south_cars.value += 1
    
        self.mutex.release()

    def leaves_tunnel(self, direction):
        self.mutex.acquire()
        if direction == NORTH:            		
            self.north_cars.value -= 1
            if self.north_cars.value == 0: # No hay coches, podemos cambiar la direccion
                print("Abre sur")
                self.open_south.notify_all()        # Primero abre el paso al tunel para los de la otra direccion
                self.open_north.notify_all()        # Abre en la misma direccion si no hay nadie en el otro sitio (previene bloqueos si en uno de los lados no viene nadie)
                self.queue_north.notify_all()
        else:
            self.south_cars.value -= 1
            if self.south_cars.value == 0:
                print("Abre norte")
                self.open_north.notify_all()
                self.open_south.notify_all()
                self.queue_south.notify_all()
                
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
