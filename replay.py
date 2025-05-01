import os
# Ensure video mode is enabled for replay
if "SDL_VIDEODRIVER" in os.environ:
    del os.environ["SDL_VIDEODRIVER"]




import pygame
import neat
import pickle

from main import Bird, Pipe, Base, draw_window, WIN_WIDTH, WIN_HEIGHT, BG_IMG

def replay_best_bird(config_path, genome_path="best_bird.pkl"):
    # Load the saved genome
    with open(genome_path, "rb") as f:
        genome = pickle.load(f)

    # Load NEAT config
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    # Create neural network from the genome
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    bird = Bird(230, 350)
    base = Base(430)
    pipes = [Pipe(600)]

    # ✅ Critical fix: Initialize Pygame video system
    pygame.init()
    pygame.display.init()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Flappy Bird AI - Replay Best Bird")

    clock = pygame.time.Clock()
    score = 0
    run = True

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        bird.move()
        output = net.activate((bird.y, abs(bird.y - pipes[0].height), abs(bird.y - pipes[0].bottom)))
        if output[0] > 0.5:
            bird.jump()

        add_pipe = False
        rem = []
        for pipe in pipes:
            pipe.move()
            if pipe.collide(bird):
                run = False
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

        if add_pipe:
            score += 1
            pipes.append(Pipe(600))

        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >= 430 or bird.y < 0:
            run = False

        base.move()
        draw_window(win, [bird], pipes, base, score, "Best")

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    replay_best_bird(config_path)
