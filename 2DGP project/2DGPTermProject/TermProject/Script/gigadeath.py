from pico2d import *

import game_world
import game_framework
import main_state
import random

from objectBase import ObjectBase
from busterProjectile import BusterProjectile
from explosionEffect import ExplosionEffect

from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode


from ioriExplosion import IoriExplosion




# Boy Run Speed
# fill expressions correctly
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
# fill expressions correctly

TIME_PER_ACTION = 0.75
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Gigadeath(ObjectBase):
    actions = 1
    idle = 0

    # test = {"ImageFile" : None,"IntervalX" : None,"IntervalY" : None,"Frames" : None}


    spriteSheet = None

    Images = []

    Test = True

    for i in range(actions):
        Images.append({"ImageFile": None, "IntervalX": None, "IntervalY": None, "Frames": None, "XRevision": None,"YRevision": None})

    Images[idle]["IntervalX"] = 100
    Images[idle]["IntervalY"] = 100
    Images[idle]["Frames"] = 4
    Images[idle]["XRevision"] = 0
    Images[idle]["YRevision"] = 0





    deathAnimationActions = 3

    defaultDeathAnimation, deathImmediately, specialDeathAnimation = range(deathAnimationActions)

    deathAnimations = []

    for i in range(deathAnimationActions):
        deathAnimations.append(
            {"ImageFile": None, "IntervalX": None, "IntervalY": None, "Frames": None, "XRevision": None,"YRevision": None})

    deathAnimations[deathImmediately]["IntervalX"] = 100
    deathAnimations[deathImmediately]["IntervalY"] = 100
    deathAnimations[deathImmediately]["Frames"] = 1
    deathAnimations[deathImmediately]["XRevision"] = 0

    def __init__(self):

        if (Gigadeath.spriteSheet == None):
            Gigadeath.spriteSheet = load_image('sprite/GigadeathIdle.png')

        self.kind = game_world.Monster

        self.land = False

        self.x, self.y = main_state.screenX - 400, 250
        self.dir = -1

        self.frame = 0
        self.event_que = []

        # self.cur_state = BusterProjectile.small

        # self.cur_state.enter(self, None)
        self.imageState = Gigadeath.idle


        self.collisionRelation = [game_world.Feature]

        self.selfGravity = False


        self.velocity = 0
        self.velocityY = 0

        self.firePositionX = PIXEL_PER_METER * 0.3
        self.firePositionY = PIXEL_PER_METER * 0.2

        self.x += self.firePositionX
        self.y += self.firePositionY

        #바운딩 박스 출력여부를 결정한다
        self.boundingBoxOn = False

        self.tempGravity = 3

        self.startTimer = get_time()
        self.endTimer = 0

        self.hPMax = 200

        self.curHP = clamp(0, self.hPMax, self.hPMax)

        self.shallHandleCollision = True

        self.deathAnimationNumber = Gigadeath.deathImmediately

        self.beingDeath = False
        self.deathAnimationFrame = 0

        self.clearness = 1



        self.speed = 0

        self.timer = 1.0  # change direction every 1 sec when wandering

        self.build_behavior_tree()

        self.recognizeRange = 100
        self.smashRange = 20


        self.smashDamage = 100

        # self.subject = boy


        self.curState = game_framework.stack[-1]

        self.moneyToGive = 200

        print(self.clearness)

    def set_direction(self):

        pass

    def DeathAnimation(self):

        self.beingDeath = True
        self.shallHandleCollision = False

        if (self.deathAnimationNumber == Gigadeath.deathImmediately):

            if (int(self.deathAnimationFrame) % 3 == 0):
                explosion = ExplosionEffect(random.randint(int(self.get_bb()[0]), int(self.get_bb()[2])),
                                            random.randint(int(self.get_bb()[1]), int(self.get_bb()[3])), self.dir, 0,
                                            0)
                game_world.add_object(explosion, 1)

        pass

    def destroy(self):
        game_world.remove_object(self)

        pass

    def update(self):

        self.endTimer = get_time() - self.startTimer



        # self.set_direction()

        if (not self.beingDeath):
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % Gigadeath.Images[self.imageState]["Frames"]
            #self.bt.run()
            self.x += self.velocity * self.dir * game_framework.frame_time

        else:
            if (self.deathAnimationNumber == Gigadeath.deathImmediately):
                self.DeathAnimation()
                self.deathAnimationFrame = (
                                                       self.deathAnimationFrame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % \
                                           Gigadeath.deathAnimations[self.deathAnimationNumber]["Frames"]

                if (self.deathAnimationFrame >= Gigadeath.deathAnimations[self.deathAnimationNumber]["Frames"] - 1):
                    self.destroy()



        self.x = clamp(0, self.x, 1600)
        self.y = clamp(0, self.y, 1000)


        pass

    def draw(self):
        if self.curState.showBoundingBox:
            self.draw_bb()
        elif self.boundingBoxOn:
            self.draw_bb()


        if self.dir == 1:
            Gigadeath.spriteSheet.clip_composite_draw(int(self.frame) * Gigadeath.Images[self.imageState]["IntervalX"] + Gigadeath.Images[self.imageState]["XRevision"], Gigadeath.Images[self.imageState]["IntervalY"] * self.imageState, Gigadeath.Images[self.imageState]["IntervalX"],
                                                      Gigadeath.Images[self.imageState]["IntervalY"], 0, '', self.x - self.curState.GetBackground().windowLeft, self.y - self.curState.GetBackground().windowBottom, Gigadeath.Images[self.imageState]["IntervalX"], Gigadeath.Images[self.imageState]["IntervalY"])
        else:
            Gigadeath.spriteSheet.clip_composite_draw(int(self.frame) * Gigadeath.Images[self.imageState]["IntervalX"] + Gigadeath.Images[self.imageState]["XRevision"], Gigadeath.Images[self.imageState]["IntervalY"] * self.imageState, Gigadeath.Images[self.imageState]["IntervalX"],
                                                      Gigadeath.Images[self.imageState]["IntervalY"], 0, 'h', self.x - self.curState.GetBackground().windowLeft, self.y - self.curState.GetBackground().windowBottom, Gigadeath.Images[self.imageState]["IntervalX"], Gigadeath.Images[self.imageState]["IntervalY"])

        if self.beingDeath:
            pass


    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 40, self.y + 20

    # fill here

    def draw_bb(self):
        left,bottom,right,top = self.get_bb()

        left -= self.curState.GetBackground().windowLeft
        bottom -= self.curState.GetBackground().windowBottom
        right -= self.curState.GetBackground().windowLeft
        top -= self.curState.GetBackground().windowBottom


        draw_rectangle(left,bottom,right,top)

    def CollisionHandling(self, object):

        if (not self.shallHandleCollision):
            return

        self.curHP -= object.damage
        if (self.curHP <= 0):
            self.DeathAnimation()
            if(object != None):
                object.subject.money += self.moneyToGive

    def SetPosition(self,x,y):


        self.x = x
        self.y = y

        pass



#인공지능 추가

    def wander(self):
        # fill here

        #state change
        self.imageState = Gigadeath.walking


        self.velocity = RUN_SPEED_PPS
        self.timer -= game_framework.frame_time
        if self.timer < 0:
            self.timer += 1.0
            self.dir = random.randint(-1,0)
            if(self.dir == 0):
                self.dir = 1
        return BehaviorTree.SUCCESS

        pass

    def find_player(self):
        # fill here
        #state change
        self.imageState = Gigadeath.walking


        boy = self.curState.get_boy()
        distance = (boy.x - self.x) ** 2
        if distance < (PIXEL_PER_METER * self.recognizeRange) ** 2:

            if(boy.x - self.x < 0):
                self.dir = -1
            else:
                self.dir = 1

            return BehaviorTree.SUCCESS
        else:
            self.velocity = 0
            return BehaviorTree.FAIL
        pass

    def move_to_player(self):
        # fill here
        self.velocity = RUN_SPEED_PPS


        #state change
        self.imageState = Gigadeath.walking


        boy = self.curState.get_boy()
        distance = (boy.x - self.x) ** 2
        if distance < (PIXEL_PER_METER * self.smashRange) ** 2:

            if(boy.x - self.x < 0):
                self.dir = -1
            else:
                self.dir = 1

            return BehaviorTree.SUCCESS

        if distance >=(PIXEL_PER_METER * self.recognizeRange) ** 2:

            if(boy.x - self.x < 0):
                self.dir = -1
            else:
                self.dir = 1

            return BehaviorTree.FAIL

        else:
            return BehaviorTree.RUNNING






        pass


    def SmashAttack(self):

        boy = self.curState.get_boy()
        self.velocity = 0

        #state change
        self.imageState = Gigadeath.smashing

        if(self.frame >= 3):
            if(self.frame - int(self.frame) < 0.1):
                explosion = IoriExplosion(boy.x ,self.y,-self.dir,self.smashDamage)
                game_world.add_object(explosion,1)

        return BehaviorTree.SUCCESS

        pass


    def build_behavior_tree(self):
        # fill here

        wander_node = LeafNode("Wander", self.wander)


        find_player_node = LeafNode("Find Player", self.find_player)
        move_to_player_node = LeafNode("Move to Player", self.move_to_player)
        SmashAttckNode = LeafNode("Smash Attck",self.SmashAttack)

        chase_node = SequenceNode("Chase")
        chase_node.add_children(find_player_node, move_to_player_node)
        chase_node.add_child(SmashAttckNode)

        wander_chase_node = SelectorNode("WanderChase")
        wander_chase_node.add_children(chase_node, wander_node)


        self.bt = BehaviorTree(wander_chase_node)

        #wander_node = LeafNode("Wander", self.wander)
        #self.bt = BehaviorTree(wander_node)
        pass