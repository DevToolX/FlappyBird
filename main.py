import time, random, pygame
from pygame.locals import *





#Declare the Global Variables

SCREEN_WIDHT = 400
SCREEN_HEIGHT = 600
SPEED = 20   
GRAVITY = 2.5
GAME_SPEED = 15

GROUND_WIDHT = 2 * SCREEN_WIDHT
GROUND_HEIGHT= 100

PIPE_WIDHT = 80
PIPE_HEIGHT = 500
PIPE_GAP = 150  




""""
This Class I will use to control the Game and what comes before and after
"""

class MasterClass(pygame.sprite.Sprite):

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))
        pygame.display.set_caption('Flappy Bird')

        self.BACKGROUND = pygame.image.load('assets/sprites/background-day.png')
        self.BACKGROUND = pygame.transform.scale(self.BACKGROUND, (SCREEN_WIDHT, SCREEN_HEIGHT))
        self.BEGIN_IMAGE = pygame.image.load('assets/sprites/message.png').convert_alpha()
        

        #Define the Sounds that the birds makes 
        self.wing = 'assets/audio/wing.wav'
        self.hit = 'assets/audio/hit.wav'

        self.bird_group = pygame.sprite.Group()
        self.bird = Bird() 
        self.bird_group.add(self.bird)
    
        self.ground_group = pygame.sprite.Group()
        
        for i in range (2):
            self.ground = Ground(GROUND_WIDHT * i)
            self.ground_group.add(self.ground)

        
        self.pipe_group = pygame.sprite.Group()
        for i in range (2):
            self.pipes = gamePlay.get_random_pipes(SCREEN_WIDHT * i + 800)
            self.pipe_group.add(self.pipes[0])
            self.pipe_group.add(self.pipes[1])



        self.clock = pygame.time.Clock()
        self.begin = True

        while self.begin:

            self.clock.tick(15)

            for event in pygame.event.get():
                if event.type == QUIT:
                     pygame.quit()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE or event.key == K_UP:
                        self.bird.bump()
                        pygame.mixer.music.load(self.wing)
                        pygame.mixer.music.play()
                        self.begin = False

            
            self.screen.blit(self.BACKGROUND, (0, 0))
            self.screen.blit(self.BEGIN_IMAGE, (120, 150))

            if gamePlay.is_off_screen(self.ground_group.sprites()[0]):
                self.ground_group.remove(self.ground_group.sprites()[0])

            self.new_ground = Ground(GROUND_WIDHT - 20)
            self.ground_group.add(self.new_ground)

            self.bird.begin()
            self.ground_group.update()

            self.bird_group.draw(self.screen)
            self.ground_group.draw(self.screen)

            pygame.display.update()


        while True:

            self.clock.tick(15)

            for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                    if event.type == KEYDOWN:
                        if event.key == K_SPACE or event.key == K_UP:
                            self.bird.bump()
                            pygame.mixer.music.load(self.wing)
                            pygame.mixer.music.play()

            self.screen.blit(self.BACKGROUND, (0, 0))

            if gamePlay.is_off_screen(self.ground_group.sprites()[0]):
                    self.ground_group.remove(self.ground_group.sprites()[0])

                    self.new_ground = Ground(GROUND_WIDHT - 20)
                    self.ground_group.add(self.new_ground)

            if gamePlay.is_off_screen(self.pipe_group.sprites()[0]):
                    self.pipe_group.remove(self.pipe_group.sprites()[0])
                    self.pipe_group.remove(self.pipe_group.sprites()[0])

                    pipes = gamePlay.get_random_pipes(SCREEN_WIDHT * 2)

                    self.pipe_group.add(pipes[0])
                    self.pipe_group.add(pipes[1])

            self.bird_group.update()
            self.ground_group.update()
            self.pipe_group.update()

            self.bird_group.draw(self.screen)
            self.pipe_group.draw(self.screen)
            self.ground_group.draw(self.screen)

            pygame.display.update()

            if (pygame.sprite.groupcollide(self.bird_group, self.ground_group, False, False, pygame.sprite.collide_mask) or
                        pygame.sprite.groupcollide(self.bird_group, self.pipe_group, False, False, pygame.sprite.collide_mask)):
                    pygame.mixer.music.load(self.hit)
                    pygame.mixer.music.play()
                    time.sleep(1)
            




class Bird(pygame.sprite.Sprite):

    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)


        self.images =  [pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha(),
                        pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha(),
                        pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha()]

        self.speed= SPEED

        
        self.current_image = 0
        self.image = pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDHT / 6
        self.rect[1] = SCREEN_HEIGHT / 2



    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        self.speed += GRAVITY

        #UPDATE HEIGHT
        self.rect[1] += self.speed


    def bump(self):
        self.speed = -SPEED


    def begin(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]



"""
 This Part of the Code deals with the Pipes of the Game

"""



class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self. image = pygame.image.load('assets/sprites/pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDHT, PIPE_HEIGHT))


        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize


        self.mask = pygame.mask.from_surface(self.image)


    def update(self):
        self.rect[0] -= GAME_SPEED

"""
The Management of the Ground of the Game
"""

class Ground(pygame.sprite.Sprite):
    
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/sprites/base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDHT, GROUND_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT
    def update(self):
        self.rect[0] -= GAME_SPEED





class gamePlay:


    def is_off_screen(sprite):
        return sprite.rect[0] < -(sprite.rect[2])


    #Also need to increase the dificullty of the game base on the score
    #I will Add an if Statment to check the score and change the Pipes Hight 
    def get_random_pipes(xpos):
        size = random.randint(100, 300)
        pipe = Pipe(False, xpos, size)
        pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
        return pipe, pipe_inverted



    #Keep Tracks of the High score of the Game
    #Use a context Manager
    def highScore():
        #Define the Path 
        with open("highscore.json", "r+") as score:
            score.dump()

        pass 




if __name__ == "__main__":
    MasterClass()