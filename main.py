import pygame

SCREEN_WIDTH = 864
SCREEN_HEIGHT = 936
CLOCK = pygame.time.Clock()
FPS = 60

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        self.images = []
        self.index = 0
        self.counter = 0
        
        for number in range(1, 4):
            image = pygame.image.load(f"assets/sprites/bird{number}.png")

            self.images.append(image)

        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
    
    def update(self):
        self.counter += 1

        flappy_cooldown = 5

        if self.counter > flappy_cooldown:
            self.counter = 0
            self.index += 1
            
            if self.index >= len(self.images):
                self.index = 0
        
        self.image = self.images[self.index]

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird")

    background_image = pygame.image.load("assets/sprites/bg.png")
    ground_image = pygame.image.load("assets/sprites/ground.png")

    bird_group = pygame.sprite.Group()

    flappy = Bird(100, int(SCREEN_HEIGHT / 2))

    bird_group.add(flappy)

    ground_scroll = 0
    ground_speed = 4

    run = True

    while run:
        CLOCK.tick(FPS)

        screen.blit(background_image, (0, 0))

        bird_group.draw(screen)
        bird_group.update()

        screen.blit(ground_image, (ground_scroll, 768))

        ground_scroll -= ground_speed

        if abs(ground_scroll) > 35:
            ground_scroll = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
