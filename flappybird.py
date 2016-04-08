
########
# MOVE JAYHAWK WITH ARROWS, PRESS SPACEBAR TO QUIT
# https://www.youtube.com/playlist?list=PL6gx4Cwl9DGAjkwJocj7vlc_mFU-4wXJq
#pipe image from http://vignette3.wikia.nocookie.net/fantendo/images/0/06/RocketPipes.png/revision/latest?cb=20100430132034

import sys, pygame, time, os
from random import randint

pygame.init()

pygame.display.set_caption("Flappy Jayhawk")
size = width, height = (600, 500)
screen = pygame.display.set_mode(size)

black = (0,0,0)
white = (255,255,255)
blue = (0, 0, 255)
red = (255, 0, 0)

clock = pygame.time.Clock()
FPS = 15

smallFont = pygame.font.SysFont("comicsansms", 25)
medFont = pygame.font.SysFont("comicsansms", 50)
largeFont = pygame.font.SysFont("comicsansms", 100)

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
    #scrolling background declaration
    back = Background(images['background'], images['background'].get_size(), height)
    
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False

        screen.fill((255, 231, 181))

        #draw background
        screen.blit(back.image, back.rect)
        screen.blit(back.image, back.rect2)
        screen.blit(back.image, back.rect3)
        #make background scroll
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
        
def game_over():
    """
    Creates the game over screen that users will see when they jayhawk touches a pipe and dies.
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

    
class Jayhawk(pygame.sprite.Sprite):
    """The Jayhawk that the player will be controlling.
    The Jayhawk will ascend or descend and its main objective is to avoid
    colliding with pipes. Ascending will occur when the player hits up/space.
    Descending will occur when the player is not causing the Jayhawk to
    ascend. Colliding with pipes will cause the Jayhawk to lose health.
    At 0 health, the player loses the game.
    Attributes: (NOTE: THIS WILL BE CHANGED. these are not the actual attributes or constants,
                        they are only here as an example of documentation for now)
    x: The bird's X coordinate.
    y: The bird's Y coordinate.
    msec_to_climb: The number of milliseconds left to climb, where a
        complete climb lasts Bird.CLIMB_DURATION milliseconds.
    Constants:
    WIDTH: The width, in pixels, of the bird's image.
    HEIGHT: The height, in pixels, of the bird's image.
    SINK_SPEED: With which speed, in pixels per millisecond, the bird
        descends in one second while not climbing.
    CLIMB_SPEED: With which speed, in pixels per millisecond, the bird
        ascends in one second while climbing, on average.  See also the
        Bird.update docstring.
    CLIMB_DURATION: The number of milliseconds it takes the bird to
        execute a complete climb.
    """
    
    def __init__(self, x, y, scale, image):
        """Initialise a new Jayhawk instance.
        Arguments:
        x: The Jayhawk's initial X coordinate.
        y: The Jayhawk's initial Y coordinate.
        scale: The Jayhawk's size multiplier.
        image: The Jayhawk's image.
        """
        super(Jayhawk, self).__init__()
        self.x = x
        self.y = y
        self.Jayhawk_image = image
        self.Jayhawk_image = pygame.transform.scale(self.Jayhawk_image, scale)
        self.Jayhawk_mask = pygame.mask.from_surface(self.Jayhawk_image)

    @property
    def image(self):
        """Get a Surface containing this bird's image.
        """
        return self.Jayhawk_image

    @property
    def mask(self):
        """Get a bitmask for use in collision detection.
        The bitmask excludes all pixels in self.image with a
        transparency greater than 127."""
        return self.Jayhawk_mask

    @property
    def rect(self):
        """Get the bird's position, width, and height, as a pygame.Rect.
            THE WIDTH AND HEIGHT PARAMETERS DON'T WORK?"""
        return pygame.Rect(self.x, self.y, 25, 25)
    
