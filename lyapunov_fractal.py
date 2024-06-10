import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


class App:
    def __init__(self, pattern, delta, x, y):
        self.pattern = pattern
        self.delta = delta
        self.x_start, self.x_end = x
        self.y_start, self.y_end = y

    def r(self, n, a, b):
        if self.pattern[n % len(self.pattern)] == 'A':
            return a
        else:
            return b

    def draw(self):
        x_range = int((self.x_end - self.x_start) / self.delta) + 1
        y_range = int((self.y_end - self.y_start) / self.delta) + 1
        data = np.zeros((y_range, x_range))

        # Calculate Lyapunov exponents
        for i in range(x_range):
            for j in range(y_range):
                a = self.x_start + i * self.delta
                b = self.y_start + j * self.delta
                x0 = 0.5
                lyapunov_exp = 0

                n_max = 150

                for n in range(n_max):
                    x0 = self.r(n, a, b) * x0 * (1 - x0)
                    lyapunov_exp += np.log(np.abs(self.r(n, a, b) * (1 - 2 * x0)) + 1e-10)

                data[j, i] = lyapunov_exp / n_max

            print(f'{i + 1} / {x_range}')

        # for i in range(x_range):
        #     for j in range(y_range):
        #         if data[j, i] > 0: data[j, i] /= data_max
        #         elif data[j, i] < 0: data[j, i] /= - data_min

        # for _ in range(len(cmaps)):
        #     plt.figure(figsize=(14, 7))
        #     plt.imshow(data.T, cmap=cmaps[_], origin='lower')
        #     plt.colorbar()
        #     plt.axis('off')
        #     plt.gca().set_aspect('auto', adjustable='box')
        #     plt.savefig(f'ex1/lyapunov{_}_fractal.jpg', dpi=300)
        #     plt.close()
        #     print(f'{_ + 1} / {len(cmaps)}')

        # Определение положений цветов в градиенте
        positions = [0, 0.25, 0.495, 0.5, 0.505, 0.75, 1]

        # Определение цветов в градиенте
        colors = [(0, 0, 0),
                  (150 / 255, 100 / 255, 8 / 255), (255 / 255, 243 / 255, 8 / 255),
                  (1, 1, 1),
                  (130 / 255, 110 / 255, 160 / 255), (8 / 255, 5 / 255, 160 / 255),
                  (0, 0, 0)]

        # Создание пользовательской colormap
        data_min = np.min(data)
        data_max = np.max(data)

        positions[1] = np.abs(data_min / 2) / (data_max - data_min)
        positions[2] = np.abs(data_min / 1.1) / (data_max - data_min)
        positions[3] = np.abs(data_min) / (data_max - data_min)
        positions[4] = np.abs(data_min / 0.9) / (data_max - data_min)
        positions[5] = (np.abs(data_min) + np.abs(data_max / 2)) / (data_max - data_min)

        print(positions)

        my_cmap = LinearSegmentedColormap.from_list('cmap', list(zip(positions, colors)))

        plt.figure(figsize=(14, 7))
        plt.imshow(data.T, cmap=my_cmap, origin='lower')
        plt.colorbar()
        plt.axis('off')
        plt.gca().set_aspect('auto', adjustable='box')
        plt.show()


app = App(pattern='AB', delta=0.005, x=[2, 4], y=[2, 4])
app.draw()
