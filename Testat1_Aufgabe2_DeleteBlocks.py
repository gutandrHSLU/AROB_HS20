from robolink import *    # RoboDK API
from robodk import *      # Robot toolbox
RDK = Robolink()

f_blocks = RDK.Item("blocks", ITEM_TYPE_FRAME)
f_tower = RDK.Item("tower", ITEM_TYPE_FRAME)
r_robot = RDK.Item('Staubli TX40')
r_robot.setJoints([0, 0, 90, 0, 0, 0])


def cleanup_blocks(parent):
    """Deletes all child items whose name starts with \"ball\", from the provided list of parent items."""
    for item in parent.Childs():
        item.Delete()

cleanup_blocks(f_blocks)
cleanup_blocks(f_tower)
