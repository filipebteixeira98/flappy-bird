import pygame

SCREEN_WIDTH = 864
SCREEN_HEIGHT = 936
CLOCK = pygame.time.Clock()
FPS = 60


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    
    background_image = pygame.image.load('assets/sprites/bg.png')
    ground_image = pygame.image.load('assets/sprites/ground.png')

    ground_scroll = 0
    ground_speed = 4

    run = True

    while run:
        CLOCK.tick(FPS)
        
        screen.blit(background_image, (0, 0))
        screen.blit(ground_image, (ground_scroll, 768))

        ground_scroll -= ground_speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
