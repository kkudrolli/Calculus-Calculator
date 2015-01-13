#Kais Kudrolli, kkudroll
#15-112, Section C, Term Project
#This file handles the user input and creates the main user interface
#of the calculator

import matplotlib.pyplot as plt
from pylab import *
import Tkinter as tk
import tkSimpleDialog
import tkMessageBox
from Functions import *
from Graphing import *
import HelpScreens as hlp

def buttonPressedZoom(lowerCanvas):
    #called when zoom button is pressed
    box = ZoomBox(lowerCanvas)
    start = box.start
    end = box.end
    steps = box.steps
    #sets new domain
    if((start != None) and (end != None)):
        lowerCanvas.data.domain = linspace(start,end,steps,endpoint=True)
        plt.clf()
        buttonPressedGraph(lowerCanvas)

def buttonPressedSymbolDerivative(lowerCanvas):
    #called when the symbolic derivative button is pressed
    derivativeRootNode = FunctionNode(0, None)
    #gets the root node from ButtonFactory's functionNodeList
    functionRootNode = ButtonFactory.functionNodeList[0]
    
    if(functionRootNode.arg1 != None):
        #performs the symbolic derivatie if there is an argument
        arg1 = functionRootNode.arg1
        derivativeRootNode.arg1 = arg1.symbolicDerivative(derivativeRootNode)
        if(derivativeRootNode.arg1 != None):
            #prints the symbolic derivative to the canvas
            derivativeString = ("f'(x) = " +
            derivativeRootNode.arg1.trim(derivativeRootNode).__repr__())
            cx = lowerCanvas.data.width/2.0
            cy = (3.0)*lowerCanvas.data.height/4.0
            width = lowerCanvas.data.width
            margin = lowerCanvas.data.width/5.0
            lowerCanvas.create_text(cx,cy,text = derivativeString,
                                    width = width-margin,fill = "white")
    
def buttonPressedIntegral(canvas):
    #called when the integral button is pressed
    xVals = canvas.data.domain
    
    try:
        #integrate the function and graphs the integral
        (newDomain, yVals) = ButtonFactory.functionNodeList[0].integrate(xVals)
        gr = Graph(newDomain,yVals)
        gr.drawGraph("F(x)")
    except TypeError:
        #catches a type error
        pass

def buttonPressedDerivative(canvas):
    #called if the derivative button is pressed
    xVals = canvas.data.domain
    #differentiates the function numerically and graphs the derivative
    yVals = ButtonFactory.functionNodeList[0].differentiate(xVals)
    gr = Graph(xVals,yVals)
    gr.drawGraph("f'(x)")

def drawEmptyGraph():
    #draws an empty graph
    
    #draws the point (0,0) which is imperceptible, looks like an empty graph
    xVals = np.array([0])
    yVals = np.array([0])
    gr = Graph(xVals,yVals)
    gr.drawGraph("")

def buttonPressedClear(upperCanvas,lowerCanvas):
    #called if the clear button is pressed
    #clears the graph and the function
    rootNode = FunctionNode(0, None)
    #resets the fucntionNodeList in ButtonFactory to just the root node
    ButtonFactory.functionNodeList = [rootNode]
    #clears the text in the lower canvas
    lowerCanvas.delete(tk.ALL)
    createBackground(upperCanvas, lowerCanvas)
    #clears the plot figure
    plt.clf()
    drawEmptyGraph()
    
def buttonPressedGraph(canvas):
    #called if the graph button is pressed
    xVals = canvas.data.domain
    #evaluates the function on the given domain and graphs the points
    yVals = ButtonFactory.functionNodeList[0].eval(xVals)
    gr = Graph(xVals,yVals)
    gr.drawGraph("f(x)")
    
def buttonPressedHelp():
    #launches the help box
    hlp.showHelpBox()

def initButtonLabelList():
    #returns a list of button labels
    return ["x","a/b","sin(x)","cos(x)","tan(x)","arcsin(x)","arccos(x)",
            "arctan(x)","a^b","log(x)","ln(x)","a+b","a-b","a*b","constant"]

def createButton(canvas,text,command, row, col):
    #draws a button on the canvas, based on given inputs
    button = tk.Button(canvas,text=text, command=command,
                       bg="orange",fg="blue",font="Arial 12 bold",
                    activebackground = "blue",activeforeground ="orange")
    button.pack()
    button.grid(row = row, column = col, sticky=tk.W+tk.E)

def otherButtonLabelDictGenerator(upperCanvas,lowerCanvas):
    #creates  dictionary of buttonPresseds mapped to labels
    
    #create wrapper functions
    def buttonPressedGraphWrapper():
        buttonPressedGraph(lowerCanvas)
    
    def buttonPressedDerivativeWrapper():
        buttonPressedDerivative(lowerCanvas)
        
    def buttonPressedIntegralWrapper():
        buttonPressedIntegral(lowerCanvas)
    
    def buttonPressedClearWrapper():
        buttonPressedClear(upperCanvas,lowerCanvas)
        
    def buttonPressedSymbolDerivativeWrapper():
        buttonPressedSymbolDerivative(lowerCanvas)
    
    def buttonPressedZoomWrapper():
        buttonPressedZoom(lowerCanvas)
        
    return {"Graph":buttonPressedGraphWrapper,
                            "Differentiate":buttonPressedDerivativeWrapper,
                            "Integrate":buttonPressedIntegralWrapper,
                            "Symbolic Derivative":
                                buttonPressedSymbolDerivativeWrapper,
                            "Help": buttonPressedHelp,
                            "Clear": buttonPressedClearWrapper,
                            "Change Domain": buttonPressedZoomWrapper}

