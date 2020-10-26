from robolink import *
from robodk import *
from tkinter import *
import random
RDK = Robolink()

global numberOfBlocks
numberOfBlocks = 26 #Startwert welcher dann mit dem Fenster angepasst werden kann.

blocks = []


def RunProgram(numberOfBlocks):
    f_blocks = RDK.Item("blocks", ITEM_TYPE_FRAME)
    for i in range(1, numberOfBlocks+1):
        newBlock = RDK.AddFile(r'C:\Users\aanng\OneDrive - Hochschule Luzern\5.Semester\AROB\Aufgaben\Testat\block.IGS', f_blocks)
        newBlock.Recolor([1/numberOfBlocks*i, 0.5, 1-(1/numberOfBlocks*i)])
        if i%2:
            newBlock.setPose(transl(20 + (i-1)*15, 65, 7.75) * rotz(90*pi/180))
        else:
            newBlock.setPose(transl(20 + (i-2)*15, 190, 7.75) * rotz(90*pi/180))
        blocks.append(newBlock.setName("block" + str(i)))
    RDK.Finish()


# Set up default parameters
PROGRAM_NAME = "Test"     # Name of the program

# Generate the main window
root = Tk()
root.title("Program settings")

entry_speed = StringVar()
entry_speed.set(str(numberOfBlocks))

# Define a label and entry text for the weld speed
Label(root, text="Number of blocks").pack()
Entry(root, textvariable=entry_speed).pack()

# Add a button and default action to execute the current choice of the user
def ExecuteChoice():
    NUMBER_OF_BLOCKS = int(entry_speed.get())
    # Run the main program once all the global variables have been set
    RunProgram(NUMBER_OF_BLOCKS)

Button(root, text='Add blocks', command=ExecuteChoice).pack()

# Important to display the graphical user interface
root.mainloop()
