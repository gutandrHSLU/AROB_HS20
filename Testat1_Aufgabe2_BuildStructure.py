from robolink import *
from robodk import *
RDK = Robolink()

r_robot = RDK.Item('Staubli TX40')
tl_tool = RDK.Item('LWS_VakuumGreifer_11')

f_world = RDK.Item('world', ITEM_TYPE_FRAME)
f_pick = RDK.Item('blocks', ITEM_TYPE_FRAME)
f_place = RDK.Item('tower', ITEM_TYPE_FRAME)
t_home = RDK.Item('home')
t_pickpose = RDK.Item('zwischenstopp')

blocks = f_pick.Childs()

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
    r_robot.MoveJ(pose_place_up)
    r_robot.MoveL(pose_place_down)
    tl_tool.DetachAll()
    cube.setParentStatic(f_place)
    r_robot.MoveJ(t_pickpose)

#Berechnet den Punkt wo der Klotz abgelegt werden muss
def calcP1(i):
    x = 0
    y = 0
    z = (i+1) * 7.75
    rot = i * (2*pi)/30
    return [x, y, z, rot]

#Berechnet den Punkt wo der Klotz geholt werden muss
def calcP2(i):
    if i%2 == 0:
        x = 20
        y = 65
    elif i%2 == 1:
        x = 20
        y = 190

    x += (int(i / 2)) * 30
    z = 7.75
    r = 0
    return[x, y, z, r]

#################################
r_robot.setJoints([0, 0, 90, 0, 0, 0])
r_robot.setPoseFrame(f_world)
r_robot.setSpeed(1000, 200, 1500, 150) # (1000, 200, 1500, 150) (125, 25, 325, 37)
#################################

for i in range(len(blocks)):
    p1 = calcP1(i) #Punkt wo der Block abgelegt werden soll
    p2 = calcP2(i) #Punkt wo der Block geholt werden soll
    pose_pick_down = pick_pose_down(p2[0], p2[1], p2[2], p2[3])
    pose_pick_up = pose_up(pose_pick_down, 20)
    pose_place_down = place_pose_down(p1[0], p1[1], p1[2], p1[3])
    pose_place_up = pose_up(pose_place_down, 5)
    pick_and_place_cube(pose_pick_up, pose_pick_down, pose_place_up, pose_place_down, blocks[i], i)
r_robot.setJoints([0, 0, 90, 0, 0, 0])
