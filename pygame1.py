
########
# MOVE JAYHAWK WITH ARROWS, PRESS SPACEBAR TO QUIT

import sys, pygame

pygame.init()

size = width, height = 600, 500
black = 0,0,0

screen = pygame.display.set_mode(size)

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
                
    screen.fill(black)
    screen.blit(jayhawk, jayrect)
    pygame.display.update()
    pygame.display.flip()
    pygame.time.delay(100)
