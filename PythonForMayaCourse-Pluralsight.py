#Python for maya
#python 3 is backwards incompatible (on purpose). Maya uses 2.7. We have to avoid using deprecated features.
# print command
print "Hello, Dhruv"

# we're going to focus on Command API, not the openMaya API. (Python can use both)
# C++ can only use openMaya
#pluralsight's course will only create scripts, not plugins

from maya import cmds
cmds.polyCube(w=15, h=15, d=15)
cmds.select(clear=true)

cmds.select('pCube1', replace=true) #as opposed to MEL in Python names comes first, flags second.
cmds.delete()

#string, ints, floats, bool, None (NoneType).

#lists
myList = [name, age, lying]
myList[0]=name #afects 1st one

#Tuple. Lists but cannot be changed once created, as opposed to lists.
myTuple = (name, 25.4, True)

#Dictionaries. Like lists, but their indexes are words instead of numbers.
myDict = {"name":name. "age":age}
myDict['age'] #will throw out the variable age

#parenting
from maya import cmds
cube = cmds.polyCube()
circle = cmds.circle()
cmds.parent(cube[0], circle[0])

#Nodes in Maya
#transform node (translation, rotation, scale)
#constructor node (depth, widht, height, subdivs, etc)

#For Loop
from maya import cmds
objectList = [cmds.polyCube, cmds.polySphere, cmds.polyCone]

for obj in objectList
	obj()

#While Loop
i = 0
while i<20:
	print i
	i = i + 1

#conditionals: if/else statements
from maya import cmds
numObjects = 5
mode = 'Cube'

import random

for n in range(numObjects):
		if mode == 'Cube':
			obj = cmds.polyCube()
		elif mode == 'Sphere':
			obj = cmds.polySphere()
		elif mode == 'Cone':
			obj = cmds.polyCone()
		else
			cmds.error("I don't know what to create") #throws an error

#querying and setting attributes
from maya import cmds
import random

print cmds.getAttr('pSphere1.translate')
print cmds.setAttr('pSphere1.translateX', 15) #changes attribute to 15


obj = cmds.polyCone()
cmds.setAttr(obj[0]+'.translateX', random.randint(0, 20))
cmds.setAttr(obj[0]+'.translateY', random.randint(0, 20))
cmds.setAttr(obj[0]+'.translateZ', random.randint(0, 20))

#functions
def createObjects(mode, numObjects):
	for nin range(numObjects):
		if mode == 'Cube':
			obj = cmds.polyCube()
		elif mode == 'Sphere':
			obj = cmds.polySphere()
		elif mode == 'Cone':
			obj = cmds.polyCone()
		else
			cmds.error("I don't know what to create") 

		objList.append(obj[0])

	return objList

def randomize(objList, minValue=0, maxValue=50):
	if objList is None:		#getting the Selection
		objList = cmds.ls(selection=True)

	for obj in objList
		cmds.setAttr(obj+'.tx', randomize.randint(minValue, maxValue))
		cmds.setAttr(obj+'.ty', randomize.randint(minValue, maxValue))
		cmds.setAttr(obj+'.tz', randomize.randint(minValue, maxValue))

objList = createObjects('Cube', 5)
randomize(objList)


#string formatting
"here goes a string %s" % (name)
"here goes a string %s and here goes another %s, and here goes the number %s" % (name, "STRING", 2)
"here goes a string {} and here goes another {}, and here goes the number {}".format(name, "STRING", 2)
"here goes a string {1} and here goes a number {2}, and here goes the name {0}".format(name, "STRING", 2)
"here goes a name {name} and here goes country {country}, and here goes the number {number}".format(name=name, country="STRING", number=2)

#scopes
myGlobal='Global Value'

def Enclosing():
	myEnclosing = 'Enclosing Value'
	def LocalFunction():
		myLocal = 'Local Value'

	LocalFunction()

Enclosing()
print object

#sharing
#file>save script (and save your "randomizer" as "randomizer.py" in maya/scripts)
import randomizer
#now you can use randomizer.randomize() to call the randomize function defined in your code
#you can reload the sript bu writing reload(randomizer). REMEMBER TO DISABLE THIS WHEN YOU SHARE IT WITH OTHERS 'CAUSE IT CAN BE DANGEROUS!
#to add documentation use three quotes """like this""" so that it can be used as help by Maya
#remember to add comments to reference it later

