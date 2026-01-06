import sprites

import pygame
pygame.init()

screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()

button = sprites.Button_UI("Click Me", 150, 60, (70, 130, 180))

def say_hi():
    print("Hello!")

running = True
while running:
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))
    button.draw(screen, 125, 120)
    button.on_click(events, say_hi)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
