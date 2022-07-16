import pygame
import gui


class StartMenu(object):
    def __init__(self, screen, clock, fps, font):
        self.screen = screen
        self.clock = clock
        self.fps = fps
        self.font = font
        self.text_surface_title = self.font.render('GTA', True, 'black') #text, antialias, color
        self.buttonStartGame = gui.Button(300, 200, 200, 50, 'start game', self.font, 'green', self.startGame)
        self.buttonEndGame = gui.Button(300, 350, 200, 50, 'end game', self.font, 'red', self.endGame)

    def addGameLoop(self, gameLoop):
        self.gameLoop = gameLoop

    def loop(self):
        running = True
        while running:
            #event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
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
        self.gameLoop.loop()
        
    def endGame(self):
        print('end game')
        pygame.quit()
    

if __name__ == '__main__':
    pygame.init()
    camW, camH = 800, 600
    screen = pygame.display.set_mode((camW, camH))
    camera = screen.get_rect()
    clock = pygame.time.Clock()
    fps = 60
    font = pygame.font.Font(pygame.font.get_default_font(), 36)

    startMenu = StartMenu(screen, clock, fps, font)
    startMenu.loop()
