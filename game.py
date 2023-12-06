import pygame
from pygame import mixer
import random

# pygame setup
pygame.init()
window_x = 1200
window_y = 700
bounds = (window_x, window_y)
screen = pygame.display.set_mode(bounds)
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
running = True
dt = 0

velocity = pygame.Vector2(0, 0)

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
initial_body_segments = 3
body_segment_spacing = 50
snake_body = [player_pos.copy() - pygame.Vector2(i * body_segment_spacing, 0) for i in range(initial_body_segments)]
speed = 250

move_started = False

#mixer.init()
#mixer.music.load('audio/munch.mp3')
#mixer.music.set_volume(0.2)
#mixer.music.play()

# apples
fruit_position = [random.randrange(1, (window_x//10)) * 10,
                  random.randrange(1, (window_y//10)) * 10]
fruit_spawn = True

# starting score
score = 0

counter = 0
prev_direction = pygame.Vector2(0, 0)
font = pygame.font.Font(None, 36)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not move_started:
            move_started = True

    screen.fill("dark green")

    fruit_radius = 15
    pygame.draw.circle(screen, "red", (fruit_position[0], fruit_position[1]), fruit_radius)

    snake_radius = 20
    for i, segment in enumerate(snake_body):
        if i == 0:
            pygame.draw.circle(screen, "blue", (int(segment[0]), int(segment[1])), snake_radius)
        else:
            pygame.draw.circle(screen, "white", (int(segment[0]), int(segment[1])), snake_radius)

    keys = pygame.key.get_pressed()
    if move_started:
        new_velocity = pygame.Vector2(0, 0)
        if keys[pygame.K_UP] and prev_direction != pygame.Vector2(0, 1):
            new_velocity = pygame.Vector2(0, -speed)
        if keys[pygame.K_DOWN] and prev_direction != pygame.Vector2(0, -1):
            new_velocity = pygame.Vector2(0, speed)
        if keys[pygame.K_LEFT] and prev_direction != pygame.Vector2(1, 0):
            new_velocity = pygame.Vector2(-speed, 0)
        if keys[pygame.K_RIGHT] and prev_direction != pygame.Vector2(-1, 0):
            new_velocity = pygame.Vector2(speed, 0)

        if new_velocity != pygame.Vector2(0, 0):
                velocity = new_velocity
                prev_direction = velocity.normalize()

    player_pos += velocity * dt

    player_pos.x = max(0, min(player_pos.x, window_x - 1))
    player_pos.y = max(0, min(player_pos.y, window_y - 1))

    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x//10)) * 10,
                          random.randrange(1, (window_y//10)) * 10]
        fruit_spawn = True

    distance = pygame.Vector2(player_pos[0] - fruit_position[0], player_pos[1] - fruit_position[1]).length()
    if distance < snake_radius + fruit_radius:
        score += 5
        fruit_spawn = False
        speed += 10
        snake_body.append(player_pos.copy())

        pygame.time.delay(10)

    else:
        snake_body.pop()

    if player_pos.x == 0 or player_pos.x == window_x - 1 or player_pos.y == 0 or player_pos.y == window_y - 1:
        running = False

    snake_body.insert(0, player_pos.copy())

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()
