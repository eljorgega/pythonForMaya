from maya import cmd
sfrom functools import partial

def align(nodes=None, axis='x', mode='mid'):
    #default nodes to selection if none are provided
    if not nodes:
        nodes = cmds.ls(sl=True)
    
    if not nodes:
        cmds.error('Nothing selected or provided')

    _nodes = []
    for node in nodes:
        if '.f[' in node:
            node = cmds.polyListComponentConversion(node, fromFace=True, toVertex=True)
        elif '.e[' in node:
            node = cmds.polyListComponentConversion(node, fromEdge=True, toVertex=True)

        cmds.select(node)
        node = cmds.ls(sl=True, fl=True)

        _nodes.extend(node)

    nodes = _nodes

    bboxes = {}
    if axis == 'x':
        start = 0
    elif axis == 'y':
        start = 1
    elif axis == 'z':
        start = 2
    else:
        cmds.error('Unknown Axis')

    minMode = mode == 'min'
    maxMode = mode == 'max'
    midMode = mode == 'mid'

    values = []

    # get the dimensions of our objects
    for node in nodes:
        if '.vtx[' in node:
            ws = cmds.xform(node, q=True, t=True, ws=True)
            minValue = midValue = maxValue = ws[start]
        else:
            bbox = cmds.exactWorldBoundingBox(node)

            minValue = bbox[start]
            maxValue = bbox[start+3]
            midValue = (maxValue+minValue)/2

        bboxes[node] = (minValue, midValue, maxValue)

        if minMode:
            values.append(minValue)
        elif maxMode:
            values.append(maxValue)
        else:
            values.append(midValue)

    #we calculate the alignment point
    if minMode:
        target=min(values)
    elif maxMode:
        target = max(values)
    else:
        target = sum(values)/len(values)
    
    print target

    #figure out the distance to the target
    for node in nodes:
        bbox = bboxes[node]
        minValue, midValue, maxValue = bbox

        ws = cmds.xform(node, query=True, translation=True, ws=True) #xform command gives back the transform values
        
        width = maxValue - minValue
        if minMode:
            distance = minValue - target
            ws[start] = (minValue-distance) + width/2
        elif maxMode:
            distance = target-maxValue
            ws[start] = (maxValue + distance) - width/2
        else:
            distance = target - midValue
            ws[start] = midValue + distance 

        #move the object to the target

        cmds.xform(node, translation=ws, ws=True)

class Aligner(object):

    def __init__(self):
        name = "Aligner"
        if cmds.window(name, query=True, exists=True):
            cmds.deleteUI(name)

        window = cmds.window(name)
        self.buildUI()
        cmds.showWindow()
        cmds.window(window, e=True, resizeToFitChildren=True)

    def buildUI(self):
        column = cmds.columnLayout()
        # Add radio buttons for axis
        cmds.frameLayout(label="Choose an axis")

        cmds.gridLayout(numberOfColumns=3, cellWidth=50)
        
        cmds.radioCollection()
        self.xAxis = cmds.radioButton(label='x', select=True)
        self.yAxis = cmds.radioButton(label='y')
        self.zAxis = cmds.radioButton(label='z')

        createIconButton('XAxis.png', command=partial(self.onOptionClick, self.xAxis))
        createIconButton('YAxis.png', command=partial(self.onOptionClick, self.yAxis))
        createIconButton('ZAxis.png', command=partial(self.onOptionClick, self.zAxis))
        
        # Add radio buttons for mode
        cmds.setParent(column)

        cmds.frameLayout(label="Choose where to align")

        cmds.gridLayout(numberOfColumns=3, cellWidth=50)

        cmds.radioCollection()
        self.minMode = cmds.radioButton(label='min')
        self.midMode = cmds.radioButton(label='mid', select=True)
        self.maxMode = cmds.radioButton(label='max')
       
        createIconButton('MinAxis.png', command=partial(self.onOptionClick, self.minMode))
        createIconButton('MidAxis.png', command=partial(self.onOptionClick, self.midMode))
        createIconButton('MaxAxis.png', command=partial(self.onOptionClick, self.maxMode))
        
        # Add apply button
        cmds.setParent(column)
        cmds.button(label='Align', command=self.onApplyClick, bgc=(0.2,0.5,0.9))

    def onOptionClick(self, opt):
        cmds.radioButton(opt, edit=True, select=True)

    def onApplyClick(self, *args):
        # get the axis
        if cmds.radioButton(self.xAxis, q=True, select=True):
            axis = 'x'
        elif cmds.radioButton(self.yAxis, q=True, select=True):
            axis = 'y'
        else:
            axis = 'z'

        # get the mode
        if cmds.radioButton(self.minMode, q=True, select=True):
            mode = 'min'
        elif cmds.radioButton(self.midMode, q=True, select=True):
            mode = 'mid'
        else:
            mode = 'max'

        # call the align function
        align(axis =  axis, mode = mode)

def getIcon(icon):
    import os
    scripts = os.path.dirname(__file__) #get 
    icons = os.path.join(scripts, 'icons')

    icon = os.path.join(icons, icon)
    return icon

def createIconButton(icon, command=None):
    if command:
        cmds.iconTextButton(image1=getIcon(icon), width=50, height=50, command=command)
    else:
        cmds.iconTextButton(image1=getIcon(icon), width=50, height=50)