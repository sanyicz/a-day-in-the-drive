import pygame
##from math import copysign
##import car
##import static_objects
##import os
##from random import randint
##import world_map
import startmenu
import gameloop


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Game')
    W, H = 800, 600 #camera width and height in pixels
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()
    fps = 60
    font = pygame.font.Font(pygame.font.get_default_font(), 36)
    ppu = 20

    gameLoop = gameloop.GameLoop(screen, clock, fps, font, ppu)
    gameLoop.createCar()
    gameLoop.loadMusic()
    gameLoop.loadWorldMap()
    
    startMenu = startmenu.StartMenu(screen, clock, fps, font)
    startMenu.addGameLoop(gameLoop)
    startMenu.loop()
    
    
##    gameLoop.loop()
