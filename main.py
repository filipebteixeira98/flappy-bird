import pygame
from pygame.locals import *
import random

SCREEN_WIDTH = 864
SCREEN_HEIGHT = 936
CLOCK = pygame.time.Clock()
FPS = 60


class Bird(pygame.sprite.Sprite):
    """Representa o pássaro controlado pelo jogador.

    A classe guarda os frames da animação de voo, a posição do pássaro
    e os estados usados pela física simples do jogo, como velocidade,
    clique atual e se o pássaro já começou a voar.
    """

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
        """Atualiza física, entrada do jogador e animação do pássaro.

        Quando o jogo está ativo, aplica gravidade, processa o clique
        para fazer o pássaro subir e alterna os sprites para simular
        o bater de asas. Quando o jogo acaba, apenas gira o pássaro
        para indicar queda.
        """

        # Gravidade: aumenta a velocidade vertical até um limite.
        if self.flying == True:
            self.velocity += 0.5

            if self.velocity > 8:
                self.velocity = 8

            if self.rect.bottom < 768:
                self.rect.y += int(self.velocity)

        if is_game_over == False:
            # Pulo: um clique aplica impulso para cima.
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.velocity = -10

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            # Animação: troca o frame do pássaro a cada poucos ciclos.
            self.counter += 1

            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1

                if self.index >= len(self.images):
                    self.index = 0

            self.image = self.images[self.index]

            # Rotação: inclina o pássaro conforme ele sobe ou cai.
            self.image = pygame.transform.rotate(
                self.images[self.index], self.velocity * -2
            )
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
    """Representa um cano superior ou inferior.

    O parâmetro ``position`` define se o cano fica em cima ou embaixo.
    Os canos se movem da direita para a esquerda e são removidos quando
    saem completamente da tela.
    """

    def __init__(self, x, y, position, pipe_gap):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("assets/sprites/pipe.png")
        self.rect = self.image.get_rect()

        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]

        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self, ground_speed):
        """Move o cano e remove o sprite quando ele sai da tela."""

        self.rect.x -= ground_speed

        if self.rect.right < 0:
            self.kill()


class Button:
    """Botão simples usado para reiniciar a partida após o fim do jogo."""

    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        """Desenha o botão e retorna ``True`` quando ele é clicado."""

        action = False

        mouse_position = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_position):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


def draw_text(text, font, text_color, x, y, screen):
    """Renderiza um texto na tela usando a fonte e a cor informadas."""

    image = font.render(text, True, text_color)

    screen.blit(image, (x, y))


def reset_game(pipe_group, flappy):
    """Reinicia os elementos principais e devolve a pontuação para zero."""

    pipe_group.empty()

    flappy.rect.x = 100
    flappy.rect.y = int(SCREEN_HEIGHT / 2)

    score = 0

    return score


def main():
    """Executa a configuração inicial e o loop principal do jogo.

    O loop principal controla desenho, eventos, colisões, pontuação,
    geração de canos, movimento do chão e reinício da partida.
    """

    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird")

    background_image = pygame.image.load("assets/sprites/bg.png")
    ground_image = pygame.image.load("assets/sprites/ground.png")
    button_image = pygame.image.load("assets/sprites/restart.png")

    pipe_gap = 150
    pipe_frequency = 1500
    last_pipe = pygame.time.get_ticks() - pipe_frequency

    font = pygame.font.SysFont("Bauhaus 93", 60)

    font_color = (255, 255, 255)

    bird_group = pygame.sprite.Group()
    pipe_group = pygame.sprite.Group()

    flappy = Bird(100, int(SCREEN_HEIGHT / 2))

    bird_group.add(flappy)

    ground_scroll = 0
    ground_speed = 4

    is_game_over = False

    score = 0
    pass_pipe = False

    run = True

    while run:
        CLOCK.tick(FPS)

        # Desenha o cenário e atualiza os sprites visíveis.
        screen.blit(background_image, (0, 0))

        bird_group.draw(screen)
        bird_group.update(is_game_over)

        pipe_group.draw(screen)

        button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 100, button_image)

        screen.blit(ground_image, (ground_scroll, 768))

        # Pontuação: conta um ponto quando o pássaro passa por um par de canos.
        if len(pipe_group) > 0:
            if (
                bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left
                and bird_group.sprites()[0].rect.right
                < pipe_group.sprites()[0].rect.right
                and pass_pipe == False
            ):
                pass_pipe = True

            if pass_pipe == True:
                if (
                    bird_group.sprites()[0].rect.left
                    > pipe_group.sprites()[0].rect.right
                ):
                    score += 1

                    pass_pipe = False

        draw_text(str(score), font, font_color, int(SCREEN_WIDTH / 2), 20, screen)

        # Colisões com canos, topo da tela ou chão encerram a partida.
        if (
            pygame.sprite.groupcollide(bird_group, pipe_group, False, False)
            or flappy.rect.top < 0
        ):
            is_game_over = True

        if flappy.rect.bottom >= 768:
            is_game_over = True

            flappy.flying = False

        # Enquanto o jogo está ativo, cria canos periodicamente e move o cenário.
        if is_game_over == False and flappy.flying == True:
            time_now = pygame.time.get_ticks()

            if time_now - last_pipe > pipe_frequency:
                pipe_height = random.randint(-100, 100)

                bottom_pipe = Pipe(
                    SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height, -1, pipe_gap
                )
                top_pipe = Pipe(
                    SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height, 1, pipe_gap
                )

                pipe_group.add(bottom_pipe)
                pipe_group.add(top_pipe)

                last_pipe = time_now

            ground_scroll -= ground_speed

            if abs(ground_scroll) > 35:
                ground_scroll = 0

            pipe_group.update(ground_speed)

        # Após o fim do jogo, mostra o botão de reinício.
        if is_game_over == True:
            if button.draw(screen) == True:
                is_game_over = False

                score = reset_game(pipe_group, flappy)

        # Eventos do Pygame: fechar janela e iniciar o voo no primeiro clique.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and flappy.flying == False
                and is_game_over == False
            ):
                flappy.flying = True

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
