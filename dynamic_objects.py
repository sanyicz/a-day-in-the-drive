import pygame
from pygame.math import Vector2
from math import pi, cos, sin, tan, radians, degrees, ceil, sqrt
from random import randint


class Car(pygame.sprite.Sprite): #inherit from pygame.sprite.Sprite?
    def __init__(self, x, y, w, h, ppu, angle=0.0):
        pygame.sprite.Sprite.__init__(self)
        self.position = Vector2(x, y)
        self.width = w #same as length
        self.height = h
        self.rect = pygame.Rect(x-w//2, y-h//2, w, h)
        self.angle = angle
        self.velocity = Vector2(0.0, 0.0)
        self.max_steering = 30
        self.max_acceleration = 5.0
        self.max_velocity = 20
        self.brake_deceleration = 10
        self.free_deceleration = 2
        
        self.acceleration = 0.0
        self.steering = 0.0
        
        self.original_image = pygame.image.load('models/car.png')
        self.original_image = self.original_image.convert_alpha()
        self.ppu = ppu
        self.original_image = pygame.transform.scale(self.original_image, (self.ppu * self.width, self.ppu * self.height))
        self.image = self.original_image

        self.mask = pygame.mask.from_surface(self.image)
        
        self.engineSound = pygame.mixer.Sound('sounds/Car Engine Running.mp3')
        pygame.mixer.Channel(0).play(self.engineSound, loops=-1)
        self.collisionSound = pygame.mixer.Sound('sounds/Metal Crash.mp3')

        self.maxhp = 100
        self.hp = 100
        self.money = 0
        self.boxes = 0
    
    def move(self, dx, dy):
        self.position.x += dx
        self.position.y += dy
        self.rect = self.rect.move(dx, dy)

    def checkCollision(self, objects, mode='mask'):
        collider = None
        if mode == 'mask':
            #mask collision
            for obj in objects:
                offset = ( int(self.ppu * (obj.rect.x - self.rect.x)), int(self.ppu * (obj.rect.y - self.rect.y)) )
                if self.mask.overlap(obj.mask, offset):
                    collider = obj
                    break
        elif mode == 'rect':
            #rect collision
                collider = pygame.sprite.spritecollideany(self, objects)

        return collider
    
    def update(self, dt, objects):
        #update movement by dt time
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

        if self.steering:
            turning_radius = self.width / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt

        self.image = pygame.transform.rotate(self.original_image, self.angle)
        rect = self.image.get_rect()
        self.rect = pygame.Rect(self.position.x - rect.width / (2 * self.ppu), self.position.y - rect.height / (2 * self.ppu), ceil(rect.width / self.ppu), ceil(rect.height / self.ppu))
        self.rect.center = self.position
##        print(self.rect)

        self.mask = pygame.mask.from_surface(self.image)
        
        #check for collision with objects
        collider = self.checkCollision(objects, 'mask')

        if collider:
            print(f'collider: {collider.object_type}')
            a = collider.height / collider.width
            b = collider.width / collider.height
##            print('collision')
            #play crash sound
            self.collisionSound.play()

##            D = sqrt((collider.width / 2)**2 + (collider.height / 2)**2)
##            if collider.position.distance_to(self.position) <= D + max(self.width, self.height) / 2:
##                print('check for collision based on distance')
                
##            v1 = collider.position - self.position
##            v2 = Vector2( cos(radians(self.angle)), -sin(radians(self.angle)) ) #v2 could be velocity?
##            if abs(v1.angle_to(v2)) <= 90:
##                print('check for collision based on angle')
                
            if self.position.x < - b * abs(self.position.y - collider.position.y) + collider.position.x: #left quarter triangle, II.
                print('left quarter triangle')
##                print(self.position.x, self.position.y)
##                print(collider.position.x, collider.position.y)
                x1 = abs(self.position.x - collider.position.x) #actual x
                y1 = abs(self.position.y - collider.position.y) #actual y
                x2 = self.rect.width / 2 + collider.rect.width / 2 #should be x
                y2 = y1 #should be y
                dx = x1 - x2 #delta x
                dy = y1 - y2 #delta y
                dx = min(collider.width, collider.height) if dx >= 0 else dx
            elif self.position.x > b * abs(self.position.y - collider.position.y) + collider.position.x: #right quarter triangle, IV.
                print('right quarter triangle')
                x1 = abs(self.position.x - collider.position.x) #actual x
                y1 = abs(self.position.y - collider.position.y) #actual y
                x2 = self.rect.width / 2 + collider.rect.width / 2 #should be x
                y2 = y1 #should be y
                dx = x2 - x1 #delta x
                dy = y1 - y2 #delta y
                dx = min(collider.width, collider.height) if dx <= 0 else dx
            elif self.position.y > a * abs(self.position.x - collider.position.x) + collider.position.y: #upper quarter triangle, I.
                print('upper quarter triangle')
                x1 = abs(self.position.x - collider.position.x) #actual x
                y1 = abs(self.position.y - collider.position.y) #actual y
                x2 = x1 #should be x
                y2 = self.rect.height / 2 + collider.rect.height / 2 #should be y
                dx = x1 - x2 #delta x
                dy = y2 - y1 #delta y
                print(f'dx, dy: {dx}, {dy}')
                dy = min(collider.width, collider.height) if dy <= 0 else dy
            elif self.position.y < - a * abs(self.position.x - collider.position.x) + collider.position.y: #lower quarter triangle, III.
                print('lower quarter triangle')
                x1 = abs(self.position.x - collider.position.x) #actual x
                y1 = abs(self.position.y - collider.position.y) #actual y
                x2 = x1 #should be x
                y2 = self.rect.height / 2 + collider.rect.height / 2 #should be y
                dx = x1 - x2 #delta x
                dy = y1 - y2 #delta y
                dy = min(collider.width, collider.height) if dy >= 0 else dy
            else:
                print('else')
                dx, dy = 0, 0
                #x1, y1, x2, y2 = 0, 0, 0, 0
#                dx = x1 - x2 #delta x
#                dy = y1 - y2 #delta y
##            print(f'x1, y1: {x1}, {y1}')
##            print(f'x2, y2: {x2}, {y2}')
            print(f'Final dx, dy: {dx}, {dy}')

##            if 'fence' in collider.object_type:
##                if dx == 0:
##                    dx = max(dx, min(collider.width, collider.height))
##                if dy == 0:
##                    dy = max(dy, min(collider.width, collider.height))
##                print(f'dx, dy: {dx}, {dy}')
                
##            dx *= 1.1
##            dy *= 1.1
                    
            self.move(dx, dy)
            self.hp = int( self.hp - self.velocity.magnitude()**2 // self.max_velocity)
            self.velocity = Vector2(0.0, 0.0)
            self.acceleration = 0.0

        self.rect.center = self.position
##        print(self.rect)

        return collider
        
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


class NPC(Car):
    def __init__(self, x, y, w, h, ppu, angle=0.0):
        Car.__init__(self, x, y, w, h, ppu, angle)


class Flyer(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, ppu, model_name, angle=0.0):
        pygame.sprite.Sprite.__init__(self)
        self.position = Vector2(x, y)
        self.width = w #same as length
        self.height = h
        self.rect = pygame.Rect(x-w//2, y-h//2, w, h)
        self.angle = angle
        self.velocity = Vector2(0.0, 0.0)

        self.original_image = model_name #image must be converted
        self.object_type = 'object_type'
        
        self.ppu = ppu
        self.original_image = pygame.transform.scale(self.original_image, ( int(self.ppu * self.width), int(self.ppu * self.height) ))
        self.original_image = pygame.transform.rotate(self.original_image, self.angle)
        self.image = self.original_image
        
        self.mask = pygame.mask.from_surface(self.image)

    def setVelocity(self, vx, vy):
        self.velocity = Vector2(vx, vy)

    def setWorldSize(self, worldWidth, worldHeight):
        self.worldWidth, self.worldHeight = worldWidth, worldHeight

    def move(self, dx, dy):
        self.position.x += dx
        self.position.y += dy
        self.rect = self.rect.move(dx, dy)

    def update(self, dt):
        self.position += self.velocity.rotate(-self.angle) * dt
        if self.position.x >= self.worldWidth:
            self.position.x, self.position.y = 0, randint(0, self.worldHeight)
        if self.position.y >= self.worldHeight:
            self.position.x, self.position.y = randint(0, self.worldWidth), 0
        self.rect.center = self.position
##        print(dt, self.position)

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

