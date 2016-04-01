import sys, pygame

pygame.init()

size = width, height = 600, 500
black = 0,0,0

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Flappy Jayhawk")

isGoingUp = False;
movementCounter = 0;

jayhawk = pygame.image.load("jayhawk.png")
jayhawk = pygame.transform.scale(jayhawk, (50, 50))
jayrect = jayhawk.get_rect()
jayrect = jayrect.move(80, 200);

while 1:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:   # listens for ESC key being pressed
                pygame.quit()       # closes program 
                sys.exit()          # closes window
            if event.key == pygame.K_SPACE:
                isGoingUp = True;                    
                
    if(not(isGoingUp)):                     # bird moves down
       jayrect = jayrect.move(0, 20)

    if(isGoingUp):
        jayrect = jayrect.move(0, -20)
        movementCounter = movementCounter + 1
        if(movementCounter > 7):
            isGoingUp = False;
            movementCounter = 0;

                
    screen.fill(black)
    screen.blit(jayhawk, jayrect)
    pygame.display.update()
    pygame.display.flip()
    pygame.time.delay(60)
