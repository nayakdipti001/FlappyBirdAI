import pygame
import sys
import random


def main():
    pygame.init()

    # Window setup
    window_width = 600
    window_height = 499
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('Flappy Bird Game')

    # Load and scale images
    background = pygame.transform.scale(
        pygame.image.load('images/background.jpg'), (window_width, window_height)
    ).convert()

    # Load bird frames for animation
    bird_frames = [
        pygame.image.load('images/bird1.png').convert_alpha(),
        pygame.image.load('images/bird2.png').convert_alpha(),
        pygame.image.load('images/bird3.png').convert_alpha()
    ]
    bird_index = 0
    bird = bird_frames[bird_index // 5]

    pipe_image = pygame.image.load('images/pipe.png').convert_alpha()
    base = pygame.image.load('images/base.png').convert_alpha()

    # Load sounds
    flap_sound = pygame.mixer.Sound('sounds/wing.wav')
    hit_sound = pygame.mixer.Sound('sounds/hit.wav')
    point_sound = pygame.mixer.Sound('sounds/point.wav')

    # Font for score
    font = pygame.font.SysFont(None, 48)

    # Clock
    clock = pygame.time.Clock()
    fps = 30

    # Bird settings
    bird_x = 100
    bird_y = 250
    bird_velocity = 0
    gravity = 1
    flap_power = -10

    # Pipe settings
    pipe_gap = 150
    pipe_velocity = -4
    pipe_x = window_width
    pipe_height = random.randint(100, 350)

    # Score
    score = 0
    scored = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = flap_power
                    flap_sound.play()

        # Bird physics
        bird_velocity += gravity
        bird_y += bird_velocity

        # Move pipes
        pipe_x += pipe_velocity
        if pipe_x < -pipe_image.get_width():
            pipe_x = window_width
            pipe_height = random.randint(100, 350)
            scored = False  # Reset score flag for new pipe

        # Animate bird flapping
        bird_index += 1
        if bird_index >= len(bird_frames) * 5:
            bird_index = 0
        bird = bird_frames[bird_index // 5]

        # Rectangles for collision detection
        bird_rect = pygame.Rect(bird_x, bird_y, bird.get_width(), bird.get_height())
        upper_pipe_rect = pygame.Rect(pipe_x, pipe_height - pipe_image.get_height() - pipe_gap, pipe_image.get_width(),
                                      pipe_image.get_height())
        lower_pipe_rect = pygame.Rect(pipe_x, pipe_height, pipe_image.get_width(), pipe_image.get_height())

        # Scoring
        if pipe_x + pipe_image.get_width() < bird_x and not scored:
            score += 1
            scored = True
            point_sound.play()

        # Draw everything
        window.blit(background, (0, 0))
        window.blit(bird, (bird_x, bird_y))
        window.blit(pipe_image, (pipe_x, pipe_height))  # lower pipe
        window.blit(pygame.transform.flip(pipe_image, False, True),
                    (pipe_x, pipe_height - pipe_image.get_height() - pipe_gap))  # upper pipe
        window.blit(base, (0, window_height - base.get_height()))

        # Draw score
        score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
        window.blit(score_surface, (10, 10))

        # Game Over Conditions
        if bird_y + bird.get_height() > window_height - base.get_height():
            hit_sound.play()
            game_over_screen(window, window_width, window_height)

        if bird_rect.colliderect(upper_pipe_rect) or bird_rect.colliderect(lower_pipe_rect):
            hit_sound.play()
            game_over_screen(window, window_width, window_height)

        pygame.display.update()
        clock.tick(fps)


def game_over_screen(window, window_width, window_height):
    font = pygame.font.SysFont(None, 48)
    msg = font.render('Game Over! Press R to Restart', True, (255, 0, 0))
    window.blit(msg, (window_width // 8, window_height // 2))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()


if __name__ == "__main__":
    main()
