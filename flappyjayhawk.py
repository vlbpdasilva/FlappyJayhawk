"""
EECS 448 - "Flappy Jayhawk" -- Project 3
@author Victor Berger, Jesse Yang, Jeromy Tsai, and Cammy Vo
prof: John Gibbons
University of Kansas
code freeze: April 8th, 2016 - 11:59 pm
 
Basic controls:
From the menu, press the spacebar to start game. Use the up arrow to control the Jayhawk up.
Hitting one of the moving blocks causes you to lose. Then, the user can press 'c' to restart 
or Escape to close the game.

Sources used:_____________________

Official Pygame documentation: http://www.pygame.org/docs/

Youtube video available at https://www.youtube.com/playlist?list=PL6gx4Cwl9DGAjkwJocj7vlc_mFU-4wXJq

Pipe image from http://vignette3.wikia.nocookie.net/fantendo/images/0/06/RocketPipes.png/revision/latest?cb=20100430132034

Github repository used for help with Pygame implementations: https://github.com/TimoWilken/flappy-bird-pygame

Pygame clock documentation: http://www.geon.wz.cz/pygame/ref/pygame_time.html

Python documentation regarding classes: https://docs.python.org/2/tutorial/classes.html

"""

#Import
import sys, pygame, time, os
from random import randint
from Jayhawk import *
from Pipe import *
from Background import *

#Initialization
pygame.init()

#Screen Initializations
pygame.display.set_caption("Flappy Jayhawk")
size = width, height = (600, 500)
screen = pygame.display.set_mode(size)

#Color Definitions
black = (0,0,0)
white = (255,255,255)
blue = (0, 0, 255)
red = (255, 0, 0)

#Clock Implementation
clock = pygame.time.Clock()
FPS = 15

#Font Definitions and sizes
smallFont = pygame.font.SysFont("comicsansms", 14)
medFont = pygame.font.SysFont("comicsansms", 25)
largeFont = pygame.font.SysFont("comicsansms", 50)

def load_images():
    """Load all images required by the game and return a dict of them.
    The returned dict has the following keys:
    jayhawk: The image of the Jayhawk bird.
    background: The game's background image.
    pipe: The image of the pipe (a 540px image extending both end-piece and body).
    """

    def load_image(img_file_name):
        """Return the loaded pygame image with the specified file name.
        This function looks for images in the game's images folder
        (./images/).  All images are converted before being returned to
        speed up blitting.
        Arguments:
        img_file_name: The file name (including its extension, e.g.
            '.png') of the required image, without a file path.
        """
        file_name = os.path.join('.', 'images', img_file_name)
        img = pygame.image.load(file_name)
        img.convert()
        return img

    return {'jayhawk': load_image('jayhawk.png'),
            'background': load_image('repeatTest_smw.png'),
            'pipe': load_image('pipe.png')
            # images for animating the flapping bird -- animated GIFs are
            # not supported in pygame
            #'bird-wingup': load_image('bird_wing_up.png'),
            #'bird-wingdown': load_image('bird_wing_down.png')
            }

def start_menu():
    """Create a start menu that gives the users the title of the game and the creators of the game
    Also gives users the directions to start the game and the directions to play the game.
    Users will stay on the start menu until they press the corresponding key to start the game or press x to exit the game.
    """
    intro = True

    images = load_images();
    #Scrolling background declaration
    back = Background(images['background'], images['background'].get_size(), height)
    
    while intro: 
        # Start menu is being shown
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False

        screen.fill((255, 231, 181))

        #Draw background
        screen.blit(back.image, back.rect)
        screen.blit(back.image, back.rect2)
        screen.blit(back.image, back.rect3)
        #Make background scroll
        back.scroll()

        message_to_screen("Flappy JayHawks",
                            blue,
                            -100,
                            "large")
        message_to_screen("By: Jeromy Tsai, Cammy Vo, Jesse Yang, Victor Berger",
                            blue,
                            -20,
                            "small")
        message_to_screen("Press SPACE to play!!",
                            red,
                            20,
                            "medium")

        pygame.display.update()
        pygame.time.delay(7)
        
def game_over():
    """
    Creates the game over screen that users will see when they jayhawk touches a pipe, causing the player to lose.
    """

    while 1:
        message_to_screen("Game Over",
                            blue,
                            0,
                            "large")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit
                quit()


def text_objects(text, color, size):
    """
    Creates text objects with corresponding sizes. 
    Can expand to a greater range of font size by adding more to this list.
    """
    if size == "small":
        textSurface = smallFont.render(text, True, color)
    elif size == "medium":
        textSurface = medFont.render(text, True, color)
    elif size == "large":
        textSurface = largeFont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg, color, y_displace=0, size="small"):
    """
    Creates the message that is displayed on the screen to users. 
    Will be centered and msg, color, size can be changed
    """
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = ((width/2),(height/2)+y_displace)
    screen.blit(textSurf,textRect)

def pipe_collisions_top(bird,pipes):
    """Takes in top pipes and the bird and returns true if there is a collision"""
    #---------Notes:--------
    #Screen is (600, 500)
    #Upper right is (600,0)
    #Lower left is (0,500)
    #Lower right is (600 ,500)
    
    if bird.y < (504 + pipes.y) and (bird.x+30 > pipes.x and bird.x-30 < pipes.x):
        return True
    return bird.colliderect(pipes)
	
    
def pipe_collisions_bot(bird,pipes):
    """Takes in bottom pipes and the bird and returns true if there is a collision"""
    if bird.y > (146 + pipes.y) and (bird.x+30 > pipes.x and bird.x-30 < pipes.x):
        return True
    return bird.colliderect(pipes)
    
