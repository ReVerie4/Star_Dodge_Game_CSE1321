import pygame
import sys
import random

from pygame.examples.grid import WINDOW_WIDTH, WINDOW_HEIGHT

class Player:
    def __init__(self, x, y, image_path, speed):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.speed = speed
        self.direction = pygame.math.Vector2(0, 0)
    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])

        if self.direction.length() != 0:
            self.direction = self.direction.normalize()
        #update position
        self.rect.centerx += self.direction.x * self.speed * dt
        self.rect.centery += self.direction.y * self.speed * dt

        #limit within bounds
        self.rect.centerx = max(self.rect.width // 2, min(self.rect.centerx, WIDTH - self.rect.width // 2))
        self.rect.centery = max(self.rect.height // 2, min(self.rect.centery, HEIGHT - self.rect.height // 2))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Star:
    def __init__(self, x, y, image_path, scale = None):
        self.image = pygame.image.load(image_path)
        if scale:
            self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect(center=(x, y))

        #initialize direction and speed for movement
        self.direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.speed = 100

    def update(self, dt, player_rect):
        # Move the star in the set direction
        self.rect.centerx += self.direction.x * self.speed * dt
        self.rect.centery += self.direction.y * self.speed * dt

        # Reposition the star when it goes off-screen
        if (self.rect.centerx < -self.rect.width or
                self.rect.centerx > WIDTH + self.rect.width or
                self.rect.centery < -self.rect.height or
                self.rect.centery > HEIGHT + self.rect.height):
            # Reset position to the opposite side of the screen
            edge = random.choice(['top', 'bottom', 'left', 'right'])
            if edge == 'top':
                self.rect.centerx = random.randint(0, WIDTH)
                self.rect.centery = -self.rect.height
            elif edge == 'bottom':
                self.rect.centerx = random.randint(0, WIDTH)
                self.rect.centery = HEIGHT + self.rect.height
            elif edge == 'left':
                self.rect.centerx = -self.rect.width
                self.rect.centery = random.randint(0, HEIGHT)
            elif edge == 'right':
                self.rect.centerx = WIDTH + self.rect.width
                self.rect.centery = random.randint(0, HEIGHT)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

def game_over_screen(screen):
    font = pygame.font.SysFont(None, 74)
    text = font.render('Game Over', True, (255, 0, 0))
    screen.fill((0,0,0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()

pygame.init()



WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Star Display')

background = pygame.image.load('images/background.PNG')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

player = Player(WIDTH // 2, HEIGHT//2, 'images/astronaut.PNG', speed = 500)

#create multiple stars at random positions
num_stars = 10
stars = []
for _ in range(num_stars):
    edge = random.choice(['top', 'bottom', 'left', 'right'])
    if edge == 'top':
        x = random.randint(0, WIDTH)
        y = -75
    elif edge == 'bottom':
        x = random.randint(0, WIDTH)
        y = HEIGHT + 75
    elif edge == 'left':
        x = -75  # Assume the star's width is 75
        y = random.randint(0, HEIGHT)
    elif edge == 'right':
        x = WIDTH + 75  # Assume the star's width is 75
        y = random.randint(0, HEIGHT)

    stars.append(Star(x, y, 'images/yellow_star.PNG', scale =(75, 75)))

clock = pygame.time.Clock()

game_over = False
while not game_over:
    dt = clock.tick(60) / 1000 #amount of seconds between each loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    player.update(dt)

    #update stars
    for star in stars:
        star.update(dt, player.rect)
        if player.rect.colliderect(star.rect):
            game_over = True

    #Draw everything
    screen.blit(background,(0,0))
    for star in stars:
        star.draw(screen)
    player.draw(screen)
    pygame.display.update()


#show game over
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    game_over_screen(screen)
