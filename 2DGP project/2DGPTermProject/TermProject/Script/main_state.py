import random
import json
import os

from pico2d import *
import game_framework
import game_world

from boy import Boy
from grass import Grass
from ball import Ball
from testBack import TestBack

from enemyTest import EnemyTest
from busterProjectile import BusterProjectile


screenX = 1600
screenY = 600


name = "MainState"

boy = None
grass = None


enemyTest = None

testBack = None

#예시
def stage_1():
    pass

#기본 스테이지
def enter():
    global boy, grass , enemyTest , testBack
    boy = Boy()
    grass = Grass()
    enemyTest = EnemyTest()
    testBack = TestBack()


    game_world.add_object(testBack,0)

    game_world.add_object(grass, 0)
    game_world.add_object(boy, 1)
    game_world.add_object(enemyTest,1)


def exit():
    global boy, grass
    del boy
    del grass
    game_world.clear()

def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            boy.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()

        for game_object_b in game_world.all_objects():

            if(game_object_b != game_object):
                for relation in game_object_b.collisionRelation:
                    if relation == game_object.kind:
                        if (collide(game_object_b,game_object)):
                            if (type(game_object_b) == BusterProjectile):
                                game_object_b.CollisionHandling(None)
                                if (game_object.kind == game_world.Monster):
                                    game_object.CollisionHandling(game_object_b)





def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b:
        return False
    if right_a < left_b:
        return False
    if top_a < bottom_b:
        return False
    if bottom_a > top_b:
        return False
    return True
    # fill here
    pass


def PushCollide(floating,fixed):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a < right_b:
        return False
    if right_a > left_b:
        return False
    if top_a > bottom_b:
        return False
    if bottom_a < top_b:
        return False

    pass



