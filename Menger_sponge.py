from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController


def create_fractal(lvl, position_, scale_):

    if lvl == 0:
        Entity(model='cube', position=position_, scale=scale_)
        return

    d = scale_ / 3
    x, y, z = position_

    create_fractal(lvl-1, [x, y, z], d)
    create_fractal(lvl - 1, [x+d, y, z], d)
    create_fractal(lvl - 1, [x+2*d, y, z], d)
    create_fractal(lvl - 1, [x, y+2*d, z], d)
    create_fractal(lvl - 1, [x, y+d, z], d)
    create_fractal(lvl - 1, [x+2*d, y+2*d, z], d)
    create_fractal(lvl - 1, [x+2*d, y+d, z], d)
    create_fractal(lvl - 1, [x+d, y+2*d, z], d)

    create_fractal(lvl - 1, [x, y, z+d], d)
    create_fractal(lvl - 1, [x+2*d, y, z+d], d)
    create_fractal(lvl - 1, [x, y+2*d, z+d], d)
    create_fractal(lvl - 1, [x+2*d, y+2*d, z+d], d)

    create_fractal(lvl - 1, [x, y, z+2*d], d)
    create_fractal(lvl - 1, [x + d, y, z+2*d], d)
    create_fractal(lvl - 1, [x + 2 * d, y, z+2*d], d)
    create_fractal(lvl - 1, [x, y + 2 * d, z+2*d], d)
    create_fractal(lvl - 1, [x, y + d, z+2*d], d)
    create_fractal(lvl - 1, [x + 2 * d, y + 2 * d, z+2*d], d)
    create_fractal(lvl - 1, [x + 2 * d, y + d, z+2*d], d)
    create_fractal(lvl - 1, [x + d, y + 2 * d, z+2*d], d)


app = Ursina()
window.color = color.black

create_fractal(2, [0, 0, 0], 2)

AmbientLight(color=(0.5, 0.5, 0.5, 1))
DirectionalLight(color=(0.5, 0.5, 0.5, 1), direction=(1, 1, 1))

player = FirstPersonController()
player.gravity = 0.0

app.run()
