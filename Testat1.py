from robolink import *
from robodk import *
RDK = Robolink()

r_robot = RDK.Item('Staubli TX40')
tl_tool = RDK.Item('LWS_VakuumGreifer_11')

f_world = RDK.Item('world', ITEM_TYPE_FRAME)
f_pick = RDK.Item('blocks', ITEM_TYPE_FRAME)
f_place = RDK.Item('tower', ITEM_TYPE_FRAME)
t_home = RDK.Item('home')
t_pickpose = RDK.Item('pickpose')
t_pickpose2 = RDK.Item('pickpose2')

block01 = RDK.Item("block01", ITEM_TYPE_OBJECT)
block02 = RDK.Item("block02", ITEM_TYPE_OBJECT)
block03 = RDK.Item("block03", ITEM_TYPE_OBJECT)
block04 = RDK.Item("block04", ITEM_TYPE_OBJECT)
block05 = RDK.Item("block05", ITEM_TYPE_OBJECT)
block06 = RDK.Item("block06", ITEM_TYPE_OBJECT)
block07 = RDK.Item("block07", ITEM_TYPE_OBJECT)
block08 = RDK.Item("block08", ITEM_TYPE_OBJECT)
block09 = RDK.Item("block09", ITEM_TYPE_OBJECT)
block10 = RDK.Item("block10", ITEM_TYPE_OBJECT)
block11 = RDK.Item("block11", ITEM_TYPE_OBJECT)
block12 = RDK.Item("block12", ITEM_TYPE_OBJECT)
block13 = RDK.Item("block13", ITEM_TYPE_OBJECT)
block14 = RDK.Item("block14", ITEM_TYPE_OBJECT)
block15 = RDK.Item("block15", ITEM_TYPE_OBJECT)
block16 = RDK.Item("block16", ITEM_TYPE_OBJECT)
block17 = RDK.Item("block17", ITEM_TYPE_OBJECT)
block18 = RDK.Item("block18", ITEM_TYPE_OBJECT)
block19 = RDK.Item("block19", ITEM_TYPE_OBJECT)
block20 = RDK.Item("block20", ITEM_TYPE_OBJECT)
block21 = RDK.Item("block21", ITEM_TYPE_OBJECT)
block22 = RDK.Item("block22", ITEM_TYPE_OBJECT)
block23 = RDK.Item("block23", ITEM_TYPE_OBJECT)
block24 = RDK.Item("block24", ITEM_TYPE_OBJECT)

blocks = [block01, block02, block13, block14, block03, block04, block15, block16, block05, block06, block17, block18, block07, block08, block19, block20, block09, block10, block21, block22, block11, block12, block23, block24]

def pick_pose_down(x, y, z, r):
    return f_pick.Pose() * transl(x, y, z) * rotz(r) * rotx(pi) 

def place_pose_down(x, y, z, r):
    return f_place.Pose() * transl(x, y, z) * rotz(r) * rotx(pi) 

def pose_up(down_pose, z):
    return down_pose * transl(0, 0, -z)

def pick_and_place_cube(pose_pick_up, pose_pick_down, pose_place_up, pose_place_down, cube, i):
    r_robot.MoveJ(t_pickpose)
    r_robot.MoveJ(pose_pick_up)
    r_robot.MoveL(pose_pick_down)
    tl_tool.AttachClosest()
    r_robot.MoveL(pose_pick_up)
    r_robot.MoveJ(t_pickpose)
    if i%4 == 1:
        r_robot.MoveJ(t_pickpose2)
    r_robot.MoveJ(pose_place_up)
    r_robot.MoveL(pose_place_down)
    tl_tool.DetachAll()
    cube.setParentStatic(f_place)
    r_robot.MoveJ(t_pickpose)

#Berechnet den Punkt wo der Klotz abgelegt werden muss
def calcP1(i):
    h = 7.75
    l = 117.7
    b = 23.1
    rot = 0
    if i%4 == 0:
        x = b/2
        y = l/2
    elif i%4 == 1:
        x = l - b/2
        y = l/2
    elif i%4 == 2:
        x = l /2
        y = b/2
        rot = pi/2
    elif i%4 == 3:
        x = l / 2
        y = l - b / 2
        rot = pi/2

    z = (int(i/2) + 1) * h
    return [x, y, z, rot]

#Berechnet den Punkt wo der Klotz geholt werden muss
def calcP2(i):
    if i%4 == 0:
        x = 20
        y = 65
    elif i%4 == 1:
        x = 50
        y = 65
    elif i%4 == 2:
        x = 20
        y = 190
    elif i%4 == 3:
        x = 50
        y = 190

    x += (int(i / 4)) * 60
    z = 7.75
    r = 0
    return[x, y, z, r]

#################################
r_robot.setJoints([0, 0, 90, 0, 0, 0])
r_robot.setPoseFrame(f_world)
r_robot.setSpeed(1000, 200, 1500, 150) # (1000, 200, 1500, 150) (125, 25, 325, 37)
#################################
tic()

for i in range(len(blocks)):
    p1 = calcP1(i) #Punkt wo der Block abgelegt werden soll
    p2 = calcP2(i) #Punkt wo der Block geholt werden soll
    pose_pick_down = pick_pose_down(p2[0], p2[1], p2[2], p2[3])
    pose_pick_up = pose_up(pose_pick_down, 20)
    pose_place_down = place_pose_down(p1[0], p1[1], p1[2], p1[3])
    pose_place_up = pose_up(pose_place_down, 5)
    pick_and_place_cube(pose_pick_up, pose_pick_down, pose_place_up, pose_place_down, blocks[i], i)

time = toc()
mbox(str(round(time, 3))+'s')