class Pipe(pygame.sprite.Sprite):
    """
    x: The bird's X coordinate.
    y: The bird's Y coordinate.
    msec_to_climb: The number of milliseconds left to climb, where a
        complete climb lasts Bird.CLIMB_DURATION milliseconds.
    Constants:
    WIDTH: The width, in pixels, of the bird's image.
    HEIGHT: The height, in pixels, of the bird's image.
    SINK_SPEED: With which speed, in pixels per millisecond, the bird
        descends in one second while not climbing.
    CLIMB_SPEED: With which speed, in pixels per millisecond, the bird
        ascends in one second while climbing, on average.  See also the
        Bird.update docstring.
    CLIMB_DURATION: The number of milliseconds it takes the bird to
        execute a complete climb.
    """
    
    
    def __init__(self, image, game_window_width):
        """Initialise a new Pipe instance.
        Arguments:
        image: The Pipe's image. This will be duplicated for both top and
                bottom pipes for the pipe pair.
        game_window_width: The position at which new pipes spawn.
        """
        super(Pipe, self).__init__()
        self.x = game_window_width
        self.reset_x = game_window_width
        self.y = randint(25, 275)

        self.Pipe_image_top = image
        self.Pipe_image_top = pygame.transform.rotate(self.Pipe_image_top, 180)
        self.Pipe_mask_top = pygame.mask.from_surface(self.Pipe_image_top)
        
        self.Pipe_image_bot = image
        self.Pipe_mask_bot = pygame.mask.from_surface(self.Pipe_image_bot)
        
        #self.Pipe_rect_top = pygame.Rect(self.x, self.y - 504, 25, 25)
        #self.Pipe_rect_bot = pygame.Rect(self.x, self.y + 100, 25, 25)


    def scroll(self):
        """Update the Pipe's position by changing its x-coord by -1.
        Get whether the pipe has hit the boundary -600 and stopped scrolling (and reset).
        When stopped scrolling, this should be the signal to pop the pipe off the pipeList.
        """
        self.x = self.x - 1
        if(self.x + 600 == 0):
            self.x = self.reset_x
            self.y = randint(25, 375)
            return False
        return True
    
    @property
    def image_top(self):
        """Get a Surface containing the top pipe's image.
        """
        return self.Pipe_image_top

    @property
    def mask_top(self):
        """Get a bitmask for use in collision detection.
        The bitmask excludes all pixels in self.image with a
        transparency greater than 127."""
        return self.Pipe_mask_top

    @property
    def rect_top(self):
        """Get the top pipe's position, width, and height, as a pygame.Rect.
            THE WIDTH AND HEIGHT PARAMETERS DON'T WORK?"""
        return pygame.Rect(self.x, self.y - 504, 25, 25)#pipe's img height is 504

    @property
    def image_bot(self):
        """Get a Surface containing the bot pipe's image.
        """
        return self.Pipe_image_bot

    @property
    def mask_bot(self):
        """Get a bitmask for use in collision detection.
        The bitmask excludes all pixels in self.image with a
        transparency greater than 127."""
        return self.Pipe_mask_bot

    @property
    def rect_bot(self):
        """Get the bot pipe's position, width, and height, as a pygame.Rect.
            THE WIDTH AND HEIGHT PARAMETERS DON'T WORK?"""
        return pygame.Rect(self.x, self.y + 100, 25, 25)

class Background(pygame.sprite.Sprite):
    """The background image that will scroll at a relatively slow pace.
    The image will repeat every image width's length apart.
    """

    def __init__(self, image, size, windowHeight):
        """Initialise a new Background instance.
            Arguments:
            image: The Background image.
        size: the size of the background image.
        windowHeight: used to align the background with the bottom of the window.
        """
        super(Background, self).__init__()
        self.x = 0
        self.BackgroundDelay = 0
        self.Background_image = image
        self.BackgroundWidth, self.BackgroundHeight = size
        self.y = windowHeight - self.BackgroundHeight

    def scroll(self):
        """Update the Background's position by changing its x-coord by -1.
        Reset position of Background image's rects back to 0 when the first rect is fully offscreen.
        This gives the illusion of infinitely repeating background.
        """
        self.BackgroundDelay = self.BackgroundDelay + 1
        if(self.BackgroundDelay % 2 == 1):
            self.x = self.x - 1
            if self.x == 0 - self.BackgroundWidth:
                self.x = 0

    @property
    def image(self):
        """Get a Surface containing the Background's image.
        """
        return self.Background_image

    @property
    def rect(self):
        """Get the background's 1st position, width, and height, as a pygame.Rect.
            THE WIDTH AND HEIGHT PARAMETERS DON'T WORK?"""
        return pygame.Rect(self.x, self.y, 25, 25)

    @property
    def rect2(self):
        """Get the background's 2nd position, width, and height, as a pygame.Rect.
        This will be the same image repeated at BackgroundWidth pixels after.
            THE WIDTH AND HEIGHT PARAMETERS DON'T WORK?"""
        return pygame.Rect(self.x + self.BackgroundWidth, self.y, 25, 25)

    @property
    def rect3(self):
        """Get the background's 3rd position, width, and height, as a pygame.Rect.
        This will be the same image repeated at BackgroundWidth + BackgroundWidth pixels after.
            THE WIDTH AND HEIGHT PARAMETERS DON'T WORK?"""
        return pygame.Rect(self.x + self.BackgroundWidth + self.BackgroundWidth, self.y, 25, 25)

