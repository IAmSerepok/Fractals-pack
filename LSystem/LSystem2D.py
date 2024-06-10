import turtle
import re
import random


# список функций для управления параметаризированными командами
# у всех функций будет префикс cmd_ и первый параметр t - черепашка
def cmd_turtle_fd(t_, length, *args):
    t_.pensize(args[1])
    t_.fd(length * args[0])


def cmd_turtle_left(t_, angle_, *args):
    t_.left(angle_ * args[0])


def cmd_turtle_right(t_, angle_, *args):
    t_.right(angle_ * args[0])


def cmd_turtle_jump(t_, length, *args):
    t_.up()
    t_.fd(length * args[0])
    t_.down()


class LSystem2D:

    def __init__(self, t_, axiom_, width_, length_, angle_):

        self.axiom = axiom_
        self.state = axiom_
        self.width = width_
        self.length = length_
        self.angle = angle_
        self.t = t_
        self.rules = {}
        self.t.pensize(self.width)
        self.function_key = None
        self.key_re_list = []
        self.cmd_functions = {}

    def add_rules(self, *rules):

        for key, value in rules:

            key_re = ""

            if not isinstance(value, str):
                key_re = key.replace("(", r"\(")
                key_re = key_re.replace(")", r"\)")
                key_re = key_re.replace("+", r"\+")
                key_re = key_re.replace("-", r"\-")
                key_re = re.sub(r"([a-z]+)([, ]*)", lambda m: r"([-+]?\b\d+(?:\.\d+)?\b)" + m.group(2), key_re)
                self.key_re_list.append(key_re)

            self.rules[key] = (value, key_re)

    def update_param_cmd(self, m):

        if not self.function_key:
            return ""

        args = list(map(float, m.groups()))
        return self.function_key(*args).lower()

    def generate_path(self, lvl):

        for n in range(lvl):

            for key, values in self.rules.items():

                if isinstance(values[0], str):
                    self.state = self.state.replace(key, values[0].lower())

                else:
                    self.function_key = values[0]
                    self.state = re.sub(values[1], self.update_param_cmd, self.state)
                    self.function_key = None

            self.state = self.state.upper()

    def set_turtle(self, my_tuple):

        self.t.up()
        self.t.goto(my_tuple[0], my_tuple[1])
        self.t.seth(my_tuple[2])
        self.t.down()

    def add_rules_move(self, *moves):

        for key, func in moves:
            self.cmd_functions[key] = func

    def draw_turtle(self, start_pos, start_angle):

        turtle.tracer(1, 0)
        self.t.up()
        self.t.setpos(start_pos)
        self.t.seth(start_angle)
        self.t.down()
        turtle_stack = []
        key_list_re = "|".join(self.key_re_list)

        for values in re.finditer(r"(" + key_list_re + r"|.)", self.state):
            cmd = values.group(0)
            args = [float(x) for x in values.groups()[1:] if x]

            if 'F' in cmd:
                if len(args) > 0 and self.cmd_functions.get('F'):
                    self.cmd_functions['F'](t, self.length, *args)
                else:
                    self.t.fd(self.length)
            elif 'S' in cmd:
                if len(args) > 0 and self.cmd_functions.get('S'):
                    self.cmd_functions['S'](t, self.length, *args)
                else:
                    self.t.up()
                    self.t.forward(self.length)
                    self.t.down()
            elif '+' in cmd:
                if len(args) > 0 and self.cmd_functions.get('+'):
                    self.cmd_functions['+'](t, self.angle, *args)
                else:
                    self.t.left(self.angle)
            elif '-' in cmd:
                if len(args) > 0 and self.cmd_functions.get('-'):
                    self.cmd_functions['-'](t, self.angle, *args)
                else:
                    self.t.right(self.angle)
            elif "[" in cmd:
                turtle_stack.append((self.t.xcor(), self.t.ycor(), self.t.heading(), self.t.pensize()))
            elif "]" in cmd:
                xcor, ycor, head, w = turtle_stack.pop()
                self.set_turtle((xcor, ycor, head))
                self.width = w
                self.t.pensize(self.width)

        turtle.done()


t = turtle.Turtle()
t.ht()

pen_width = 2
f_len = 2
angle = 120

axiom = "FXF--FF--FF"

l_sys = LSystem2D(t, axiom, pen_width, f_len, angle)

l_sys.add_rules(("F", "FF"),
("X", "--FXF++FXF++FXF--")
                )

l_sys.add_rules_move(("F", cmd_turtle_fd), ("+", cmd_turtle_left), ("-", cmd_turtle_right), ("S", cmd_turtle_jump))
l_sys.generate_path(4)
print(l_sys.state)
l_sys.draw_turtle((100, -100), 90)
