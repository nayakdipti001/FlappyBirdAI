import os
os.environ["SDL_VIDEODRIVER"] = "dummy"  # Enable headless mode before importing pygame

import pygame
import neat
import random
import pickle
import matplotlib.pyplot as plt
import numpy as np
import visualize  # New module to draw network (ensure visualize.py is present)

pygame.font.init()

WIN_WIDTH = 600
WIN_HEIGHT = 499
GEN = 0  # generation counter
fitness_history = []  # To store max fitness per generation
avg_fitness_history = []  # To store average fitness per generation

# Load assets and scale to window size
BIRD_IMGS = [
    pygame.image.load("images/bird1.png"),
    pygame.image.load("images/bird2.png"),
    pygame.image.load("images/bird3.png"),
]
PIPE_IMG = pygame.image.load("images/pipe.png")
BASE_IMG = pygame.image.load("images/base.png")
BG_IMG = pygame.transform.scale(pygame.image.load("images/background.jpg"), (WIN_WIDTH, WIN_HEIGHT))

STAT_FONT = pygame.font.SysFont("comicsans", 30)

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2
        d = min(d, 16)
        if d < 0:
            d -= 2
        self.y += d
        if d < 0 or self.y < self.height + 50:
            self.tilt = self.MAX_ROTATION
        else:
            self.tilt = max(self.tilt - self.ROT_VEL, -90)

    def draw(self, win):
        self.img_count += 1
        self.img = self.IMGS[self.img_count // self.ANIMATION_TIME % 3]
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    GAP = 150
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.gap = self.GAP
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 350)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.gap

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)
        return b_point or t_point

class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

def draw_window(win, birds, pipes, base, score, gen):
    win.blit(BG_IMG, (0, 0))
    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)
    for bird in birds:
        bird.draw(win)
    text = STAT_FONT.render(f"Score: {score}", 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    gen_text = STAT_FONT.render(f"Gen: {gen}", 1, (255, 255, 255))
    win.blit(gen_text, (10, 10))
    pygame.display.update()

def main(genomes, config, render=True):
    global GEN
    GEN += 1
    nets = []
    ge = []
    birds = []
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    base = Base(430)
    pipes = [Pipe(700)]

    if render:
        pygame.display.init()
        win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    else:
        win = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))

    clock = pygame.time.Clock()
    score = 0
    run = True
    while run:
        clock.tick(30)
        if render:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()

        if len(birds) == 0:
            run = False
            break

        pipe_ind = 0
        if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
            pipe_ind = 1

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1
            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
            if output[0] > 0.5:
                bird.jump()

        base.move()
        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)
            if len(birds) > 0 and not pipe.passed and pipe.x < birds[0].x:
                pipe.passed = True
                add_pipe = True
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600))

        for r in rem:
            pipes.remove(r)

        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 430 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        if render:
            draw_window(win, birds, pipes, base, score, GEN)

def run(config_path, render=False):
    neat_config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    p = neat.Population(neat_config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    def wrapped_main(genomes, config):
        return main(genomes, config, render)

    winner = p.run(wrapped_main, 50)

    # Plot best and average fitness over generations
    generations = list(range(len(stats.most_fit_genomes)))
    best_fitness = [g.fitness for g in stats.most_fit_genomes]
    avg_fitness = stats.get_fitness_mean()

    plt.plot(generations, best_fitness, label="Best Fitness", color="blue")
    plt.plot(generations, avg_fitness, label="Average Fitness", color="orange", linestyle="--")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.title("Fitness Over Generations")
    plt.legend()
    plt.grid(True)
    plt.savefig("fitness_plot.png")
    plt.show()

    # Visualize the best neural network
    visualize.draw_net(neat_config, winner, view=True, filename="winner_net")

    return winner

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    winner = run(config_path, render=False)

    with open("best_bird.pkl", "wb") as f:
        pickle.dump(winner, f)