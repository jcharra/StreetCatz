import pygame
from statemachine import StateMachine
from vectors import Vector2 
from random import randint

class GameEntity(object):
    def __init__(self, startCoordinates, name=''):
        self.location = startCoordinates
        self.name = name
        
    def set_image(self, image):
        self.image = image
        
    def render(self, surface, offset):
        surface.blit(self.image, (self.location.x - offset[0],
                                  self.location.y - offset[1]))
 
class AnimatedGameEntity(GameEntity):
    def __init__(self, startCoordinates, name=''):
        GameEntity.__init__(self, startCoordinates, name)
        self.frameNumber = 1
        self.imageFrame = 0
        self.frameTime = 0.
        self.animationSpeed = 0.5 + randint(-3, 3) / 10.0
        self.frameWidth = 0
        self.speed = 0
        self.width = self.height = 0
        self.brain = StateMachine()
        self.actionQueue = []
        
    def set_image(self, image, frameNumber=1):
        self.image = image
        self.frameNumber = frameNumber
        self.frameWidth = self.image.get_width() / self.frameNumber
        self.width, self.height = self.image.get_size()
        
    def render(self, surface, offset):
        surface.blit(self.image, 
                     (self.location.x - offset[0], self.location.y - offset[1]), 
                     (self.frameWidth * self.imageFrame, 0, self.frameWidth, self.height))
    
    def adjustPosition(self, dimension):
        self.location.x = min(self.location.x, dimension[0] - 20)
        self.location.x = max(self.location.x, 10)
        self.location.y = min(self.location.y, dimension[1] - 20)
        self.location.y = max(self.location.y, 10)
    
    def handleAction(self, action):
        raise NotImplementedError('Entity %s cannot handle Action %s' % (self.name, action))
    
    def process(self, time_passed):
        self.frameTime += time_passed
        if self.frameTime > self.animationSpeed:
            self.frameTime = 0.
            self.imageFrame = (self.imageFrame + 1) % self.frameNumber

        if self.speed > 0. and self.location != self.destination:
            vec_to_destination = self.destination - self.location
            distance_to_destination = vec_to_destination.get_magnitude()
            heading = vec_to_destination.get_normalized()
            travel_distance = min(distance_to_destination, time_passed * self.speed)
            self.location += heading * travel_distance
        
        if self.actionQueue:
            action = self.actionQueue.pop()
            self.handleAction(action)
        else:
            self.brain.think()


