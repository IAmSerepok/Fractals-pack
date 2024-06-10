import pygame
import numpy as np
from random import random


class SIF:

    def __init__(self, app_):
        self.app = app_
        self.transformation = []
        self.probabilities = []
        self.current_point = [0, 0]

    def get_random_transformation(self):

        pos = random()
        index = 0
        for chance in self.probabilities:
            if pos > chance:
                index += 1

        return self.transformation[index]

    def get_next_point(self):

        x, y = self.current_point
        a, b, c, d, e, f = self.get_random_transformation()
        cords = np.matrix([[a, b], [c, d]]) * np.matrix([[x], [y]]) + np.matrix([[e], [f]])
        x = cords[0].item()
        y = cords[1].item()
        self.current_point = [x, y]


class App:

    def __init__(self, size, position, bg_color):

        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen_width = 600
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.scale = size
        self.pos = position
        self.screen.fill(bg_color)
        self.FPS = 120
        self.sif = SIF(self)

    def set_transformations(self, rules_):
        self.sif.transformation = rules_

    def set_probabilities(self, probabilities):
        counter = 0
        for chance in probabilities:
            counter += chance
            self.sif.probabilities.append(counter)

    def run(self, max_iter, speed, point_color):

        n_iter = 1
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            for _ in range(speed):
                if n_iter < max_iter:
                    x, y = self.sif.current_point
                    pygame.draw.circle(self.screen, point_color,
                                       (x * self.scale[0] + self.pos[0], y * self.scale[1] + self.pos[1]), 1)
                    self.sif.get_next_point()
                    n_iter += speed

            pygame.display.update()
            self.clock.tick(self.FPS)


app = App(size=(50, 50), position=(250, 70), bg_color='black')
app.set_transformations([(0, 0, 0, 0.16, 0, 0),
(0.85, 0.04, -0.04, 0.85, 0, 1.6),
(0.2, -0.26, 0.23, 0.22, 0, 1.6),
(-0.15, 0.28, 0.26, 0.24, 0, 0.44)])

app.set_probabilities([0.01, 0.85, 0.07, 0.07])
app.run(max_iter=5000000000, speed=2, point_color='green')
