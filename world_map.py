import pygame
import static_objects
import dynamic_objects
from random import randint


class WorldMap(object):
    def __init__(self, ppu):
        self.objects = pygame.sprite.Group()
        self.road_network = []
        self.flyers = pygame.sprite.Group()
        self.ppu = ppu

    def loadModels(self):
        #load images
        self.images = {}
        self.images['road1'] = pygame.image.load('models/road1.png').convert_alpha()
        self.images['road2'] = pygame.image.load('models/road2.png').convert_alpha()
        self.images['road3'] = pygame.image.load('models/road3.png').convert_alpha()
        self.images['field1'] = pygame.image.load('models/field1.png').convert_alpha()

        self.images['house1'] = pygame.image.load('models/house1.png').convert_alpha()
        self.images['house2'] = pygame.image.load('models/house2.png').convert_alpha()
        self.images['shop1'] = pygame.image.load('models/shop1.png').convert_alpha()
        self.images['post1'] = pygame.image.load('models/post1.png').convert_alpha()
        self.images['church1'] = pygame.image.load('models/church1.png').convert_alpha()
        self.images['school1'] = pygame.image.load('models/school1.png').convert_alpha()

        self.images['tree1'] = pygame.image.load('models/tree1.png').convert_alpha()

        self.images['fence1'] = pygame.image.load('models/fence1.png').convert_alpha()
        self.images['fence2'] = pygame.image.load('models/fence2.png').convert_alpha()

        self.images['water1'] = pygame.image.load('models/water1.png').convert_alpha()

        self.images['box1'] = pygame.image.load('models/box1.png').convert_alpha()

        self.images['car_blue'] = pygame.image.load('models/car_blue.png').convert_alpha()
        self.images['truck_red'] = pygame.image.load('models/truck_red.png').convert_alpha()

        self.images['bird1'] = pygame.image.load('models/bird1.png')
        self.images['cloud1'] = pygame.image.load('models/cloud1.png') #load image of a cloud
##        self.images['cloud1'].set_colorkey(pygame.Color('white')) #white colors will not be blitted
        self.images['cloud1'].set_alpha(128) #set transparency
        
    def createFromData(self, data):
        #data = {model_name1 : [ [data1], [data2], [data3], ...],  model_name2 : [ [data1], [data2], ... ], ...}
        for key, value in data.items():
            image = self.images[key]
            if 'road' in key or 'field' in key:
                for row in value:
                    self.road_network.append(static_objects.StaticObject(*row, self.ppu, image))
            elif 'fence' in key:
                for row in value:
                    x, y, deltax, deltay = row
                    if deltax == 1:
                        self.objects.add(static_objects.StaticObject(x, y, 0.4, deltay, self.ppu, self.images['fence1']))
                    elif deltay == 1:
                        self.objects.add(static_objects.StaticObject(x, y, deltax, 0.4, self.ppu, self.images['fence1']))
            elif 'water' in key:
                for row in value:
                    self.objects.add(static_objects.Water(*row, self.ppu, image))
            elif 'box' in key:
                for row in value:
                    box = static_objects.Collectible(*row, self.ppu, image)
                    box.setEffect(100, 10)
                    self.objects.add(box)
            elif 'car' in key:
                for row in value:
                    x, y, dx, dy = row
                    self.objects.add(static_objects.StaticObject(x, y, dx - 1, dy - 1, self.ppu, image))
            else:
                for row in value:
                    self.objects.add(static_objects.StaticObject(*row, self.ppu, image))

    def createFlyersFromData(self, data):
        for key, value in data.items():
            image = self.images[key]
            for row in value:
                flyer = dynamic_objects.Flyer(*row, self.ppu, image)
                flyer.setVelocity(5, 0) #encode velocity in data!
                self.flyers.add(flyer)

    def createFlyers(self, worldWidth, worldHeight, nrOfClouds, nrOfBirds):
        #randomly generate Flyer objects
        wx, wy = 5, 0
        cloudImage = self.images['cloud1']
        for i in range(nrOfClouds):
            x, y, w, h = randint(0, 300), randint(0, 300), randint(5, 15), randint(4, 7)
            cloud = dynamic_objects.Flyer(x, y, w, h, self.ppu, cloudImage)
            cloud.setWorldSize(worldWidth, worldHeight)
            cloud.setVelocity(wx, wy)
            self.flyers.add(cloud)
        

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Game')
    W, H = 800, 600 #camera width and height in pixels
    screen = pygame.display.set_mode((W, H))
    ppu = 20

    worldMap = WorldMap(ppu)
    worldMap.loadModels()
    data = { 'house2' : [ [10, 10, 12, 10] ]}
    worldMap.createFromData(data)
    objects = worldMap.objects
    road_network = worldMap.road_network

