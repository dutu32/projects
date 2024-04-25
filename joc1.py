import pygame
import random


pygame.init()


WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 5


BALL_SIZE = 20
BALL_SPEED_X = 5
BALL_SPEED_Y = 5


class Paddle(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, HEIGHT // 2)

    def update(self):
        keys = pygame.key.get_pressed()
        if self.rect.top > 0 and keys[pygame.K_UP]:
            self.rect.y -= PADDLE_SPEED
        if self.rect.bottom < HEIGHT and keys[pygame.K_DOWN]:
            self.rect.y += PADDLE_SPEED


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.dx = BALL_SPEED_X
        self.dy = BALL_SPEED_Y

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.dy *= -1

    
        if pygame.sprite.spritecollideany(ball, paddles):
            self.dx *= -1

     
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.rect.center = (WIDTH // 2, HEIGHT // 2)
            self.dx *= random.choice([-1, 1])
            self.dy *= random.choice([-1, 1])


paddle1 = Paddle(20)
paddle2 = Paddle(WIDTH - 20)
ball = Ball()

paddles = pygame.sprite.Group()
paddles.add(paddle1)
paddles.add(paddle2)

all_sprites = pygame.sprite.Group()
all_sprites.add(paddle1)
all_sprites.add(paddle2)
all_sprites.add(ball)

clock = pygame.time.Clock()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()


    screen.fill(BLACK)


    all_sprites.draw(screen)


    pygame.display.flip()

   
    clock.tick(FPS)


pygame.quit()
