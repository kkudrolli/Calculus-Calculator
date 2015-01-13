#Kais Kudrolli, kkudroll
#15-112, Section C, Term Project
#This file creates a help screen and a prefix notation tutorial

from Tkinter import *
import Input as inpt
import tkMessageBox
import tkSimpleDialog

def showHelpBox():
    #shows a help box that gives user instructions about the calculator
    message = """
    Click on the function buttons to create a function.
    To enter a constant, click the Constant button and enter a number in the prompt box.
    The Graph button graphs your function.
    The Differentiate button graphs the derivative of your function.
    The Integrate button graphs the integral of your function.
    The Symbolic Derivative button displays the symbolic derivative of your function.
    The Clear button resets your function and the graph.
    The Change Domain button lets you set the minimum and maximum x-values of the graph.
    None indicates that another argument is required, you cannot graph or get the symbolic
    derivative until there are no more Nones in your function.
    The buttons will not function unless there is a valid function entered.
    Remember that the binary functions (+,-,*,/,^) use prefix notation.
    """
    title = "Help"
    tkMessageBox.showinfo(title, message)

def createPlus(upperCanvas,lineWidth):
    #creates a plus sign
    lengthOfSpoke = upperCanvas.data.width/10.0
    cx = upperCanvas.data.width/4.0
    cy = upperCanvas.data.height/4.0
    #create vertical line
    upperCanvas.create_line(cx, cy-lengthOfSpoke,cx,cy+lengthOfSpoke,
                            fill="orange", width=lineWidth)
    #create horizontal line
    upperCanvas.create_line(cx-lengthOfSpoke,cy, cx+lengthOfSpoke,cy,
                            fill="orange", width=lineWidth)
    
def createMinus(upperCanvas,lineWidth):
    #creates a minus sign
    lengthOfSpoke = upperCanvas.data.width/10.0
    cx = 3.0*upperCanvas.data.width/4.0
    cy = upperCanvas.data.height/4.0
    #create horizontal line
    upperCanvas.create_line(cx-lengthOfSpoke,cy, cx+lengthOfSpoke,cy,
                            fill="orange", width=lineWidth)
    
def createX(upperCanvas,lineWidth):
    #creates a multiplication sign
    lengthOfSpoke = upperCanvas.data.width/10.0
    cx = upperCanvas.data.width/4.0
    cy = 3.0*upperCanvas.data.height/4.0
    L = lengthOfSpoke/(2**0.5)
    upperCanvas.create_line(cx-L,cy-L,cx+L,cy+L,fill="orange",width=lineWidth)
    upperCanvas.create_line(cx-L,cy+L,cx+L,cy-L,fill="orange",width=lineWidth)

def createCircle(upperCanvas,lineWidth,cx,cy):
    #draws a circle
    r = lineWidth
    upperCanvas.create_oval(cx-r,cy-r,cx+r,cy+r,fill="orange")
    
def createObelus(upperCanvas,lineWidth):
    #creates a division sign
    lengthOfSpoke = upperCanvas.data.width/10.0
    cx = 3.0*upperCanvas.data.width/4.0
    cy = 3.0*upperCanvas.data.height/4.0
    offset = upperCanvas.data.width/20.0
    #create horizontal line
    upperCanvas.create_line(cx-lengthOfSpoke,cy, cx+lengthOfSpoke,cy,
                            fill="orange", width=lineWidth)
    #create circles above and below line
    createCircle(upperCanvas,lineWidth,cx,cy-offset)
    createCircle(upperCanvas,lineWidth,cx,cy+offset)

def createBackground(upperCanvas, lowerCanvas):
    #creates the backgound image
    
    #sets backgorund color to black
    upperCanvas.create_rectangle(0,0,upperCanvas.data.width,
                                 upperCanvas.data.height,fill = "black")
    lowerCanvas.create_rectangle(0,0,lowerCanvas.data.width,
                                 lowerCanvas.data.height,fill = "black")
    #creates four shapes in the background
    lineWidth = 10.0
    createPlus(upperCanvas,lineWidth)
    createMinus(upperCanvas,lineWidth)
    createX(upperCanvas,lineWidth)
    createObelus(upperCanvas,lineWidth)
    
