import sys, pygame

pygame.init()

screen = pygame.display.set_mode([600, 500])
pygame.display.set_caption("Flappy Jayhawk")

isGoingUp = False;

jayhawk = pygame.image.load("jayhawk.png")
jayhawk = pygame.transform.scale(jayhawk, (50, 50))
jayrect = jayhawk.get_rect()
jayrect = jayrect.move(80, 200);

up_speed = -22;
down_speed = 2;
up_counter = 0;
down_counter = 0;


while 1:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:   # listens for ESC key being pressed
                pygame.quit()                  # closes program 
                sys.exit()                     # closes window
            if event.key == pygame.K_SPACE:
                isGoingUp = True;                    

    if(isGoingUp):
        jayrect = jayrect.move(0, (up_speed * 2))
        print(up_counter , up_speed)
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
        jayrect = jayrect.move(0, down_speed)
        print(down_counter, down_speed)
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
    
        

                
    screen.fill((0,0,0))
    screen.blit(jayhawk, jayrect)
    pygame.display.update()
    pygame.display.flip()
    pygame.time.delay(60)
