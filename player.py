import pygame
from pygame.math import Vector2
from math import cos, sin, tan, radians, degrees, ceil, sqrt
import dynamic_objects

class Player(dynamic_objects.Car):
    def __init__(self, x, y, w, h, ppu, angle=0.0):
        dynamic_objects.Car.__init__(self, x, y, w, h, ppu, angle)
