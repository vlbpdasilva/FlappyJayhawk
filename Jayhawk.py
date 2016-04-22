import pygame
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

    #is the Jayhawk moving up (jumping)?
    isGoingUp = False
    #Jayhawk speeds going up and down
    up_speed = -22
    down_speed = 2
    """
    Counters for up and down movement
    These counters allow for the changing of speed according to length of movement of the Jayhawk
    Generates effect of acceleration
    """
    up_counter = 0
    down_counter = 0
    
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

    def updatePosition(self):
        """Update the position of the Jayhawk by calculating all necessary
        position movements affected by gravity function and player-inputted jumps.
        """
        
        """
        The following IF statement controls the entire movement of the Jayhawk while it's going up.
        The counter is used to control speed, giving the user a feeling of acceleration.
        
        The following ELSE statement controls the entire movement of the Jayhawk while it's going Jayhawk.down.
        The counter is used to control speed, giving the user a feeling of acceleration.
        """
        if(Jayhawk.isGoingUp):
            self.y = self.y + Jayhawk.up_speed/2
            Jayhawk.up_counter += 1
            Jayhawk.down_counter = 0        
            if(Jayhawk.up_counter == 1):
                Jayhawk.up_speed = -16
            elif(Jayhawk.up_counter == 2):
                Jayhawk.up_speed = -12
            elif(Jayhawk.up_counter == 3):
                Jayhawk.up_speed = -10    
            elif(Jayhawk.up_counter == 4):
                Jayhawk.up_speed = -6           
            elif(Jayhawk.up_counter == 5):
                Jayhawk.up_speed = -4         
            elif(Jayhawk.up_counter == 6):
                Jayhawk.up_speed = -2           
            elif(Jayhawk.up_counter > 6):
                Jayhawk.isGoingUp = False
                Jayhawk.up_counter = 0
                Jayhawk.up_speed = -22 
        else:
            self.y = self.y + Jayhawk.down_speed/8            
            Jayhawk.down_counter += 1
            Jayhawk.up_counter = 0            
            if(Jayhawk.down_counter == 1):
                Jayhawk.down_speed = 4            
            elif(Jayhawk.down_counter == 2):
                Jayhawk.down_speed = 6            
            elif(Jayhawk.down_counter == 3):
                Jayhawk.down_speed = 10            
            elif(Jayhawk.down_counter == 4):
                Jayhawk.down_speed = 12            
            elif(Jayhawk.down_counter == 5):
                Jayhawk.down_speed = 16            
            elif(Jayhawk.down_counter > 5):
                Jayhawk.down_speed = 22

    def jump(self):
        """ The Jayhawk jumps up thus moving up.
        listens for UP ARROW key.
        Triggers isGoingUp to be True, sets up_counter to 0 to begin initial jump speed (up_speed to -16).
        """
        Jayhawk.isGoingUp = True
        Jayhawk.up_counter = 0

    def clamp(self):
        """ Clamp the Jayhawk to stay within the screen's boundaries.
        This is done rather than calling clamp_ip() because returning the Jayhawk class's rect does not
        seem to qualify as a proper get_rect() that clamp_ip() looks for.
        """
        if(self.y < 0):
            self.y = 0
        elif(self.y > 450):
            self.y = 450
    
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
