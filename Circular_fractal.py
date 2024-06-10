import pygame
import math


def get_pos(center_, radius_, angle_):
    x = center_[0] + radius_ * math.cos(math.radians(angle_) - math.pi / 2)
    y = center_[1] + radius_ * math.sin(math.radians(angle_) - math.pi / 2)
    return x, y


class Circle:
    def __init__(self, app_, center_, radius_, angle_, lvl_):

        self.center = center_
        self.app = app_
        self.radius = radius_
        self.angle = angle_
        self.lvl = lvl_

    def draw(self):
        pygame.draw.circle(self.app.surface, 'gray', self.center, self.radius, 2)
        if self.lvl > 0:
            delta = 360 / self.app.number_of_circle
            for _ in range(self.app.number_of_circle):
                center = get_pos(self.center, 2*self.radius/3, self.angle)
                circ = Circle(self.app, center, 1*self.radius/3, 0, self.lvl - 1)
                circ.draw()
                self.update(delta)
            if self.app.number_of_circle == 6:
                circ = Circle(self.app, self.center, 1 * self.radius / 3, 0, self.lvl - 1)
                circ.draw()

    def update(self, delta):
        self.angle = (self.angle + delta) % 360


class App:

    def __init__(self, length, number_of_circle, lvl):

        pygame.init()
        self.FPS = 60
        self.screen_width = 1200
        self.screen_height = 800
        self.surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()

        self.center = (self.screen_width//2, self.screen_height//2)
        self.number_of_circle = number_of_circle
        self.length = length
        self.circle = Circle(self, self.center, self.length, 0, lvl)

    def run(self):

        while True:

            self.surface.fill('black')
            self.circle.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            pygame.display.flip()
            self.clock.tick(self.FPS)


app = App(length=350, number_of_circle=6, lvl=5)
app.run()