#User Interface
#There exists a UI interface called QT (PyQT) that is used in many other apps and industries, but we will not be using that one.

def showWindow():
	name = "RanomizerWindow"
	if cmds.window(name, query=True, exists=True): #check if window is open, if it is close it so that you open it again later
		cmds.deleteUI(name)

	cmds.window(name)
	cmds.showWindow()

	#radios, numbers, buttons

#CODE FROM THIS LESSON

from maya import cmds
import random


def createObjects(mode, numObjects = 5):
	"""this creates objects. Supports Cubes, Spheres, Cylinders, and Cones. """
	objList = []

	for n in range(numObjects):
		if mode == 'Cube':
			obj = cmds.polyCube()
		elif mode == 'Sphere':
			obj = cmds.polySphere()
		elif mode == 'Cylinder':
			obj = cmds.polyCylinder()
		elif mode == 'Cone':
			obj = cmds.polyCone()
		else: cmds.error("I don't know what to create") 

		objList.append(obj[0])

	cmds.select(objList)

def randomize(objList=None, minValue=0, maxValue=10, axes='xyz', mode= 'Absolute'):
	if objList is None:		#getting the Selection
		objList = cmds.ls(selection=True)

	for obj in objList:
		for axis in axes:
			current = 0
			if mode == 'Relative':
				current = cmds.getAttr(obj+'.t%s' % axis)
			val = current + random.uniform(minValue, maxValue)
			cmds.setAttr(obj+'.t%s' % axis, val)
		

#objList = createObjects('Cube', 5)
#randomize(objList)

def showWindow():
	name = "RanomizerWindow"
	if cmds.window(name, query=True, exists=True): #check if window is open, if it is close it so that you open it again later
		cmds.deleteUI(name)

	cmds.window(name)
	cmds.showWindow()

	column = cmds.columnLayout()
	cmds.frameLayout(label ="Choose an object type")

	cmds.columnLayout()
	cmds.radioCollection("objectCreationType")
	cmds.radioButton(label="Sphere")
	cmds.radioButton(label="Cube", select=True)
	cmds.radioButton(label="Cone")

	cmds.intField("numObjects", value=3)
	
	cmds.setParent(column)
	frame = cmds.frameLayout("Choose your max ranges")

	cmds.gridLayout(numberOfColumns=2, cellWidth=100)

	for axis in 'xyz':
		cmds.text(label='%s axis' % axis)
		cmds.floatField('%sAxisField' % axis, value=random.uniform(0,10))
	
	cmds.setParent(frame)
	cmds.rowLayout(numberOfColumns=2)

	cmds.radioCollection("randomMode")
	cmds.radioButton(label='Absolute', select=True)
	cmds.radioButton(label='Relative')

	cmds.setParent(column)
	cmds.rowLayout(numberOfColumns=2)
	cmds.button(label="Create", command=onCreateClick)
	cmds.button(label="Randomize", command=onRandomClick)

def onCreateClick(*args): #*args takes any arguments passed to this function and stores it in that word args, making sure the program doesn't stop
	radio = cmds.radioCollection("objectCreationType", query=True, select=True)
	mode = cmds.radioButton(radio, query=True, label=True)

	numObjects = cmds.intField("numObjects", query=True, value=True)
	
	createObjects(mode, numObjects)
	onRandomClick()

def onRandomClick(*args): 
	radio = cmds.radioCollection("randomMode", query=True, select=True)
	mode = cmds.radioButton(radio, query=True, label=True)

	for axis in 'xyz':
		val = cmds.floatField("%sAxisField" % axis, query=True, value=True)
		randomize(minValue=val*-1, maxValue=val, mode=mode, axes=axis)
	
	
#Classes
#capital letter in class name denotes it's a class
#a method is a function inside a class, it takes the word self as a first argument
#self lets an instance refer to its methids and data and is unique in each instance of a class
#magic mehods (implicit methods in all classes)
#	__init__ : is called when an instance of a class is created
#	__bool__ or __nonzero__: checks if the object evaluates as true or false
#	__len__: gives the length of the object if it is a list or something similar
#	__str__: creates a string representation of the object
#Super: Super function lets a class call functionality from its parent (class), it also handles classes with multiple parents (classes), it's useful for overriding while using
#Example code:
class Human(object) :
    
    def __init__(self,name): #is called as soon as the object is initiated
        self.firstName = name.split()[0]
        self.lastName = name.split()[1]

    def greet(self):
        print "Hello! My name is %s" % self.firstName

    def sleep(self, length): 
        print "Z"+("z"*length)