def createBackground(upperCanvas, lowerCanvas):
    #creates the backgound image
    
    #sets background color to black
    upperCanvas.create_rectangle(0,0,upperCanvas.data.width,
                                 upperCanvas.data.height,fill = "black")
    lowerCanvas.create_rectangle(0,0,lowerCanvas.data.width,
                                 lowerCanvas.data.height,fill = "black")
    
def init(canvas,lowerCanvas,buttonFrame): 
    #initializes the main calculator screen
    
    createBackground(canvas, lowerCanvas)
    
    buttonLabelList = initButtonLabelList()
    rows = 5
    cols = 5
    #loop creates buttons for all the labels in the buttonLabelList
    for i in xrange(len(buttonLabelList)):
        row = i % rows
        col = i / cols
        button = ButtonFactory()
        ButtonFactory.makeButton(canvas, buttonFrame,lowerCanvas,
                                 buttonLabelList[i],row,col)
    
    otherButtonLabelDict = otherButtonLabelDictGenerator(canvas,lowerCanvas)
    counter = 0
    
    #create buttons for the functionalities
    for key in otherButtonLabelDict.keys():
        row = counter % rows
        col = 3 + (counter / cols)
        text = key
        command = otherButtonLabelDict[key]
        createButton(buttonFrame,text,command,row,col)
        counter += 1
    #align the buttons to the left
    buttonFrame.pack(side=tk.LEFT)
    
    #show help box initially
    buttonPressedHelp()

def confirmClose(root):
    #confirms that the user wants to exit the program
    message = "Are you sure you would like to quit?"
    title = "Confirm Quit"
    response = tkMessageBox.askquestion(title, message)
    if(str(response) == "yes"):
        plt.close()
        root.destroy()

def formatRoot(root,initialPositionX, initialPositionY):
    #sets up root window and calls the main loop
    def confirmCloseWrapper():
        confirmClose(root)
    #when the X in the corner is pressed, a fucntion is called to confirm
    #closing the window
    root.protocol('WM_DELETE_WINDOW', confirmCloseWrapper)
    #makes window not resizable
    root.resizable(width=0, height=0)
    #sets the initial position of the window
    root.geometry('+' + str(initialPositionX) + '+' + str(initialPositionY))
    root.title("Derivative and Integral Calculator")
    root.mainloop()

def initCanvasData(upperCanvas,lowerCanvas,width,height):
    #initiates the data in the canvas Structs
    upperCanvas.data.width = width
    upperCanvas.data.height = height
    lowerCanvas.data.width = width
    lowerCanvas.data.height = height
    lowerCanvas.data.domain = linspace(0, 2*np.pi, 256,endpoint=True)
    
def run():
    # create the root and the canvases
    root = tk.Tk()
    width = 500
    height = 200
    initialPositionX = 100
    initialPositionY = 180
    upperCanvas = tk.Canvas(root,width = 500, height = 500)
    upperCanvas.pack()
    lowerCanvas = tk.Canvas(root,width = 500, height = 200)
    lowerCanvas.pack()
    
    #sets up frame for buttons
    buttonFrame = tk.Frame(upperCanvas)
    
    # Set up canvas data and call init
    class StructUpper: pass
    upperCanvas.data = StructUpper()
    class StructLower: pass
    lowerCanvas.data = StructLower()
    
    initCanvasData(upperCanvas,lowerCanvas,width,height)
    init(upperCanvas,lowerCanvas,buttonFrame)
    formatRoot(root,initialPositionX, initialPositionY)

