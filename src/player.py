import pygame
from simpleobjects import Food
from vectors import Vector2, UP, DOWN, LEFT, RIGHT, STOP
from math import sin, cos, pi
from gameobjects import AnimatedGameEntity, GameEntity
from actions import MoveAction

class Car(AnimatedGameEntity):
    def __init__(self, start_coordinates):
        self.image = pygame.image.load('../images/auto.PNG').convert_alpha()
        self.soundChannel = pygame.mixer.Channel(1)
        self.screechSound = pygame.mixer.Sound('../sounds/screech.ogg')
        self.motorStartSound = pygame.mixer.Sound('../sounds/motorstart.ogg')
        self.drivingSound = pygame.mixer.Sound('../sounds/driving.ogg')
        
        self.speed = 0.0
        self.max_speed = 20.0
        
        self.rotation_direction = 0.0
        self.rotation_speed = 10.0
        self.rotation = 0.0
        self.rotationToDo = 0.0
        
        self.location = start_coordinates
        self.name = 'car'
        self.isDriving = False
        self.actionQueue = []    
        
    def move(self, direction):
        self.actionQueue.append(MoveAction(direction))
                
    def accelerate(self):
        self.speed = min(self.speed + 0.8, self.max_speed)
        
    def brake(self):
        self.speed = max(self.speed - 1.6, -1.0)
    
    def start(self):
        self.soundChannel.play(self.motorStartSound)
         
    def brakeHard(self):
        if self.speed > 4.0:
            self.soundChannel.play(self.screechSound)
        self.speed = 0.0
        
    def steer(self, direction):
        if self.rotationToDo != 0.0:
            return
        
        if direction == LEFT:
            self.rotationToDo = 45.0
        if direction == RIGHT:
            self.rotationToDo = -45.0
            
    def render(self, surface, worldCoords):
        rotated_sprite = pygame.transform.rotate(self.image, self.rotation)
        w, h = rotated_sprite.get_size()
        surface.blit(rotated_sprite, (self.location.x - w/2 - worldCoords[0], 
                                      self.location.y - h/2 - worldCoords[1]))
        
    def process(self, time_passed):
        if self.speed != 0.0:
            rotationDelta = self.rotationToDo * time_passed * self.rotation_speed
            if abs(self.rotationToDo - rotationDelta) < 5.0:
                rotationDelta = self.rotationToDo                
            self.rotationToDo -= rotationDelta
            self.rotation += rotationDelta
            
            heading_x = sin(self.rotation*pi/180.0)
            heading_y = cos(self.rotation*pi/180.0)
            heading = Vector2(heading_x, heading_y)
            
            self.location += heading * self.speed
            
            if not self.soundChannel.get_busy():
                self.soundChannel.play(self.drivingSound, -1)

        # no more rotation to do => handle next action
        if not self.rotationToDo and self.actionQueue:
            moveAction = self.actionQueue.pop()
            direction = moveAction.direction
            if direction in [LEFT, RIGHT]:
                self.steer(direction)
            elif direction == UP:
                self.accelerate()
            elif direction == DOWN:
                self.brake()
            elif direction == STOP:
                self.brakeHard()
        
class Player(AnimatedGameEntity):
    def __init__(self, start_coordinates):
        self.image = pygame.image.load('../images/nedde.png').convert_alpha()
        self.location = start_coordinates
        
        self.speed = 40.0
        self.walking_direction = Vector2(0, 0)
        self.name = "player"
        self.foodAmount = 15
        self.vehicle = None
       
    def switchVehicle(self, vehicle):
        self.speed = 0.0
        if self.vehicle == vehicle:
            self.vehicle.move(STOP)
            self.vehicle = None
            self.location = vehicle.location + Vector2(-20,0)    
        elif self.vehicle == None and Vector2.get_distance(self.location, vehicle.location) <= 50:
            self.vehicle = vehicle
            self.vehicle.start()
            
    def render(self, surface, worldCoords):
        if self.vehicle is not None:
            return
        
        GameEntity.render(self, surface, worldCoords)
       
    def move(self, direction):
        if self.vehicle is not None:
            self.vehicle.move(direction)
        else:
            self.speed = 40.0
            self.walking_direction = direction   
                 
    def process(self, time_passed):
        if not self.vehicle:
            self.location += self.walking_direction * time_passed * self.speed        
        
    def dropFood(self):
        if self.foodAmount <= 0 or self.vehicle:
            return None
        else:
            self.foodAmount -= 1
            return Food(self.location - Vector2(10,0))
        
        