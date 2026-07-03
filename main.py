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
        self.velocity = 0
        self.clicked = False
        self.flying = False
    
    def update(self, is_game_over):
        # Gravity
        if self.flying == True:
            self.velocity += 0.5

            if self.velocity > 8:
                self.velocity = 8

            if self.rect.bottom < 768:
                self.rect.y += int(self.velocity)

        if is_game_over == False:
            # Jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.velocity = -10

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            # Animation
            self.counter += 1

            flappy_cooldown = 5

            if self.counter > flappy_cooldown:
                self.counter = 0
                self.index += 1
                
                if self.index >= len(self.images):
                    self.index = 0
            
            self.image = self.images[self.index]
            
            # Rotation
            self.image = pygame.transform.rotate(self.images[self.index], self.velocity * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

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
    
    is_game_over = False

    run = True

    while run:
        CLOCK.tick(FPS)

        screen.blit(background_image, (0, 0))

        bird_group.draw(screen)
        bird_group.update(is_game_over)

        screen.blit(ground_image, (ground_scroll, 768))

        if flappy.rect.bottom > 768:
            is_game_over = True

            flappy.flying = False

        if is_game_over == False:
            ground_scroll -= ground_speed

            if abs(ground_scroll) > 35:
                ground_scroll = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and flappy.flying == False and is_game_over == False:
                flappy.flying = True

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
