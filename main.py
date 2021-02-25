import math
from functools import reduce

class Road:
  def __init__(self, name, start, end, L):
    self.name = name
    self.start = start
    self.end = end
    self.L = L

    self.carsDriving = []
    self.carsWaiting = []

    self.visits = 0
    self.priority = 0

  def __str__(self):
    return f'{self.name}'

  def set_name(self, name):
    self.name = name

  def get_name(self):
    return self.name

  def reduceWait(self):
    for car in self.carsDriving:
      car.reduceWait()
      if car.getWait() == 0:
        self.carsWaiting.append(car)
        self.carsDriving.remove(car)

    if self.end.greenExit == self:
      car = self.carsWaiting.pop()
      road = car.move(0)
      road.addDriving(car)
  
  def addDriving(self, car):
    self.carsDriving.append(car)
  
  def incrementVisits(self):
    self.visits += 1

  def getVisits(self):
    return self.visits

  def getPriority(self):
    return self.priority

  def setPriority(self, priority):
    self.priority = priority
  
    


class Intersection:
  def __init__(self, id):
    self.id = id
    self.exits = []
    self.entrances = []
    self.greenExit = None
    self.lightCycle = [] # In the format [[time in cycle, entrance0]...[time, entrance n-1]]?

  def addEntrance(self, road):
    self.entrances.append(road)

  def addExit(self, road):
    self.exits.append(road)

  def generateLightCycle(self, simTime):
    totalVisits = 0
    for exit in self.exits:
      totalVisits += exit.getVisits()

    for exit in self.exits:
      if exit.getVisits() == 0:
        priority = 0
      else:
        priority = math.ceil((totalVisits/exit.getVisits()))
        exit.priority = priority
      self.lightCycle.append([exit.get_name(), exit.priority])
      
    priorityList = []
    
    for exit in self.exits:
      priorityList.append(exit.visits)
      
    def find_gcd(list):
      return reduce(math.gcd, list)

    gcdInt = find_gcd(priorityList)
    
    if(gcdInt != 0):
      priorityList = [x / gcdInt for x in priorityList]

    for exitn in range(len(self.exits)):
      if(gcdInt != 0):
        self.exits[exitn].setPriority(priorityList[exitn])
  
  def getLightCycle(self):
    self.lightCycle = []
    for exit in self.exits:
      self.lightCycle.append([exit.get_name(), exit.priority])
    return self.lightCycle
  
  #def setLightCycle(self, exit, priority):
    

  def getEntrances(self):
    print(self.entrances)
    
    

  
class Car:
  def __init__(self, numRoads, roadList):
    self.numRoads = numRoads
    self.roadList = roadList
    self.visitedRoads = []
    self.timeToWait = 0
    
  
  
  def getWait(self):
    return self.timeToWait
    
  def move(self):
    if self.roadList:
      self.visitedRoads.append(self.roadList.pop(0))
      return self.roadList[0]
    else:
      self.finished = True
    
  def reduceWait(self):
    self.timeToWait -= 1


class Map:
  def __init__(self, file):
    self.data = file.readline().split()
    self.roads = {}
    self.intersections = []
    self.cars = []

    for i in range(0, int(self.data[1])):
      # Initialise each intersection with id n-1
      intersection = Intersection(i)
      self.intersections.append(intersection)
    

    for lineNum in range(0, int(self.data[2])):  # Read streets from file
      streetData = file.readline().split()
      start = self.getIntersection(streetData[0])
      end = self.getIntersection(streetData[1])
      self.roads[streetData[2]] = Road(streetData[2], start, end, streetData[3])
      start.addEntrance(self.roads[streetData[2]])
      end.addExit(self.roads[streetData[2]])

      
    for lineNum in range(0, int(self.data[3])):  # Read cars from file
      carData = file.readline().split()
      roads = []
      for i in range(1, int(carData[0])):
        roads.append(self.roads[carData[i]])
      car = Car(carData[0], roads)
      roads[i-1].addDriving(car)
      self.cars.append(car)
  
  def getIntersection(self, id):
    return self.intersections[int(id)]
  
  def reduceWait(self):
    for road in self.roads:
      self.roads[road].reduceWait()

  def simulate(self):
    points = 0
    total = 0

    for i in range(0, int(self.data[0])):
      self.reduceWait()
    
    for car in self.cars:
      if car.finished:
        points += int(self.data[4])
      
      total += int(self.data[4])
    
    print(f"{points}/{total} points")

  def getPriority(self):
    for car in self.cars:
      for road in car.roadList:
        road.incrementVisits()

  def getLightCycles(self):
    print(len(self.intersections))
    for intersection in self.intersections:
      intersection.generateLightCycle(self.data[0])
      lightcycle = intersection.getLightCycle()
      #print(intersection.priorityList)
      print(intersection.id)
      cycletime = 0
      for light in lightcycle:
        if light[1] != 0:
          cycletime += light[1]
      print(int(cycletime))
      for light in lightcycle:
        print(f'{light[0]} {int(light[1])}')

      



f = open("b.txt", "r")
myMap = Map(f)
myMap.getPriority()
myMap.getLightCycles()

def create_output():
  print()