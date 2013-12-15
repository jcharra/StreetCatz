
import pygame
pygame.init()
pygame.mixer.set_num_channels(10)

from pygame.locals import *
from statemachine import State, StateMachine
from vectors import Vector2
from random import randint, choice
from cat import Cat
from player import Player, Car
from simpleobjects import Food
from gameobjects import GameEntity
from world import World, WorldObserver, UP, DOWN, LEFT, RIGHT
from levelbuilder import LevelBuilder

SCREEN_SIZE = (800, 600)
LEVEL_INTERMEDIATE_TIME = 550 

def runLevel(screen, level_number, cat_number) 
    finishSound = pygame.mixer.Sound('../sounds/finish.ogg')  
    builder = LevelBuilder()
    level = builder.buildLevelFromFile('../levels/level%s.txt' % level_number)
    world = World(SCREEN_SIZE, level)
    
    car = Car(Vector2(100,100))
    player = Player(Vector2(100, 180))
    
    world.add_entity(player)
    world.add_entity(car)
    world.focussed_entity = player
    
    worldobserver = WorldObserver(world)
    clock = pygame.time.Clock()
    
    for i in range(cat_number)
        cat = Cat(Vector2(randint(0, world.dimension[0]), randint(0, world.dimension[1])), world)
        world.add_entity(cat)
    
    countdown_to_next_level = LEVEL_INTERMEDIATE_TIME
    while True
        
        for event in pygame.event.get()
            if event.type == QUIT
                exit()
            if event.type == KEYDOWN
                if event.key == K_LEFT
                    player.move(LEFT)
                elif event.key == K_RIGHT
                    player.move(RIGHT)
                elif event.key == K_UP
                    player.move(UP)
                elif event.key == K_DOWN
                    player.move(DOWN)
                elif event.key == K_SPACE
                    food = player.dropFood()
                    if food is not None
                        world.add_entity(food)
                elif event.key == K_c
                    player.switchVehicle(car)
                    world.focussed_entity = player.vehicle or player
                elif event.key == K_m
                    world.minimapVisible = not world.minimapVisible
                        
        time_passed = clock.tick(30)
        
        world.process(time_passed)
        world.render(screen)
        worldobserver.writeMessages(screen)
        if worldobserver.levelFinished
            if countdown_to_next_level == LEVEL_INTERMEDIATE_TIME
                finishSound.play()
            countdown_to_next_level -= 2
            if countdown_to_next_level <= 0
                return
            
            for r in range(countdown_to_next_level+1, LEVEL_INTERMEDIATE_TIME, 8)
                pygame.draw.circle(screen, (0, 0, 0), (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2), r, 1)
        
        pygame.display.update()
        
        
if __name__ == "__main__"
    screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
    runLevel(screen, 1, 10)    
    runLevel(screen, 2, 20)
