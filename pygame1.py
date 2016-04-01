
########
# MOVE JAYHAWK WITH ARROWS, PRESS SPACEBAR TO QUIT
# https://www.youtube.com/playlist?list=PL6gx4Cwl9DGAjkwJocj7vlc_mFU-4wXJq

import sys, pygame, time

pygame.init()

size = width, height = (600, 500)
black = (0,0,0)
white = (255,255,255)

screen = pygame.display.set_mode(size)
gameExit = False;
clock = pygame.time.Clock()
FPS = 15

smallFont = pygame.font.SysFont("comicsansms", 25)
medFont = pygame.font.SysFont("comicsansms", 50)
largeFont = pygame.font.SysFont("comicsansms", 100)

def start_menu():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit

        screen.fill(white)
        message_to_screen("Flappy JayHawks",
                            black,
                            -100,
                            "large")
        message_to_screen("By: Jeromy Tsai, Cammy Vo, Jesse Yang, Victor Berger",
                            black,
                            -20,
                            "small")

        pygame.display.update()
        clock.tick(15)


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

def gameLoop():
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
        screen.fill(white)
        pygame.display.update()

        clock.tick(FPS)

    pygame.quit()
    sys.exit

start_menu()