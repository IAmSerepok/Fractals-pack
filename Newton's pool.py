import pygame as pg
import numpy as np
import numba


# settings
screen_size = width, height = 800, 800
offset = np.array([width//2, height//2])
max_iter = 60
zoom = 5


class Fractal:

    def __init__(self, app_):
        self.app = app_
        self.screen_array = np.full((width, height, 3), [0, 0, 0], dtype=np.uint8)

    @staticmethod
    @numba.njit(fastmath=True, parallel=True)
    def render(screen_array):
        for x in numba.prange(width):
            for y in numba.prange(height):
                c = complex((x - offset[0]) * zoom, (y - offset[1]) * zoom)
                col = 0
                num_iter = 0
                for i in numba.prange(max_iter):
                    f = c**6 - 1  # функция
                    if f.real**2 + f.imag**2 < 0.00001:
                        col = num_iter / max_iter * 255
                        break
                    df = 6*c**5  # производная функции
                    if df != complex(0):
                        c = c - (f / df)
                    else:
                        break
                    num_iter += 1
                screen_array[x, y][2] = col
        return screen_array

    def update(self):
        self.screen_array = self.render(self.screen_array)

    def draw(self):
        pg.surfarray.blit_array(self.app.screen, self.screen_array)

    def run(self):
        self.update()
        self.draw()


class App:

    def __init__(self):
        self.screen = pg.display.set_mode(screen_size, pg.SCALED)
        pg.display.set_caption("Бассейн Ньютона")
        self.clock = pg.time.Clock()
        self.fractal = Fractal(self)

    def run(self):
        self.screen.fill('black')
        self.fractal.run()
        pg.display.flip()
        while True:
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            self.clock.tick()


app = App()
app.run()
