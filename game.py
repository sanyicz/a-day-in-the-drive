import pygame
from math import copysign
import player
import static_objects
import dynamic_objects
import os
from random import randint
import world_map
import numpy as np
import PIL.Image
import loadmapimage_test
import gui



############################################################
class Game(object):
    def __init__(self, screen, clock, fps, font, ppu):
        self.screen = screen
        self.clock = clock
        self.fps = fps
        self.font = font
        self.ppu = ppu #pixel per unit distance
        W, H = screen.get_size()
        self.camW, self.camH = W / self.ppu, H / self.ppu #in meters

    def startMenuLoop(self):
        self.text_surface_title = self.font.render('GTA', True, 'black') #text, antialias, color
        self.buttonStartGame = gui.Button(300, 200, 200, 50, 'start game', self.font, 'green', self.startGame)
        self.buttonEndGame = gui.Button(300, 350, 200, 50, 'end game', self.font, 'red', self.endGame)

        self.startMenuLoopRunning = True
        while self.startMenuLoopRunning:
            #event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.startMenuLoopRunning = False
                self.buttonStartGame.update(event)
                self.buttonEndGame.update(event)

            self.screen.fill('white')
            self.screen.blit(self.text_surface_title, dest=(0, 0))
            self.buttonStartGame.draw(self.screen)
            self.buttonEndGame.draw(self.screen)

            pygame.display.flip()

            self.clock.tick(self.fps)

    def startGame(self):
        print('start gameLoop')
        self.gameLoop()
        
    def endGame(self):
        print('end game')
        pygame.quit()
        
    def createCar(self, position, angle=0.0):
        self.car = player.Player(*position, 4, 2, self.ppu) #x, y, w, h, ppu
        self.car.angle = angle
        self.camera = {'x' : self.car.position.x, 'y': self.car.position.y, 'w' : self.camW, 'h' : self.camH}

    def loadMusic(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.musicList = os.listdir(current_dir + '/music')
        self.musicList = [current_dir + '/music/' + music for music in self.musicList]
        self.actualMusicIndex = randint(0, len(self.musicList)-1)
##        print(self.musicList)

    def playMusic(self, actualMusicIndex):
        nextMusicIndex = randint(0, len(self.musicList)-1)
        while nextMusicIndex == actualMusicIndex:
            nextMusicIndex = randint(0, len(self.musicList)-1)
        music = self.musicList[nextMusicIndex]
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1) #-1 means that the music repeats indefinately
        return nextMusicIndex

    def loadWorldMap(self, data=None, flyerData=None):
        print('Loading map...')
        self.worldMap = world_map.WorldMap(self.ppu)
        self.worldMap.loadModels()
##        print(data)
##        print(data['tree1'][:15])
        self.boxCount = len(data['box1'])
##        print(f'box1 count: {self.boxCount}')
        if data != None:
            self.worldMap.createFromData(data)
        else:
            print('No map data')
        self.objects = self.worldMap.objects
        self.road_network = self.worldMap.road_network
        
        self.visible_objects_range = 2 * max(self.camW, self.camH)
        self.visible_objects = pygame.sprite.Group()
        self.getVisibleObjects()

        if flyerData != None:
            self.worldMap.createFlyersFromData(flyerData)
        else:
            print('No flyer data')
        self.flyers = self.worldMap.flyers
        print('...map loaded')

    def getVisibleObjects(self):
        for obj in self.objects:
            if obj.position.distance_to(self.car.position) < self.visible_objects_range:
                self.visible_objects.add(obj)

    def gameLoop(self):
        print('meö')
        self.dt = 0
        H, M, S = 0, 0, 0
        playTime = { 'H' : H, 'M' : M, 'S' : S}
        seconds, minutes, hours = 0, 0, 0
        
        self.gameLoopRunning = True
        while self.gameLoopRunning:
            #event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameLoopRunning = False
            #user input
            pressed = pygame.key.get_pressed() #returns a list of button states
            #quit
            if pressed[pygame.K_ESCAPE]:
                self.gameLoopRunning = False
                break
            #radio
            if pressed[pygame.K_r]:
                self.actualMusicIndex = self.playMusic(self.actualMusicIndex)#, self.musicList)
            #moving
            if pressed[pygame.K_UP]:
                if self.car.velocity.x < 0:
                    self.car.acceleration = self.car.brake_deceleration
                else:
                    self.car.acceleration += 1 * self.dt
            elif pressed[pygame.K_DOWN]:
                if self.car.velocity.x > 0:
                    self.car.acceleration = -self.car.brake_deceleration
                else:
                    self.car.acceleration -= 1 * self.dt
            elif pressed[pygame.K_SPACE]:
                if abs(self.car.velocity.x) > self.dt * self.car.brake_deceleration:
                    self.car.acceleration = -copysign(self.car.brake_deceleration, self.car.velocity.x)
                else:
                    self.car.acceleration = -self.car.velocity.x / self.dt
            else:
                if abs(self.car.velocity.x) > self.dt * self.car.free_deceleration:
                    self.car.acceleration = -copysign(self.car.free_deceleration, self.car.velocity.x)
                else:
                    if self.dt != 0:
                        self.car.acceleration = -self.car.velocity.x / self.dt
            self.car.acceleration = max(-self.car.max_acceleration, min(self.car.acceleration, self.car.max_acceleration))
            #turning
            if pressed[pygame.K_RIGHT]:
                self.car.steering -= 30 * self.dt
            elif pressed[pygame.K_LEFT]:
                self.car.steering += 30 * self.dt
            else:
                self.car.steering = 0
            self.car.steering = max(-self.car.max_steering, min(self.car.steering, self.car.max_steering))

            
            #updating
            self.collider = self.car.update(self.dt, self.visible_objects)
            if isinstance(self.collider, static_objects.Collectible):
                self.collider.effect(self.car)
                self.objects.remove(self.collider)
                self.car.boxes += 1
            elif isinstance(self.collider, static_objects.Water):
