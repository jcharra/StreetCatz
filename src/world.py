import pygame
from cat import Cat
from vectors import Vector2 
from gameobjects import AnimatedGameEntity
from simpleobjects import Food

class WorldObserver(object):
    def __init__(self, world):
        self.world = world
        self.player = world.player
        
        self.font = pygame.font.SysFont("Arial", 20)
        self.levelFinished = False
        self.focussed_entityFailed = False
         
    def writeMessages(self, surface):
        cat_hunger = 0
        if not self.levelFinished:            
            for ent in self.world.active_entities.itervalues():
                if isinstance(ent, Cat) and ent.hunger >= Cat.THRESHOLD_HUNGRY:
                    cat_hunger += ent.hunger - Cat.THRESHOLD_HUNGRY                   
        else:
            surface.blit(self.font.render('Great! All cats are happy!', 
                                            False, 
                                            (0, 0, 0), 
                                            (255, 255, 255)), 
                                          (300,300))
        if self.focussed_entityFailed:
            surface.blit(self.font.render('You do not have enough food left ... you failed this level',
                                            False, 
                                            (0, 0, 0), 
                                            (255, 255, 255)), 
                                          (200,300))    
        
        surface.blit(self.font.render('Food %s' % self.world.player.foodAmount, 
                                        False, 
                                        (0, 0, 0), 
                                        (255, 255, 255)),
                                      (10, 10))

        surface.blit(self.font.render('Cat hunger %s' % cat_hunger, 
                                        False, 
                                        (0, 0, 0), 
                                        (255, 255, 255)),
                                      (10, 40))
            
        if cat_hunger <= 0:
            self.levelFinished = True
        
        rest_nutrition = self.world.player.foodAmount * Food.NUTRITION_VALUE
        for ent in self.world.entities.itervalues():
            if isinstance(ent, Food):
                rest_nutrition += ent.nutritionValue 
        if cat_hunger > rest_nutrition:
            self.focussed_entityFailed = True 
            

        
class World(object):
    def __init__(self, display_size, background_image):
        self.entities = {}
        self.active_entities = {}
        self.entity_id = 0
        self.background = background_image
        self.dimension = self.background.get_size()
        self.focussed_entity = None
        self.display_size = display_size
        self.maximum_expansion = Vector2(*display_size).get_magnitude()
        self.minimapVisible = True
        
    def add_entity(self, entity):
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        
        if isinstance(entity, AnimatedGameEntity):
            self.active_entities[self.entity_id] = entity
        
        if entity.name == 'player':
            self.player = entity
        
        self.entity_id += 1
        
    def remove_entity(self, entity):
        del self.entities[entity.id]
        if self.active_entities.has_key(entity.id):
            del self.active_entities[entity.id]
        
    def get_entity(self, entity_id):
        if entity_id in self.entities:
            return self.entities[entity_id]
        else:
            return None
    
    def get_closest_entity(self, fromLocation, targetClass, range=1000, validityTest=None):
        closestDist = range
        closestEntity = None
        for ent in self.entities.itervalues():
            if isinstance(ent, targetClass) and Vector2.get_distance(ent.location, fromLocation) < closestDist:
                if not validityTest or validityTest(ent):
                    closestDist = Vector2.get_distance(ent.location, fromLocation)
                    closestEntity = ent
        return closestEntity
     
    def toggleMinimap(self):
        self.minimapVisible = not self.minimapVisible
        
    def setFocus(self, entity):
        self.focussed_entity = entity
             
    def process(self, time_passed):
        time_passed_seconds = time_passed / 1000.0
        for entity in self.active_entities.values():
            entity.process(time_passed_seconds)
            entity.adjustPosition(self.dimension)
           
    def render(self, surface):
        display_x = min(self.dimension[0] - self.display_size[0], max(0, self.focussed_entity.location.x - self.display_size[0]/2))
        display_y = min(self.dimension[1] - self.display_size[1], max(0, self.focussed_entity.location.y - self.display_size[1]/2))
        surface.blit(self.background, (0, 0), (display_x, display_y, self.display_size[0], self.display_size[1]))
        
        for entity in self.entities.itervalues():
            if Vector2.get_distance(self.focussed_entity.location, entity.location) <= self.maximum_expansion:
                entity.render(surface, (display_x, display_y))
        
        if self.minimapVisible:
            minimapSize = (200, 100)
            minimapOffset = (10, 490)
            pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(minimapOffset, minimapSize))
            pygame.draw.rect(surface, (255, 255, 255), 
                             pygame.Rect((minimapOffset[0]-1, minimapOffset[1]-1), (minimapSize[0]+2, minimapSize[1]+2)),
                             1)
            
            for entity in self.active_entities.itervalues():
                # render entity point on minimap
                x = minimapOffset[0] + int((minimapSize[0] * entity.location.x) / self.dimension[0])
                y = minimapOffset[1] + int((minimapSize[1] * entity.location.y) / self.dimension[1])
                if entity.name == 'player' and not entity.vehicle:
                    color = (0, 0, 255)
                    pygame.draw.circle(surface, color, (x, y), 3)
                elif entity.name == 'cat':
                    color = entity.hungerColour                    
                    pygame.draw.rect(surface, color, pygame.Rect((x, y), (2, 2)))
                elif entity.name == 'car':
                    color = (200, 200, 200)
                    pygame.draw.circle(surface, color, (x, y), 3)
                
        
          
          
            