class ButtonFactory(object):
    #class variable, holds all the nodes in the tree
    rootNode = FunctionNode(0, None)
    functionNodeList = [rootNode] #initially has root node
    
    @classmethod
    def makeButton(cls, canvas, containerFrame, eqCanvas, text, row, col):
        #creates the button
        
        #dictionary of all the button labels with their corresponding functions
        buttonLabelDict = {"x":"x","a/b":"/","sin(x)":np.sin,"cos(x)":np.cos,
                           "tan(x)":np.tan,"arcsin(x)":np.arcsin,
                           "arccos(x)":np.arccos,"arctan(x)":np.arctan,
                           "a^b":"^","log(x)":np.log10,"ln(x)":np.log,
                           "a+b":"+","a-b":"-","a*b":"*"}
        
        def areArgsLeft(node):
            #checks if there are open children at a node of the function tree
            unaryFunctions = [np.sin,np.cos,np.tan,np.arcsin,
                              np.arccos,np.arctan,np.log10,np.log]
            binaryFunctions = ["^","+","-","*","/"]
            
            #checks if the function is x or a constant (stored in a list)
            if((node.evalFunction=="x") or (type(node.evalFunction)==list)):
                return False
            #if its a unary function is its only child unfilled
            elif(((node.evalFunction in unaryFunctions) == True) and
                (node.arg1 != None)):
                return False
            #if its a binary function, checks if either child is unfilled
            elif(((node.evalFunction in binaryFunctions) == True) and
                (node.arg1 != None) and (node.arg2 != None)):
                return False
            else:
                return True
        
        def updateEquationText():
            #updates the text on the canvas displaying the function
            rootNode = ButtonFactory.functionNodeList[0]
            #gets the string representation of function
            equationString = ("f(x) = " +
                              ButtonFactory.functionNodeList[0].__repr__())
            #deletes the existing text and creates the new text
            eqCanvas.delete(tk.ALL)
            cx = eqCanvas.data.width/2.0
            cy = eqCanvas.data.height/4.0
            width = eqCanvas.data.width
            height = eqCanvas.data.height
            margin = eqCanvas.data.width/5.0
            createBackground(canvas, eqCanvas)
            eqCanvas.create_text(cx,cy,text=equationString,
                                 width = width-margin,fill = "white")
        
        def isIncomplete():
            #determines if function can take more arguments
            return True
            
        def buttonPressed():
            #called if a button is pressed
            
            #removes nodes from the node list until the last node in the list
            #has available children
            for node in ButtonFactory.functionNodeList[::-1]:
                if(areArgsLeft(node) == True):
                    break
                else:
                    ButtonFactory.functionNodeList.remove(node)
            #catches index error that occurs when no children are available
            #and a button is pressed
            try:        
                parent = ButtonFactory.functionNodeList[-1]
            except IndexError:
                return
            
            #prompts user to input constant if the constant button is pressed
            if(text == "constant"):
                argument = []
                child = FunctionNode(argument,parent)
                InputBox(canvas,argument)
            else: 
                child = FunctionNode(buttonLabelDict[text],parent)
            
            #sets the new node as a child of another node    
            if(parent.arg1 == None):
                parent.setArg1(child)
            else:
                parent.setArg2(child)
                
            #adds the new node to the node list
            if(isIncomplete() == True):
                ButtonFactory.functionNodeList.append(child)
                updateEquationText()
            
        #calls the super class' constructor     
        button = tk.Button(containerFrame, text=text, command=buttonPressed,
                           bg="orange",fg="blue",font="Arial 12 bold",
                    activebackground = "blue",activeforeground ="orange")
        #places the button a grid
        button.grid(row = row, column = col, sticky=tk.W+tk.E)
        
class InputBox(tkSimpleDialog.Dialog):
    #class that creates an input box
    
    def __init__(self, master, argument):
        #constructor method
        self.master = master
        self.argument = argument
        self.entry = None
        #calls super class init
        tkSimpleDialog.Dialog.__init__(self, master)
        
    def body(self, master):
        #creates body of box
        tk.Label(master, text="Constant:").grid(row=1)
        self.entry = tk.Entry(master)
        self.entry.grid(row=1, column=1)
        return self.entry
    
    def apply(self):
        #handles input given to the box
        try:
            #gets the value entered by the user and stores it
            entry = self.entry.get()
            value = float(entry)
            self.argument.append(value)
        except ValueError:
            #catches invalid input and makes the user re-input a value
            message = """
            Your input was invalid.
            Enter a decimal or integer.
            """
            title = "Invalid Input"
            response = tkMessageBox.showerror(title, message)
            #creates a new input box
            InputBox(self.master, self.argument)
    
class ZoomBox(tkSimpleDialog.Dialog):
    #class that creates a box for user to input the bounds of a new domain to zoom 
    
    def __init__(self, master):
        self.master = master
        self.entry1 = None
        self.entry2 = None
        self.start = None
        self.end = None
        self.steps = 600 #constant number of steps
        #call super class constructor
        tkSimpleDialog.Dialog.__init__(self, master)
        
    def body(self, master):
        #creates body of the box
        tk.Label(master, text="Enter new domain endpoints").grid(row=0)
        tk.Label(master, text="Start:").grid(row=1)
        tk.Label(master, text="End:").grid(row=2)
        self.entry1 = tk.Entry(master)
        self.entry2 = tk.Entry(master)
        self.entry1.grid(row=1, column=1)
        self.entry2.grid(row=2, column=1)
        return self.entry1
    
    def apply(self):
        #handles user input into box
        try:
            #gets the value entered by the user and stores it
            self.start = float(self.entry1.get())
            self.end = float(self.entry2.get())
        except ValueError:
            #catches invalid input and makes the user re-input a value
            message = """
            Your input was invalid.
            Enter decimals or integers.
            """
            title = "Invalid Input"
            response = tkMessageBox.showerror(title, message)
            #creates a new zoom box
            ZoomBox(self.master)
        #checks if the end is greater than the start
        if(self.start >= self.end):
            message = """
            Your end must be greater than your start.
            """
            title = "Invalid Input"
            response = tkMessageBox.showerror(title, message)
            #creates a new zoom box
            ZoomBox(self.master)
        

    
    
    