def gameLoop():
    """
    Runs the game loop until users lose by allowing the jayhawk to collide with the pipes.
    When game over the game will show the game over screen and give the users the option to play again.
    """
    gameOver = False
    gameExit = False
    isGoingUp = False
    
    images = load_images();

    #Scrolling background declaration
    back = Background(images['background'], images['background'].get_size(), height)

    #Array declaration for moving pipes
    pipe = Pipe(images['pipe'], width)
    pipeList = []
    pipeList.append(pipe)
    #add pipes every 2 seconds
    delayBeforeNextPipe = 286 #(1000 / pygame.time.delay(n)) * 2
    delayBeforeNextPipeIncr = 0;
    
    #Definition of the jayhawk object and its corresponding rect
    jayhawk = images['jayhawk']
    jayhawk = pygame.transform.scale(jayhawk, (60, 60))
    jayrect = jayhawk.get_rect()
    jayrect = jayrect.move(80, 200)

    #Jayhawk speeds going up and down
    up_speed = -22;
    down_speed = 2;
    
    """
    Counters for up and down movement
    These counters allow for the changing of speed according to length of movement of the Jayhawk
    Generates effect of acceleration
    """
    up_counter = 0;
    down_counter = 0;
    
    #Random pipe declaration for testing
    pip = images['pipe']
    pip = pygame.transform.scale(pip, (50, 100))
    piprect = pip.get_rect()
    piprect = piprect.move(5,0)

    #Rect declaration of screen
    screenrect = screen.get_rect()
    
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                pygame.quit()
                quit()
                sys.exit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:   
                    # listens for ESCAPE key to close the game
                    gameExit = True
                    pygame.quit()
                    sys.exit
                if event.key == pygame.K_UP: 
                    # listens for UP ARROW key. Triggers isGoingUp to be True
                    isGoingUp = True
                    
        """
        The following IF statement controls the entire movement of the Jayhawk while it's going up.
        The counter is used to control speed, giving the user a feeling of acceleration.
        """
        if(isGoingUp):
            jayrect = jayrect.move(0, (up_speed/2))
            up_counter += 1
            down_counter = 0        
            if(up_counter == 1):
                up_speed = -16
            elif(up_counter == 2):
                up_speed = -12
            elif(up_counter == 3):
                up_speed = -10    
            elif(up_counter == 4):
                up_speed = -6           
            elif(up_counter == 5):
                up_speed = -4         
            elif(up_counter == 6):
                up_speed = -2           
            elif(up_counter > 6):
                isGoingUp = False
                up_counter = 0
                up_speed = -22 
                """
        The following IF statement controls the entire movement of the Jayhawk while it's going down.
        The counter is used to control speed, giving the user a feeling of acceleration.
        """
        else:
            jayrect = jayrect.move(0, (down_speed)/8)            
            down_counter += 1
            up_counter = 0            
            if(down_counter == 1):
                down_speed = 4            
            elif(down_counter == 2):
                down_speed = 6            
            elif(down_counter == 3):
                down_speed = 10            
            elif(down_counter == 4):
                down_speed = 12            
            elif(down_counter == 5):
                down_speed = 16            
            elif(down_counter > 5):
                down_speed = 22
                
        #Keeps the Jayhawk in screen for testing
        jayrect.clamp_ip(screenrect)
        

        screen.fill((255, 231, 181))

        #Draw background
        screen.blit(back.image, back.rect)
        screen.blit(back.image, back.rect2)
        screen.blit(back.image, back.rect3)
        
        #Make background scroll
        back.scroll()
        
    
        #Generates new pipes by appending them to the end of Pipe array
        delayBeforeNextPipeIncr = delayBeforeNextPipeIncr + 1
        if(delayBeforeNextPipeIncr > delayBeforeNextPipe):
            pipe1 = Pipe(images['pipe'], width)
            pipeList.append(pipe1)
            delayBeforeNextPipeIncr = 0
        #Draw pipe
        for pipeElement in pipeList:
            screen.blit(pipeElement.image_top, pipeElement.rect_top)
            screen.blit(pipeElement.image_bot, pipeElement.rect_bot)
            #make pipe scroll
            if(pipeElement.scroll() == False):
                pipeList.pop(0)
                
        #Draw Jayhawk
        screen.blit(jayhawk, jayrect)

        #Implements collisions
        for pipeElement in pipeList:
            botPipeRect = pipeElement.rect_bot
            topPipeRect = pipeElement.rect_top
            if (pipe_collisions_top(jayrect,topPipeRect)):
                gameOver = True
            if (pipe_collisions_bot(jayrect,botPipeRect)):
                gameOver = True

            
        while gameOver == True:
            #Draw background
            screen.blit(back.image, back.rect)
            screen.blit(back.image, back.rect2)
            screen.blit(back.image, back.rect3)
            #Make background scroll
            back.scroll()
            message_to_screen("Game Over",
                            blue,
                            -50,
                            "large")
            message_to_screen("Press c to play again",
                            blue,
                            50,
                            "small")
            pygame.display.update()
            pygame.time.delay(7)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        gameLoop()
                    if event.key == pygame.K_ESCAPE:
                        gameExit = True
                        pygame.quit()
                        sys.exit
        
        #Updates screen and implements delay
        pygame.display.update()
        pygame.display.flip()
        pygame.time.delay(7)

def main():
    """
    The application's entry point. Calls "start_menu" and "gameLoop" functions
    """
    gameExit = False
    start_menu()
    gameLoop()
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
    pygame.quit()
    quit()
    sys.exit
    
    
"""
Starts application by calling main function
"""
if __name__ == '__main__':
    main()
