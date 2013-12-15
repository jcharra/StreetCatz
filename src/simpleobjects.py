import pygame
from gameobjects import GameEntity

class Food(GameEntity):
    NUTRITION_VALUE = 100
    
    def __init__(self, startCoordinates):
        GameEntity.__init__(self, startCoordinates, name='food')
        self.image = pygame.image.load('../images/food.png').convert_alpha()
        self.set_image(self.image)
        self.nutritionValue = self.NUTRITION_VALUE
        
    def render(self, surface, offset):
        GameEntity.render(self, surface, offset)
        surface.fill((128, 128, 128), (self.location.x - offset[0], 
                                       self.location.y - offset[1] + self.image.get_height() + 5, 
                                       self.nutritionValue/5, 4))        