def removePreviousButtons(lowerCanvas):
    #removes all current buttons from canvas
    lowerCanvas.delete(ALL)
    for button in lowerCanvas.data.buttons:
        button.destroy()

def welcomeScreen(upperCanvas,lowerCanvas,root):
    #displays initial welcome screen
    welcomeString = """
    Welcome to Kais's Derivative
    and Integral Calculator!
    """
    
    #information for creating text
    cx = upperCanvas.data.width/2.0
    cy = upperCanvas.data.height/3.0
    aFont = "Arial 18 bold"
    
    createBackground(upperCanvas, lowerCanvas)
    
    upperCanvas.create_text(cx,cy,text = welcomeString, font = aFont,
                            anchor = "n", fill = "blue")
    
    def firstScreenWrapper():
        #wrapper function to call next screen
        firstScreen(upperCanvas,lowerCanvas,root)
    
    beginButton = Button(lowerCanvas,text = "Begin", command =
                           firstScreenWrapper,bg="orange",fg="blue",
                           font="Arial 12 bold",activebackground = "blue",
                           activeforeground ="orange")
    beginButton.pack()
    #adds the button to a button list in the canvas
    lowerCanvas.data.buttons.append(beginButton)
    
def createFirstScreenMessages():
    #creates messages for first tutorial screen
    header = "Prefix Notation Tutorial"
    introMsg = """
    In this calculator, prefix notation is used
    with binary functions (with two operands)
    in place of normal infix notation.
    """
    diagramText = """
    a + b (infix) = + a b (prefix)
    """
    return [header,introMsg,diagramText]

def firstScreen(upperCanvas,lowerCanvas,root):
    #displays the first screen of the tutorial
    
    #remove everything from the canvases
    removePreviousButtons(lowerCanvas)
    upperCanvas.delete(ALL)
    
    messageList = createFirstScreenMessages()
    
    #define text information
    aFont = "Arial 18 bold"
    bFont = "Arial 12 italic bold"
    cFont = "Arial 16 bold"
    color = "blue"
    cx = upperCanvas.data.width/2.0
    cyHeader = upperCanvas.data.height/10.0
    cyMsg = upperCanvas.data.height/5.0
    cyDiagram = (2.0)*upperCanvas.data.height/5.0
    anchor = "n"
    
    createBackground(upperCanvas, lowerCanvas)
    
    #create the texts
    upperCanvas.create_text(cx,cyHeader,text=messageList[0],font=aFont,
                            anchor=anchor,fill=color)
    upperCanvas.create_text(cx,cyMsg,text=messageList[1],font =bFont,
                            anchor=anchor,fill=color)
    upperCanvas.create_text(cx,cyDiagram,text=messageList[2],font= cFont,
                            anchor=anchor,fill=color)
    
    #wrapper for secondScreen 
    def secondScreenWrapper(): secondScreen(upperCanvas,lowerCanvas,root)
    
    nextButton = Button(lowerCanvas,text = "Next",command=secondScreenWrapper,
                        bg="orange",fg="blue",font="Arial 12 bold",
                        activebackground = "blue",activeforeground ="orange")
    nextButton.pack()

    lowerCanvas.data.buttons.append(nextButton)

