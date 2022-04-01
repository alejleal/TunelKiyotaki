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

        self.north_waiting = Value('i', 0)
        self.south_waiting = Value('i', 0)
        
        self.direction = Value('i', NONE) # Direccion en la que circulan o pueden circular los coches dentro del tunel

        self.north_entry = Condition(self.mutex)         # open_* es el semaforo que deja pasar al tunel
        self.south_entry = Condition(self.mutex)
        self.north_queue = Condition(self.mutex)        # queue_* es el semaforo que deja pasar a la cola del tunel
        self.south_queue = Condition(self.mutex)

    def wants_enter(self, direction):
        self.mutex.acquire()

        if direction == SOUTH:
            # Deja pasar a la cola para el grupo siguiente si vienen coches hacia esta direccion o si no hay direccion establecida
            self.north_queue.wait_for(lambda: self.direction.value == NORTH or self.direction.value == NONE)
            self.north_waiting.value += 1

            # Deja pasar cuando los de la otra direccion hayan salido o no haya esperando en el otro sentido
            self.north_entry.wait_for(lambda: self.south_cars.value == 0 or self.south_waiting.value == 0)           

            self.direction.value = SOUTH
            self.south_queue.notify_all()       # Es necesario notificar el cambio de direccion para llenar la otra cola

            self.north_cars.value += 1
            self.north_waiting.value -= 1

        else:
            self.south_queue.wait_for(lambda: self.direction.value == SOUTH or self.direction.value == NONE)
            self.south_waiting.value += 1

            self.south_entry.wait_for(lambda: self.north_cars.value == 0 or self.north_waiting.value == 0)

            self.direction.value = NORTH
            self.north_queue.notify_all()

            self.south_cars.value += 1
            self.south_waiting.value -= 1
    
        self.mutex.release()

    def leaves_tunnel(self, direction):
        self.mutex.acquire()
        if direction == SOUTH:            		
            self.north_cars.value -= 1
            if self.north_cars.value == 0:           # No hay coches, podemos cambiar la direccion
                self.direction.value = NONE          # Se restablece la direccion por si vuelven a pasar en el mismo sentido

                print("Abre sur - ", self.south_waiting.value)
                self.south_entry.notify_all()        # Primero abre el paso al tunel para los de la otra direccion

                self.north_queue.notify_all()
                self.north_entry.notify_all()        # Abre en la misma direccion si no hay nadie en el otro sitio (previene bloqueos si en uno de los lados no viene nadie)
        else:
            self.south_cars.value -= 1
            if self.south_cars.value == 0:
                self.direction.value = NONE

                print("Abre norte - ", self.north_waiting.value)
                self.north_entry.notify_all()

                self.south_queue.notify_all()
                self.south_entry.notify_all()
                    
                
        self.mutex.release()

def pdir(dir):
    return 'N' if dir else 'S'

def delay(n=3):
    time.sleep(random.random()*n)

def car(cid, direction, monitor):
    print(f"car {cid} direction {pdir(direction)} created")
    delay(6)
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
