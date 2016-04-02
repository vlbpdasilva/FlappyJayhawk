
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
        self.scale = pygame.transform.scale(self.Jayhawk_image, scale)
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
        """Get the bird's position, width, and height, as a pygame.Rect."""
        return Jayhawk_rect(self.x, self.y, 50, 50)
    
        
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

    jayhawk = Jayhawk(0,0,(50,50), images['jayhawk'])
    #jayhawk = pygame.transform.scale(jayhawk, (50, 50))
    jayrect = images['jayhawk'].get_rect()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:   # listens for pressing spacebar
                    pygame.quit()       # closes program and window
                    sys.exit()
                if event.key == pygame.K_LEFT:
                    jayrect = jayrect.move(-20,0)
                if event.key == pygame.K_RIGHT:
                    jayrect = jayrect.move(20,0)
                if event.key == pygame.K_UP:
                    jayrect = jayrect.move(0, -20)
                if event.key == pygame.K_DOWN:
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
        
        screen.blit(jayhawk.image, jayrect)
        pygame.display.update()
        pygame.display.flip()
        pygame.time.delay(7)


if __name__ == '__main__':
    # If this module had been imported, __name__ would be 'pygame1'.
    # It was executed (e.g. by double-clicking the file), so call main.
    main()
