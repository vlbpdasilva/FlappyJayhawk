
########
# MOVE JAYHAWK WITH ARROWS, PRESS SPACEBAR TO QUIT

#pipe image from http://vignette3.wikia.nocookie.net/fantendo/images/0/06/RocketPipes.png/revision/latest?cb=20100430132034

import sys, pygame
from random import randint


def main():
    """The application's entry point.

    If someone executes this module (instead of importing it, for
    example), this function is called.
    """
    
    pygame.init()

    size = width, height = 600, 500
    black = 0,0,0

    screen = pygame.display.set_mode(size)

    #scrolling background declaration
    bg = "repeatTest_smw.png"
    back = pygame.image.load(bg).convert()
    back2 = pygame.image.load(bg).convert()
    back3 = pygame.image.load(bg).convert()
    bgWidth, bgHeight = back.get_size()
    x = 0
    bgdelay = 0

    jayhawk = pygame.image.load("jayhawk.png")
    jayhawk = pygame.transform.scale(jayhawk, (50, 50))
    jayrect = jayhawk.get_rect()

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
        
        screen.blit(jayhawk, jayrect)
        pygame.display.update()
        pygame.display.flip()
        pygame.time.delay(7)


if __name__ == '__main__':
    # If this module had been imported, __name__ would be 'pygame1'.
    # It was executed (e.g. by double-clicking the file), so call main.
    main()
