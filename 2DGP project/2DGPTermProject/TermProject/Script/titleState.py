import game_framework
from pico2d import *
import stage1
import random
import tutorialState

name = "TitleState"
image = None
font = None

screenX = 1600
screenY = 600

firtGenerated = False

def enter():
    global  image, font
    image = load_image('sprite/titleLogo/titleScreen.png')
    font = load_font('ENCR10B.TTF')

def exit():
    global  image
    del(image)


def handle_events():
    global firtGenerated
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type,event.key) ==(SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                if not firtGenerated:
                    game_framework.change_state(tutorialState)
                    firtGenerated = True
                else:
                    game_framework.change_state(stage1)


def draw():

    clear_canvas()
    image.draw(stage1.screenX//2,stage1.screenY//2,stage1.screenX,stage1.screenY)

    font.draw(stage1.screenX // 2 * 0.8,stage1.screenY * 0.2, 'Press Space Button' ,(random.randint(55,255),random.randint(155,255),random.randint(195,255)))
    update_canvas()








def update():
    pass


def pause():
    pass


def resume():
    pass






