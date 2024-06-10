import tkinter as tk
from math import sin, cos, pi
from PIL import ImageGrab


class App(tk.Tk):
    def __init__(self, size, axiom, angle, length, width, start):
        super().__init__()
        self.title("Dragon curve")
        self.label = tk.Label(self)
        self.canvas = tk.Canvas(self, height=size[0], width=size[1], bg='#1e1f22')
        self.canvas.pack()

        self.canvas.pack()
        self.label.pack()
        self.axiom = axiom
        self.pattern = axiom
        self.width = width
        self.rules = {}
        self.length, self.angle = length, angle
        self.x, self.y = start
        self.x_prev, self.y_prev, self.start_angle = self.x, self.y, 0

        self.gradient = [
            # for tree
            # '#934900'
            # for tree
            # '#69ab72', '#5aa461', '#4a9d4f', '#3a963d', '#288f28'
            # for snowflake
            # '#ffffff'
            # for dragon
            '#00ff22', '#00fd37', '#00fa47', '#00f856', '#00f564',
            '#00f272', '#00ef7f', '#00eb8c', '#00e89a', '#00e4a7',
            '#00e1b4', '#00ddc1', '#00d9ce', '#00d5db', '#00d1e8',
            '#00cdf4', '#00c9ff', '#00c5ff', '#00c1ff', '#00bcff',
            '#00b8ff', '#00b4ff', '#00afff', '#00aaff', '#00a5ff',
            '#00a0ff', '#009bff', '#0095ff', '#008fff', '#0089ff',
            '#0082ff', '#007bff', '#0073ff', '#006aff', '#0061ff',
            '#0057ff', '#004aff', '#003cff', '#0029ff', '#1500ff'
        ]
        self.step = 0

    def create_pattern(self, n_iter):
        for _ in range(n_iter):
            for key, values in self.rules.items():
                self.pattern = self.pattern.replace(key, values[0].lower())
            self.pattern = self.pattern.upper()

    def add_rules(self, *rules):
        for key, value in rules:
            key_re = ""
            self.rules[key] = (value, key_re)

    def save(self):
        ImageGrab.grab().save('../../NewYear/temp.png')

    def draw(self):
        for c in self.pattern:
            if c == '+':
                self.start_angle += self.angle
            elif c == '-':
                self.start_angle -= self.angle
            elif c == 'F':
                self.x = self.x_prev + self.length * sin(self.start_angle * pi / 180)
                self.y = self.y_prev + self.length * cos(self.start_angle * pi / 180)
                self.canvas.create_polygon([self.x_prev, self.y_prev,
                                            self.x, self.y], outline=self.gradient[self.step],
                                           width=self.width)
                self.x_prev, self.y_prev = self.x, self.y
                self.step = (self.step + 1) % len(self.gradient)
                self.update()

    def run(self):
        self.draw()
        self.mainloop()
        self.save()


f_len = 4
f_width = 2
angle_ = 90
start_pos = [500, 550]
axiom_ = "-FX"
app = App([800, 1200], axiom_, angle_, f_len, f_width, start_pos)
app.add_rules(("FX", "FX+FY+"), ("FY", "-FX-FY"))
app.create_pattern(13)
print(app.pattern)
# app.pattern = app.pattern + '--' + app.pattern + '--' + app.pattern
app.run()
