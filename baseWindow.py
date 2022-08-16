from maya import cmds

class Window(object):
    def __init__(self, name):

        if cmds.window(name, query=True, exists=True): #check if window is open, if it is close it so that you open it again later
            cmds.deleteUI(name)

        cmds.window(name)
        self.buildUI()
        cmds.showWindow()
    
    def buildUI(self):
            print "no UI is defined"