def secondScreen(upperCanvas,lowerCanvas,root):
    #displays the second screen of the tutorial
    
    #removes everything from the canvases
    removePreviousButtons(lowerCanvas)
    upperCanvas.delete(ALL)
    
    msg = """
    For example, instead of entering "a" plus "b,"
    you must choose the "a+b" function and enter
    some arguments "a" and "b".
    """
    msg2 = """
    As a further example: you can represent "a*b"
    as "*ab" and "a/b" as "/ab".
    """
    
    #define text information
    aFont = "Arial 12 italic bold"
    color = "blue"
    cx = upperCanvas.data.width/2.0
    cyMsg = upperCanvas.data.height/5.0
    cyMsg2 = 2.0*upperCanvas.data.height/5.0
    anchor = "n"
    
    createBackground(upperCanvas, lowerCanvas)
    
    upperCanvas.create_text(cx,cyMsg,text = msg, font = aFont, anchor = anchor,
                            fill = color)
    upperCanvas.create_text(cx,cyMsg2,text = msg2, font = aFont, anchor = anchor,
                            fill = color, width = upperCanvas.data.width)
    
    #wrapper for thirdScreen
    def thirdScreenWrapper(): thirdScreen(upperCanvas,lowerCanvas,root)
    nextButton = Button(lowerCanvas,text = "Next", command =
                           thirdScreenWrapper,bg="orange",fg="blue",
                           font="Arial 12 bold",activebackground = "blue",
                           activeforeground ="orange")
    nextButton.pack()
    lowerCanvas.data.buttons.append(nextButton)
    
    #button to return to previous screen
    def firstScreenWrapper(): firstScreen(upperCanvas,lowerCanvas,root)
    backButton = Button(lowerCanvas,text = "Back", command =
                           firstScreenWrapper,bg="orange",fg="blue",
                           font="Arial 12 bold",activebackground = "blue",
                           activeforeground ="orange")
    backButton.pack()
    lowerCanvas.data.buttons.append(backButton)

def runCalculator(root):
    #launches the calculator part of the program
    
    #closes the current screen 
    root.withdraw()
    root.destroy()
    #launches the calculator
    inpt.run()

def buttonPressedFinish(lowerCanvas,root):
    #called when the Finish button is pressed
    
    #loop checks if all problems have been solved
    for elem in lowerCanvas.data.finished:
        if(elem == False):
            #alerts the user if all the problems have not been solved
            message = "You must complete the exercises before moving on!"
            title = "Exercise(s) Incomplete"
            tkMessageBox.showerror(title, message)
            return
    else:
        #runs the calculator if all the problems have been solved
        runCalculator(root)
        
def buttonPressedProblem1(lowerCanvas):
    #shows the first problem
    problem = ProblemBox(lowerCanvas, "a-b =", "-ab")
    #sets the complete status of the problem
    lowerCanvas.data.finished[0] = problem.complete

def buttonPressedProblem2(lowerCanvas):
    #shows the second problem
    problem = ProblemBox(lowerCanvas, "(no parentheses in answer): (a+b)*(c+d) =", "*+ab+cd")
    lowerCanvas.data.finished[1] = problem.complete

def buttonPressedProblem3(lowerCanvas):
    #shows the third problem
    problem = ProblemBox(lowerCanvas, "a/b =", "/ab")
    lowerCanvas.data.finished[2] = problem.complete

def createButtonLists(upperCanvas,lowerCanvas,root):
    #return lists of the button labels and button pressed functions
    
    #create wrapper functions
    def buttonPressedProblem1Wrapper():
        return buttonPressedProblem1(lowerCanvas)
    def buttonPressedProblem1Wrapper2():
        return buttonPressedProblem2(lowerCanvas)
    def buttonPressedProblemWrapper3():
        return buttonPressedProblem3(lowerCanvas)
    def buttonPressedFinishWrapper():
        return buttonPressedFinish(lowerCanvas,root)
    def secondScreenWrapper():
        secondScreen(upperCanvas,lowerCanvas,root)
    
    buttonLabelList = ["Problem 1","Problem 2","Problem 3", "Finish", "Back"]
    buttonPressedList = [buttonPressedProblem1Wrapper,
                         buttonPressedProblem1Wrapper2,
                         buttonPressedProblemWrapper3,
                         buttonPressedFinishWrapper,
                         secondScreenWrapper]
    return (buttonLabelList,buttonPressedList)

