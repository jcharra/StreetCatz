
import pygame
from pygame.locals import *

class LevelBuilder(object):
    def __init__(self):
        loadImage = lambda f: pygame.image.load('../images/scenery/%s' % f)
        self.background_color = (23, 179, 23)
        STREET_STRAIGHT = loadImage('streetStraight.png') 
        STREET_STRAIGHT_UP = loadImage('streetStraightUp.png')
        BEND_BOTTOM_LEFT = loadImage('bendbottomleft.png')
        BEND_LEFT_UP = loadImage('bendleftup.png')
        BEND_UP_RIGHT = loadImage('bendupright.png')
        BEND_BOTTOM_RIGHT = loadImage('bendbottomright.png')
        
        self.expected_image_width = 120
        self.expected_image_height = 120
        
        self.characterMap = {'-': STREET_STRAIGHT,
                             '|': STREET_STRAIGHT_UP,
                             'r': BEND_BOTTOM_RIGHT,
                             ')': BEND_LEFT_UP,
                             'l': BEND_BOTTOM_LEFT,
                             '(': BEND_UP_RIGHT,}
    
    def buildLevelFromFile(self, filename):
        file = open(filename)
        lines = file.readlines()
        width, height = max([len(x) for x in lines]), len(lines)
        
        image = pygame.surface.Surface((width * self.expected_image_width, height * self.expected_image_height))
        image.fill(self.background_color)
        
        x = y = 0
        for line in lines:
            for char in line:
                img = char in self.characterMap and self.characterMap[char]
                if img:
                    image.blit(img, (x, y))
                x += self.expected_image_width
            x = 0
            y += self.expected_image_height
        
        return image
    
if __name__ == "__main__":
    screen = pygame.display.set_mode((800, 600), 0, 32)
    builder = LevelBuilder()
    level = builder.buildLevelFromFile('../levels/level1.txt')
    
    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        
        screen.blit(level, (0, 0))
        
        pygame.display.update()