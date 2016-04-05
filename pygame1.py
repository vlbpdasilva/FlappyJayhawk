
########
# MOVE JAYHAWK WITH ARROWS, PRESS SPACEBAR TO QUIT
# https://www.youtube.com/playlist?list=PL6gx4Cwl9DGAjkwJocj7vlc_mFU-4wXJq
#pipe image from http://vignette3.wikia.nocookie.net/fantendo/images/0/06/RocketPipes.png/revision/latest?cb=20100430132034

import sys, pygame, time, os

pygame.init()

size = width, height = (600, 500)
black = (0,0,0)
white = (255,255,255)
blue = (0, 0, 255)
red = (255, 0, 0)


screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
FPS = 15

smallFont = pygame.font.SysFont("comicsansms", 25)
medFont = pygame.font.SysFont("comicsansms", 50)
largeFont = pygame.font.SysFont("comicsansms", 100)

def load_images():
    """Load all images required by the game and return a dict of them.

    The returned dict has the following keys:
    background: The game's background image.
    bird-wingup: An image of the bird with its wing pointing upward.
        Use this and bird-wingdown to create a flapping bird.
    bird-wingdown: An image of the bird with its wing pointing downward.
        Use this and bird-wingup to create a flapping bird.
    pipe-end: An image of a pipe's end piece (the slightly wider bit).
        Use this and pipe-body to make pipes.
    pipe-body: An image of a slice of a pipe's body.  Use this and
        pipe-body to make pipes.
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
    intro = True
    x = 0
    bgdelay = 0
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False

        images = load_images();

        #scrolling background declaration
        back = images['background']
        back2 = images['background']
        back3 = images['background']
        bgWidth, bgHeight = back.get_size()

        screen.fill((255, 231, 181))

        #draw background
        screen.blit(back, (x,height - bgHeight))
        screen.blit(back2,(x + bgWidth,height - bgHeight))
        screen.blit(back3,(x + bgWidth + bgWidth,height - bgHeight))
        #make background scroll
        bgdelay = bgdelay + 1
        if(bgdelay % 2 == 1):
            x = x - 1
            if x == 0 - bgWidth:
                x = 0

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
        


def text_objects(text, color, size):
    if size == "small":
        textSurface = smallFont.render(text, True, color)
    elif size == "medium":
        textSurface = medFont.render(text, True, color)
    elif size == "large":
        textSurface = largeFont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg, color, y_displace=0, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = ((width/2),(height/2)+y_displace)
    screen.blit(textSurf,textRect)

def pipe_collisions(bird,pipes):
	return bird.colliderect(pipes)

def gameLoop():
    gameOver = False
    gameExit = False
    showGameOver = False
    x = 0
    bgdelay = 0
    images = load_images();

    #scrolling background declaration
    back = images['background']
    back2 = images['background']
    back3 = images['background']
    bgWidth, bgHeight = back.get_size()
    

    jayhawk = images['jayhawk']
    jayhawk = pygame.transform.scale(jayhawk, (50, 50))
    jayrect = jayhawk.get_rect()

    #random pipe declaration
    pip = images['pipe']
    pip = pygame.transform.scale(pip, (50, 100))
    piprect = pip.get_rect()
    piprect = piprect.move(65,0)

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    jayrect = jayrect.move(-20,0)
                if event.key == pygame.K_RIGHT:
                    jayrect = jayrect.move(20,0)
                if event.key == pygame.K_UP:
                    jayrect = jayrect.move(0, -20)
                if event.key == pygame.K_DOWN:
                    jayrect = jayrect.move(0, 20)
                    
        #pipe
        if (pipe_collisions(jayrect,piprect)):
            showGameOver = True

        screen.fill((255, 231, 181))

        #draw background
        screen.blit(back, (x,height - bgHeight))
        screen.blit(back2,(x + bgWidth,height - bgHeight))
        screen.blit(back3,(x + bgWidth + bgWidth,height - bgHeight))
        #make background scroll
        bgdelay = bgdelay + 1
        if(bgdelay % 2 == 1):
            x = x - 1
            if x == 0 - bgWidth:
                x = 0
		#draw pipe
        screen.blit(pip, piprect)        
		#draw jayhawk
        screen.blit(jayhawk, jayrect)
        if showGameOver:
            youlost = largeFont.render("Game Over!",1,black)
            screen.blit(youlost,(100,100))
        pygame.display.update()
    

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
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_C:
                    gameLoop()
    pygame.quit()
    sys.exit


if __name__ == '__main__':
    # If this module had been imported, __name__ would be 'pygame1'.
    # It was executed (e.g. by double-clicking the file), so call main.
    main()