def makeThirdScreenButton(lowerCanvas, buttonLabel, command):
    #makes a button for the third tutorial screen
    button = Button(lowerCanvas,text = buttonLabel, command = command,
                    bg="orange",fg="blue",font="Arial 12 bold",
                    activebackground = "blue",activeforeground ="orange")
    button.pack()
    button.grid(sticky=W+E)
    lowerCanvas.data.buttons.append(button)
    

def thirdScreen(upperCanvas,lowerCanvas,root):
    #displays the third screen of the tutorial
    
    #removes all previous elements
    removePreviousButtons(lowerCanvas)
    upperCanvas.delete(ALL)
    
    msg = """
    To ensure you understand prefix notation
    before you move onto the calculator, do
    these three problems.
    """
    
    #text information
    aFont = "Arial 12 italic bold"
    color = "blue"
    cx = upperCanvas.data.width/2.0
    cy = upperCanvas.data.height/3.0
    anchor = "n"
    
    createBackground(upperCanvas, lowerCanvas)
    
    upperCanvas.create_text(cx,cy,text = msg, font = aFont,
                            anchor = anchor, fill = color)
    
    (buttonLabelList, buttonPressedList) = createButtonLists(upperCanvas,
                                                             lowerCanvas,root)
    
    #create buttons
    for i in xrange(len(buttonLabelList)):
        makeThirdScreenButton(lowerCanvas,buttonLabelList[i],
                              buttonPressedList[i])
    
def keyPressedCheat(root,event):
    #handles pressed keys
    if(event.char == "q"):
        #if cheat code entered, skips tutorial
        runCalculator(root)

def formatRoot(root,initialPositionX, initialPositionY):
    #sets up the root window and calls the mainloop
    root.bind("<Key>", lambda event: keyPressedCheat(root, event))
    #set the initial screen position
    root.geometry('+' + str(initialPositionX) + '+' + str(initialPositionY))
    root.configure(background = 'black')
    root.title("Derivative and Integral Calculator")
    root.mainloop()
    
def tutorialRun():
    root = Tk()
    #sets initial dimensions and screen position
    width, height = 500, 300
    initialPositionX, initialPositionY = 400, 250
    #create canvases
    upperCanvas = Canvas(root, width = 500, height = 300)
    lowerCanvas = Canvas(root, width = 500, height = 300)
    upperCanvas.pack()
    lowerCanvas.pack()
    root.resizable(width=0, height=0)
    #create Structs to hold canvas data
    class Struct: pass
    upperCanvas.data = Struct()
    upperCanvas.data.width = width
    upperCanvas.data.height = height
    class Struct: pass
    lowerCanvas.data = Struct()
    lowerCanvas.data.buttons = []
    lowerCanvas.data.finished = [False,False,False]
    lowerCanvas.data.width = width
    lowerCanvas.data.height = height
    #launch the welcome screen
    welcomeScreen(upperCanvas,lowerCanvas,root)
    formatRoot(root,initialPositionX, initialPositionY)

class ProblemBox(tkSimpleDialog.Dialog):
    #class that creates a box containing a tutorial problem
    
    def __init__(self, master,text, answer):
        #constructor method
        self.master = master
        self.entry = None
        self.text = text
        self.answer = answer
        self.complete = False
        self.value = None
        #call super class constructor
        tkSimpleDialog.Dialog.__init__(self, master)
        
    def body(self, master):
        #makes body of the problem box
        Label(master, text=self.text).grid(row=0)
        Label(master).grid(row=1)
        self.entry = Entry(master)
        self.entry.grid(row=1, column=1)
        return self.entry
    
    def apply(self):
        value = str(self.entry.get())
        self.value = value
        #checks if the user input response matches answer
        if(self.value == self.answer):
            #the user was correct
            self.complete = True
            message = "Your answer was correct!"
            title = "Correct"
            tkMessageBox.showinfo(title, message)
        else:
            #tells the user the response was incorrect
            message = "Your answer was incorrect!"
            title = "Incorrect"
            tkMessageBox.showerror(title, message)
    
    
