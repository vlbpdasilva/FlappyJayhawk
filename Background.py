import pygame
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
        """
        return pygame.Rect(self.x, self.y, 25, 25)

    @property
    def rect2(self):
        """Get the background's 2nd position, width, and height, as a pygame.Rect.
        This will be the same image repeated at BackgroundWidth pixels after.
        """
        return pygame.Rect(self.x + self.BackgroundWidth, self.y, 25, 25)

    @property
    def rect3(self):
        """Get the background's 3rd position, width, and height, as a pygame.Rect.
        This will be the same image repeated at BackgroundWidth + BackgroundWidth pixels after.
            THE WIDTH AND HEIGHT PARAMETERS DON'T WORK?"""
        return pygame.Rect(self.x + self.BackgroundWidth + self.BackgroundWidth, self.y, 25, 25)