class Canadian(Human):
    def __init__(self, name, city): #overriding original init from parent class
        super(Canadian, self).__init__(name) #this creates a temporary instance of the parent class and calls it's __init__ method, 
        self.city = city
    def greet(self):
        print "Hello, my name is %s. How are you, eh?" % self.name

bob = Canadian("Bob bobert", "Vancouver")
bob.greet()


#updated Randomizer code:

from maya import cmds
import random
import baseWindow


def createObjects(mode, numObjects = 5):
	"""this creates objects. Supports Cubes, Spheres, Cylinders, and Cones. """
	objList = []

	for n in range(numObjects):
		if mode == 'Cube':
			obj = cmds.polyCube()
		elif mode == 'Sphere':
			obj = cmds.polySphere()
		elif mode == 'Cylinder':
			obj = cmds.polyCylinder()
		elif mode == 'Cone':
			obj = cmds.polyCone()
		else: cmds.error("I don't know what to create") 

		objList.append(obj[0])

	cmds.select(objList)

def randomize(objList=None, minValue=0, maxValue=10, axes='xyz', mode= 'Absolute'):
	if objList is None:		#getting the Selection
		objList = cmds.ls(selection=True)

	for obj in objList:
		for axis in axes:
			current = 0
			if mode == 'Relative':
				current = cmds.getAttr(obj+'.t%s' % axis)
			val = current + random.uniform(minValue, maxValue)
			cmds.setAttr(obj+'.t%s' % axis, val)
		

class RandomizerUI(baseWindow.Window):

	def __init__(self, name= 'Randomizer'):
		super(RandomizerUI, self).__init__(name)

	def buildUI(self):
		column = cmds.columnLayout()
		cmds.frameLayout(label ="Choose an object type")

		cmds.columnLayout()
		self.objType = cmds.radioCollection("objectCreationType")
		cmds.radioButton(label="Sphere")
		cmds.radioButton(label="Cube", select=True)
		cmds.radioButton(label="Cone")

		self.intField = cmds.intField("numObjects", value=3)
		
		cmds.setParent(column)
		frame = cmds.frameLayout("Choose your max ranges")

		cmds.gridLayout(numberOfColumns=2, cellWidth=100)

		for axis in 'xyz':
			cmds.text(label='%s axis' % axis)
			cmds.floatField('%sAxisField' % axis, value=random.uniform(0,10))
		
		cmds.setParent(frame)
		cmds.rowLayout(numberOfColumns=2)

		cmds.radioCollection("randomMode")
		cmds.radioButton(label='Absolute', select=True)
		cmds.radioButton(label='Relative')

		cmds.setParent(column)
		cmds.rowLayout(numberOfColumns=2)
		cmds.button(label="Create", command=self.onCreateClick)
		cmds.button(label="Randomize", command=self.onRandomClick)



	

	def onCreateClick(self, *args): #*args takes any arguments passed to this function and stores it in that word args, making sure the program doesn't stop
		radio = cmds.radioCollection(self.objType, query=True, select=True)
		mode = cmds.radioButton(radio, query=True, label=True)

		numObjects = cmds.intField(self.intField, query=True, value=True)
		
		createObjects(mode, numObjects)
		onRandomClick()

	def onRandomClick(self, *args): 
		radio = cmds.radioCollection("randomMode", query=True, select=True)
		mode = cmds.radioButton(radio, query=True, label=True)

		for axis in 'xyz':
			val = cmds.floatField("%sAxisField" % axis, query=True, value=True)
			randomize(minValue=val*-1, maxValue=val, mode=mode, axes=axis)
		
# def showWindow():
# 	name = "RanomizerWindow"
# 	if cmds.window(name, query=True, exists=True): #check if window is open, if it is close it so that you open it again later
# 		cmds.deleteUI(name)

# 	cmds.window(name)
# 	cmds.showWindow()
	
#Building a tool from scratch
#Design process
#1 Determine our user needs
#2 layout a rough skeleton of our code and logic
#3 implement the logic first
#4 build the UI

