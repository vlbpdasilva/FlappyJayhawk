########
# MOVE JAYHAWK WITH ARROWS, PRESS SPACEBAR TO QUIT

#pipe image from http://vignette3.wikia.nocookie.net/fantendo/images/0/06/RocketPipes.png/revision/latest?cb=20100430132034

import sys, pygame, os
from random import randint

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
        This will decide whether to return an image where the bird's
        visible wing is pointing upward or where it is pointing downward
        based on pygame.time.get_ticks().  This will animate the flapping
        bird, even though pygame doesn't support animated GIFs.
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
        """Initialise a new Jayhawk instance.
        Arguments:
        x: The Jayhawk's initial X coordinate.
        y: The Jayhawk's initial Y coordinate.
        scale: The Jayhawk's size multiplier.
        """
        super(Pipe, self).__init__()
        self.x = game_window_width
        self.reset_x = game_window_width
        self.y = randint(25, 375)

        self.Pipe_image_top = image
        self.Pipe_image_top = pygame.transform.rotate(self.Pipe_image_top, 180)
        self.Pipe_mask_top = pygame.mask.from_surface(self.Pipe_image_top)
        
        self.Pipe_image_bot = image
        self.Pipe_mask_bot = pygame.mask.from_surface(self.Pipe_image_bot)

    def scroll(self):
        self.x = self.x - 1
        if(self.x + 600 == 0):
            self.x = self.reset_x
            self.y = randint(25, 375)
            return False
        return True
    
    @property
    def image_top(self):
        """Get a Surface containing this bird's image.
        This will decide whether to return an image where the bird's
        visible wing is pointing upward or where it is pointing downward
        based on pygame.time.get_ticks().  This will animate the flapping
        bird, even though pygame doesn't support animated GIFs.
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
        """Get the bird's position, width, and height, as a pygame.Rect.
            THE WIDTH AND HEIGHT PARAMETERS DON'T WORK?"""
        return pygame.Rect(self.x, self.y - 504, 25, 25)#pipe's img height is 504

    @property
    def image_bot(self):
        """Get a Surface containing this bird's image.
        This will decide whether to return an image where the bird's
        visible wing is pointing upward or where it is pointing downward
        based on pygame.time.get_ticks().  This will animate the flapping
        bird, even though pygame doesn't support animated GIFs.
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
        """Get the bird's position, width, and height, as a pygame.Rect.
            THE WIDTH AND HEIGHT PARAMETERS DON'T WORK?"""
        return pygame.Rect(self.x, self.y + 100, 25, 25)
        
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

def main():
    """The application's entry point.
    If someone executes this module (instead of importing it, for
    example), this function is called.
    """
    
    pygame.init()

    size = width, height = 600, 500
    black = 0,0,0

    screen = pygame.display.set_mode(size)

    images = load_images();

    #scrolling background declaration
    back = images['background']
    back2 = images['background']
    back3 = images['background']
    bgWidth, bgHeight = back.get_size()
    x = 0
    bgdelay = 0

    #scrolling pipe declaration
    pipe = Pipe(images['pipe'], width)    #piperect = pipe.rect #this is updated by calling scroll and then calling pipe's rect property
    pipeList = []
    pipeList.append(pipe)
    #add pipes every 2 seconds
    delayBeforeNextPipe = 286 #(1000 / pygame.time.delay(n)) * 2
    delayBeforeNextPipeIncr = 0;

    jayhawk = Jayhawk(0,0,(50,50), images['jayhawk'])
    jayrect = jayhawk.rect

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:   # listens for pressing spacebar
                    pygame.quit()       # closes program and window
                    sys.exit()
                if event.key == pygame.K_LEFT:
                    jayrect = jayrect.move(-20,0)
                elif event.key == pygame.K_RIGHT:
                    jayrect = jayrect.move(20,0)
                elif event.key == pygame.K_UP:
                    jayrect = jayrect.move(0, -20)
                elif event.key == pygame.K_DOWN:
                    jayrect = jayrect.move(0, 20)
                    
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
        
        screen.blit(jayhawk.image, jayrect)
        pygame.display.update()
        pygame.display.flip()
        pygame.time.delay(7)


if __name__ == '__main__':
    # If this module had been imported, __name__ would be 'pygame1'.
    # It was executed (e.g. by double-clicking the file), so call main.
    main()
