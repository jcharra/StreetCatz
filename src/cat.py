import pygame
from gameobjects import AnimatedGameEntity
from simpleobjects import Food
from statemachine import StateMachine, State
from random import randint 
from vectors import Vector2

class Cat(AnimatedGameEntity):
    roamingImage = pygame.image.load('../images/catRoaming.png')
    eatingImage = pygame.image.load('../images/catEating.png')
        
    meowSound = pygame.mixer.Sound('../sounds/meow.ogg')    
    eatingSound = pygame.mixer.Sound('../sounds/chew.ogg')
    
    THRESHOLD_HUNGRY = 30
    THRESHOLD_VERY_HUNGRY = 50
        
    def __init__(self, startCoordinates, world, name='cat'):
        AnimatedGameEntity.__init__(self, startCoordinates, name=name)
        self.hunger = 35
        
        self.brain.add_state(CatRoaming(self))
        self.brain.add_state(CatRunningToPot(self))
        self.brain.add_state(CatEating(self))
          
        self.destination = self.location  
        self.world = world
        self.pot = None
        self.hungerColor = (0, 255, 0)
        
        self.perceptionRange = 250
        
        self.brain.set_state("roaming")
      
    def process(self, time_passed):
        r = randint(1, 10000)
        if r < self.hunger:
            self.meowSound.play()
        
        if self.hunger > self.THRESHOLD_HUNGRY:
            self.hungerColour = (255, 0, 0)    
        elif self.hunger > self.THRESHOLD_VERY_HUNGRY:
            self.hungerColour = (255, 255, 0)
        else:
            self.hungerColour = (0, 255, 0)
            
        AnimatedGameEntity.process(self, time_passed)
        
    def render(self, surface, offset):
        AnimatedGameEntity.render(self, surface, offset)
        surface.fill(self.hungerColour, (self.location.x - offset[0], 
                                         self.location.y - offset[1] + self.image.get_height() + 5, 
                                         self.hunger, 4))
        
class CatRoaming(State):
    def __init__(self, cat):
        State.__init__(self, "roaming")
        self.cat = cat        
    
    def findRandomTarget(self):
        self.cat.destination = self.cat.location + Vector2(randint(-200, 200), randint(-200, 200))
    
    def do_actions(self):
        r = randint(1, 2000)
        if r < 50:
            self.cat.hunger += 2
        if r < 10:
            self.findRandomTarget()
        
    def entry_actions(self):
        self.cat.set_image(self.cat.roamingImage, 4)
        self.cat.speed = 15 + randint(1,10)
        self.findRandomTarget()
                 
    def check_conditions(self):
        if self.cat.hunger > Cat.THRESHOLD_HUNGRY:
            nearPot = self.cat.world.get_closest_entity(self.cat.location, 
                                                        Food, 
                                                        self.cat.perceptionRange, 
                                                        validityTest=lambda x: x.nutritionValue > 0)
            if nearPot:
                self.cat.pot = nearPot
                return "runningToPot"
        
        return None

class CatRunningToPot(State):
    def __init__(self, cat):
        State.__init__(self, "runningToPot")
        self.cat = cat
        
    def entry_actions(self):
        self.cat.set_image(self.cat.roamingImage, 4)
        self.cat.speed = 100
        self.cat.animationSpeed = 0.1
        self.cat.destination = self.cat.pot.location - Vector2(30, 0)
        
    def check_conditions(self):
        if self.cat.pot is not None and Vector2.get_distance(self.cat.location, self.cat.destination) < 10:
            return "eating"
        return None
        
class CatEating(State):
    def __init__(self, cat):
        State.__init__(self, "eating")
        self.cat = cat
    
    def do_actions(self):
        if randint(1, 10) == 1:
            self.cat.hunger -= 1
            self.cat.eatingSound.play()
            self.cat.pot.nutritionValue -= 1
            if self.cat.pot.nutritionValue <= 0:
                self.cat.pot = None
        
    def entry_actions(self):
        self.cat.set_image(self.cat.eatingImage, 1)
        self.cat.speed = 0
                
    def check_conditions(self):
        if self.cat.hunger <= 10 or self.cat.pot is None:
            return "roaming"
        return None

        
        
        
        
        
