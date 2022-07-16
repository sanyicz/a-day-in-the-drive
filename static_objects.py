import pygame
from pygame.math import Vector2
from math import pi, sin, cos


class StaticObject(pygame.sprite.Sprite): #inherit from pygame.sprite.Sprite?
    def __init__(self, x, y, w, h, ppu, model_name, angle=0.0):
        pygame.sprite.Sprite.__init__(self)
        self.position = Vector2(x, y)
        self.angle = angle
##        angle = pi * (angle / 180)
##        self.width = w * cos(angle) + h * sin(angle)
##        self.height = w * sin(angle) + h * cos(angle)
        self.width = w
        self.height = h
        self.rect = pygame.Rect(x - self.width//2, y - self.height//2, self.width, self.height)
        self.original_image = model_name #image must be converted
        self.object_type = 'object_type'
        
        self.ppu = ppu
        self.original_image = pygame.transform.scale(self.original_image, ( int(self.ppu * self.width), int(self.ppu * self.height) ))
        self.original_image = pygame.transform.rotate(self.original_image, self.angle)
        self.image = self.original_image
        
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self, dt, objects):
        #update movement by dt time
        #check for collision with objects
        pass
    
    def draw(self, screen, camera):
        #draw on the screen
        #calculate world coordinates into display coordinates
        rect = self.image.get_rect()
        x = self.position.x - camera['x']
        y = self.position.y - camera['y']
        x_ = x * self.ppu
        y_ = y * self.ppu
        x__ = x_ - rect.width / 2
        y__ = y_ - rect.height / 2
        screen.blit(self.image, (x__,y__))

    def effect(self, car):
        pass

    def __del__(self):
        self.kill()
        print(self.object_type + ' deleted.')


class Collectible(StaticObject):
    def __init__(self, x, y, w, h, ppu, model_name, angle=0.0):
        StaticObject.__init__(self, x, y, w, h, ppu, model_name, angle=0.0)

    def setEffect(self, value, hp):
        self.value = value
        self.hp = hp

    def effect(self, car):
        car.money += self.value
        car.hp = min(car.maxhp, car.hp + self.hp)


class Water(StaticObject):
    def __init__(self, x, y, w, h, ppu, model_name, angle=0.0):
        StaticObject.__init__(self, x, y, w, h, ppu, model_name, angle=0.0)
        pygame.mixer.init()
        self.splashSound = pygame.mixer.Sound('sounds/splash.ogg')

    def effect(self, car):
        car.hp = 0
        self.splashSound.play()