##                self.collider.effect(self.car)
                self.car.position.x, self.car.position.y = 38, 288
                self.car.hp = 10

            if self.car.hp <= 0:
                print('Game over')
##                self.car.max_velocity = 0
                self.gameLoopRunning = False
            if self.car.boxes == self.boxCount:
                print(playTime)
                print('You won')

            self.flyers.update(self.dt)


            #camera position 1
        ##    iprev, jprev = gridPos[0], gridPos[1]
        ##    gridPos = checkGridPos(car, gridPos)
        ##    i, j = gridPos[0], gridPos[1]
        ##    if i != iprev or j != jprev:
        ##        camera = {'x' : i * camW, 'y': j * camH, 'w' : camW, 'h' : camH}
        ##        visible_objects = []
        ##        for obj in objects:
        ##            if obj.position.distance_to(car.position) < 2 * camW:
        ##                visible_objects.append(obj)
            #camera position 2
            self.camera['x'] = self.car.position.x - self.camW / 2
            self.camera['y'] = self.car.position.y - self.camH / 2


            #drawing
            self.screen.fill('chartreuse4')
        ##    screen.blit(ground, dest=(-(camera['x'] + car.width) * ppu, -(camera['y'] + car.height) * ppu))
            #if objects is a sprite group: objects.draw(screen) + ppu
            for self.obj in self.road_network:
                self.obj.draw(self.screen, self.camera)
            self.visible_objects.empty()
            for self.obj in self.objects:
                if self.obj.position.distance_to(self.car.position) < self.visible_objects_range:
                    self.visible_objects.add(self.obj)
            for self.obj in self.visible_objects:
                self.obj.draw(self.screen, self.camera)
            self.car.draw(self.screen, self.camera)
            
            for flyer in self.flyers:
                flyer.draw(self.screen, self.camera)


            #night settings, must be improved!
            w, h = self.screen.get_size()
            s = pygame.Surface((w, h))
##            s.fill((0, 0, 0, 255))
##            s.set_colorkey((0, 0, 0, 255))
            pygame.draw.rect(s, (0, 0, 0), (0, 0, 200, 100))
            s.set_alpha(200)
            self.screen.blit(s, (0, 0))


            #hud
            text_surface_hp = self.font.render('HP: ' + str(self.car.hp), True, 'black') #text, antialias, color
            self.screen.blit(text_surface_hp, dest=(0, 0))
            text_surface_money = self.font.render('Money: ' + str(self.car.money), True, 'black') #text, antialias, color
            self.screen.blit(text_surface_money, dest=(0, 36))
            text_surface_v = self.font.render('V: ' + str(int(self.car.velocity.magnitude())), True, 'black') #text, antialias, color
            self.screen.blit(text_surface_v, dest=(0, 72))
            text_surface_fps = self.font.render('FPS: ' + str(int(self.clock.get_fps())), True, 'black') #text, antialias, color
            self.screen.blit(text_surface_fps, dest=(0, 108))
            text_surface_boxes = self.font.render('Boxes: ' + str(self.boxCount) + '/' + str(self.car.boxes), True, 'black') #text, antialias, color
            self.screen.blit(text_surface_boxes, dest=(0, 144))
            text_surface_timer = self.font.render('Time: ' + str(playTime['H']) + ':' + str(playTime['M']) + ':' + str(playTime['S']), True, 'black') #text, antialias, color
            self.screen.blit(text_surface_timer, dest=(0, 180))
            
            pygame.display.flip()
            
            self.dt = self.clock.tick(self.fps) / 1000 #elapsed time since the last frame in seconds

            seconds += self.dt
            minutes = seconds // 60
            hours = minutes // 60
            H, M, S = hours % 24, minutes % 60, seconds % 60
            playTime['H'] = int(H)
            playTime['M'] = int(M)
            playTime['S'] = int(S)
        pygame.quit()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Game')
    W, H = 800, 600 #camera width and height in pixels
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()
    fps = 60
    font = pygame.font.Font(pygame.font.get_default_font(), 36)
    ppu = 20

    image = PIL.Image.open('world1.png')
    image = np.array(image)
    worldWidth, worldHeight, rgba = image.shape
    startX, startY = loadmapimage_test.findStart(image, loadmapimage_test.colors['pink'])
    print(f'startX, startY: {startX, startY}')
    angle = 10
    
    game = Game(screen, clock, fps, font, ppu)
    game.createCar((startX, startY), angle)
    game.loadMusic()

    
    data = loadmapimage_test.findObjectsInImage(image, loadmapimage_test.object_definitions)
    game.loadWorldMap(data)
    game.worldMap.createFlyers(worldWidth, worldHeight, 50, 0)
##    flyerData = {'cloud1' : [ [-100, 20, 10, 7], [-120, 10, 10, 7], ], 'bird1' : []}
##    game.loadWorldMap(data, flyerData)

    game.startMenuLoop()
    game.gameLoop()

##########################################################