def pipe_collisions_top(bird,pipes):
    #notes
    #Screen is (600, 500)
    #Upper right is (600,0)
    #Lower left is (0,500)
    #Lower right is (600 ,500)
    
    if bird.y < (404 + pipes.y) and (bird.x+30 > pipes.x and bird.x-30 < pipes.x):
        return True
    
    return bird.colliderect(pipes)
	
    
def pipe_collisions_bot(bird,pipes):
 
    #if bird.y > (96 + pipes.y) and (bird.x+45 > pipes.x and bird.x-35 < pipes.x):
    if bird.y > (96 + pipes.y) and (bird.x+30 > pipes.x and bird.x-30 < pipes.x):
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

    #scrolling background declaration
    back = Background(images['background'], images['background'].get_size(), height)

    #scrolling pipe declaration
    pipe = Pipe(images['pipe'], width)    #piperect = pipe.rect #this is updated by calling scroll and then calling pipe's rect property
    pipeList = []
    pipeList.append(pipe)
    #add pipes every 2 seconds
    delayBeforeNextPipe = 286 #(1000 / pygame.time.delay(n)) * 2
    delayBeforeNextPipeIncr = 0;
    
    #jayhawk
    jayhawk = images['jayhawk']
    jayhawk = pygame.transform.scale(jayhawk, (50, 50))
    jayrect = jayhawk.get_rect()
    jayrect = jayrect.move(80, 200)

    #jayhawk speeds
    up_speed = -22;
    down_speed = 2;
    up_counter = 0;
    down_counter = 0;
    
    #random pipe declaration for testing
    pip = images['pipe']
    pip = pygame.transform.scale(pip, (50, 100))
    piprect = pip.get_rect()
    piprect = piprect.move(5,0)

    #rect declaration of screen
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
                    gameExit = True
                    pygame.quit()
                    sys.exit
                if event.key == pygame.K_UP:
                    isGoingUp = True
                if event.key == pygame.K_LEFT:
                    jayrect = jayrect.move(-20,0)
                if event.key == pygame.K_RIGHT:
                    jayrect = jayrect.move(20,0)
                    
        if(isGoingUp):
            jayrect = jayrect.move(0, (up_speed / 3))
            #print(up_counter , up_speed)
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
        else:
            jayrect = jayrect.move(0, (down_speed)/3)
            #print(down_counter, down_speed)
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
                
        #keeps the jayhawk in screen
        jayrect.clamp_ip(screenrect)     

        screen.fill((255, 231, 181))

        #draw background
        screen.blit(back.image, back.rect)
        screen.blit(back.image, back.rect2)
        screen.blit(back.image, back.rect3)
        #make background scroll
        back.scroll()
    #draw pipe for testing
        #screen.blit(pip, piprect)        
    
        #add pipes every 2 seconds
        delayBeforeNextPipeIncr = delayBeforeNextPipeIncr + 1
        if(delayBeforeNextPipeIncr > delayBeforeNextPipe):
            pipe1 = Pipe(images['pipe'], width)
            pipeList.append(pipe1)
            delayBeforeNextPipeIncr = 0
        #draw pipe
        for pipeElement in pipeList:
            screen.blit(pipeElement.image_top, pipeElement.rect_top)
            screen.blit(pipeElement.image_bot, pipeElement.rect_bot)
            #make pipe scroll
            if(pipeElement.scroll() == False):
                pipeList.pop(0)
                
        #draw jayhawk
        screen.blit(jayhawk, jayrect)

        #collisions
        for pipeElement in pipeList:
            botPipeRect = pipeElement.rect_bot
            topPipeRect = pipeElement.rect_top
            if (pipe_collisions_top(jayrect,topPipeRect)):
                gameOver = True
            if (pipe_collisions_bot(jayrect,botPipeRect)):
                gameOver = True

            
        while gameOver == True:
            #draw background
            screen.blit(back.image, back.rect)
            screen.blit(back.image, back.rect2)
            screen.blit(back.image, back.rect3)
            #make background scroll
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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        gameLoop()
        

        pygame.display.update()
        pygame.display.flip()
        pygame.time.delay(7)

def main():
    """The application's entry point.

    If someone executes this module (instead of importing it, for
    example), this function is called.
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


if __name__ == '__main__':
    # If this module had been imported, __name__ would be 'pygame1'.
    # It was executed (e.g. by double-clicking the file), so call main.
    main()
