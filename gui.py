import pygame
from pygame.math import Vector2

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, text, font, color, action=None): #x, y, w, h parameters in pixels
        pygame.sprite.Sprite.__init__(self)
        self.position = Vector2(x, y)
        self.width = w
        self.height = h
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.inactiveColor = color
        self.activeColor = 'dark' + color
        self.color = color
        self.action = action

    def update(self, event):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.color = self.activeColor
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.action != None:
                    self.action()
            else:
                pass
        else:
            self.color = self.inactiveColor
        self.textSurface = self.font.render(self.text, True, 'black')
        self.textRect = self.textSurface.get_rect()
        self.textRect.center = self.rect.center

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.textSurface, self.textRect)

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Game')
    W, H = 800, 600
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()
    fps = 60
    font = pygame.font.Font(pygame.font.get_default_font(), 36)
    
    def startGame():
        print('start game')
    buttonStartGame = Button(300, 200, 200, 50, 'start game', font, 'green', startGame)
    def endGame():
        print('end game')
    buttonEndGame = Button(300, 350, 200, 50, 'end game', font, 'red', endGame)

    running = True
    while running:
        #event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            buttonStartGame.update(event)
            buttonEndGame.update(event)

        screen.fill('white')
        buttonStartGame.draw(screen)
        buttonEndGame.draw(screen)

        pygame.display.flip()

        clock.tick(fps)
        
    pygame.quit()
