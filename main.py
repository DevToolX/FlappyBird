import time, random, pygame
from typing import Any
from pygame.locals import *
from pygame.sprite import _Group





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



class Bird(pygame.sprite.Sprite):


    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)


        self.images= [



        ]

        self.speed= SPEED

        self.current_image=0
    



    def update():
        pass 




    def bump(self):
        self.speed = -SPEED




    def begin(self):
        pass 





"""


    This Part of the Code deals with the Pipes of the Game

"""





class Pipe(pygame.sprite.Sprite):


    def __init__(self, *groups: _Group) -> None:
        super().__init__(*groups)





    def update():
        pass 






"""
The Management of the Ground of the Game

"""

class ground(pygame.sprite.Sprite):


    def __init__(self, *groups: _Group) -> None:
        super().__init__(*groups)


    

    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)
    



class randompipes():

    def __init__(self) -> None:
        pass


