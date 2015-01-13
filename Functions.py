#Kais Kudrolli, kkudroll
#15-112, Section C, Term Project
#This file creates the functions and derivative functions
#It performs numerical evaluations of functions, derivatives, and integrals

from pylab import *
import math
import warnings

class FunctionNode(object):
    #class that creates a node of a function tree
    
    def __init__(self,evalFunction,parent):
        #constructor
        self.evalFunction = evalFunction
        self.parent = parent
        #children nodes
        self.arg1 = None
        self.arg2 = None
        
    def setArg1(self,functionNode):
        #sets arg1
        self.arg1 = functionNode
        
    def setArg2(self,functionNode):
        #sets arg2
        self.arg2 = functionNode    
        
    def binaryEval(self,domain):
        #evaluates a binary function over a given domain
        
        #recursive calls of eval
            evaluatedArg1 = self.arg1.eval(domain)
            evaluatedArg2 = self.arg2.eval(domain)
            operator = self.evalFunction
            #performs the desired operation with the two evaluated children
            if(operator == "+"):
                return evaluatedArg1 + evaluatedArg2
            elif(operator == "-"):
                return evaluatedArg1 - evaluatedArg2
            elif(operator == "*"):
                return evaluatedArg1 * evaluatedArg2
            elif((operator == "/")):
                #catches division by zero
                if(evaluatedArg2.any() == 0):
                    print "Division by zero encountered."
                else:
                    return evaluatedArg1 / evaluatedArg2
            elif(operator == "^"):
                return evaluatedArg1 ** evaluatedArg2
        
    def eval(self, domain):
        #evaluates a function on a given domain
        
        #ignores runtime warnings thrown by ln, log, arcsin, and arccos
        warnings.filterwarnings('ignore')
        
        #checks if the evalFunction is 0, i.e. it is the root node
        if((self.evalFunction == 0) and (self.arg1 != None)):
            #recursive call to eval
            return self.arg1.eval(domain)
        #the node is x
        if(self.evalFunction == "x"):
            #base case to recursion
            return domain
        #the node is a constant
        if((type(self.evalFunction) == list)):
            #recursive call to eval
            return np.array(self.evalFunction*len(domain))
        
        #the second child is empty, so it is a unary function
        if((self.arg1 != None) and (self.arg2 == None)):
            #recursive call of eval
            evaluatedArg = self.arg1.eval(domain)
            return self.evalFunction(evaluatedArg)
        #it is a binary function
        elif((self.arg1 != None) and (self.arg2 != None)):
            return self.binaryEval(domain)

    def differentiate(self,domain):
        #numerically differentiates a funtion on a given domain
        h = .00001 #defines an h
        xPlusH = domain + h
        #evaluates derivative with equation f(x+h)-f(x) / h
        if((self.eval(xPlusH) != None) or (self.eval(domain) != None)):    
            derivative = (self.eval(xPlusH) - self.eval(domain)) / h
            return derivative
    
    def integrate(self,domain):
        #integrates a function over a given domain
        
        #get dx by subtracting domain without first value from domain
        #without last value
        domainCopyUpper = domain.copy()
        domainCopyLower = domain.copy()
        domainCopyUpper = domainCopyUpper[1:]
        domainCopyLower = domainCopyLower[:-1]
        
        dx = domainCopyUpper - domainCopyLower
        #get midpoints for riemann sums
        midpoints = (domainCopyUpper + domainCopyLower)/2.0
        #get heights of rectangles
        yVals = self.eval(midpoints)
        if(yVals != None):
            rectangleAreas = dx*yVals
            integral = rectangleAreas.cumsum(axis=0)
            return (midpoints, integral)
    
    def unaryRepr(self,evalFunction):
        #gives the string repr of each evalFunction
        
        reprDict = {np.sin:"sin",np.cos:"cos",
                    np.tan:"tan",np.arcsin:"arcsin",
                    np.arccos:"arccos",np.arctan:"arctan",
                    np.log10:"log",np.log:"ln"}
        
        return reprDict[evalFunction]
        
    def __repr__(self):
        #generates the string representation of a function
        unaryFunctions = [np.sin,np.cos,np.tan,np.arcsin,
                          np.arccos,np.arctan,np.log10,np.log]
        binaryFunctions = ["^","+","-","*","/"]
        
        #uses recursion to traverse function tree and get string repr
        if(self.evalFunction == "x"):
            #base case
            return self.evalFunction
        elif(type(self.evalFunction) == list):
            return str(self.evalFunction[0])
        elif(self.evalFunction == 0):
            return self.arg1.__repr__()
        elif((self.evalFunction in unaryFunctions) == True):
            return (self.unaryRepr(self.evalFunction) +
                    "(" + self.arg1.__repr__() + ")")
        elif((self.evalFunction in binaryFunctions) == True):
            return ("(" + self.arg1.__repr__() + str(self.evalFunction) +
                    self.arg2.__repr__() + ")")
        elif(self.arg1 == None):
            return "arg"
    
    @classmethod
    def getUnaryFunctionDerivatives(cls):
        #creates dictionary of all unary function derivative rules
        return {np.sin: FunctionNode.sinDerivative,
                                    np.cos: FunctionNode.cosDerivative,
                                    np.tan: FunctionNode.tanDerivative,
                                    np.arcsin: FunctionNode.aSinDerivative,
                                    np.arccos: FunctionNode.aCosDerivative,
                                    np.arctan: FunctionNode.aTanDerivative,
                                    np.log10: FunctionNode.logDerivative,
                                    np.log: FunctionNode.lnDerivative}
    
    @classmethod
    def getBinaryFunctionDerivatives(cls):
        #creates dictionary of all binary function derivative rules
        return {"^": FunctionNode.powerDerivative,
                           "+": FunctionNode.addDerivative,
                           "-": FunctionNode.subtractDerivative,
                           "*": FunctionNode.multiplyDerivative,
                           "/": FunctionNode.divideDerivative}
    
    def symbolicDerivative(self, parent):
        #generates the symbolic derivative of a function
        unaryFunctionDerivatives = FunctionNode.getUnaryFunctionDerivatives()
        binaryFunctionDerivatives = FunctionNode.getBinaryFunctionDerivatives()
        
        #uses recursion 
        if(self.evalFunction == "x"):
            #first base case: if x
            return FunctionNode([1], parent)
        
        elif(type(self.evalFunction) == list):
            #second base case: if constant
            return FunctionNode([0], parent)
        
        elif(((self.evalFunction in unaryFunctionDerivatives.keys()) == True)
            and (self.arg1 != None)):
            #calls appropriate derivative rule, which has recursive call
            return unaryFunctionDerivatives[self.evalFunction](self.arg1,
                                                               parent)
        
        elif(((self.evalFunction in binaryFunctionDerivatives.keys()) == True)
            and (self.arg1 != None) and (self.arg2 != None)):
            #calls appropriate derivative rule for binary functions
            return binaryFunctionDerivatives[self.evalFunction](self.arg1,
                                                                self.arg2,
                                                                parent)
    
    @classmethod
    def areConstants(cls, arg1, arg2):
        #checks if the two arguments are constants
        if(arg1 != None and arg2 != None and (type(arg1.evalFunction) == list) and (type(arg2.evalFunction) == list)):
            return True
        else:
            return False
        
    @classmethod
    def powerTrim(cls, node, parent):
        #rules for trimming power function
        child1 = node.arg1.evalFunction
        child2 = node.arg2.evalFunction
        #arg^0
        if((child1 != [0]) and (child2 == [0])):
            return FunctionNode([1], parent)
        #0^arg
        elif((child1 == [0]) and (child2 != [0])):
            return FunctionNode([0], parent)
        #arg^1
        elif((child1 != [0]) and (child2 == [1])):
            return node.arg1
        #1^arg
        elif((child1 == [1]) and (child2 != [0])):
            return FunctionNode([1], parent)
        else:
            return node
        
    @classmethod
    def addTrim(cls, node, parent):
        #rules for trimming add function
        child1 = node.arg1.evalFunction
        child2 = node.arg2.evalFunction
        #0 + arg2
        if(child1 == [0]):
            return node.arg2
        #arg1 + 0
        elif(child2 == [0]):
            return node.arg1
        else:
            return node
    
    @classmethod
    def subtractTrim(cls, node, parent):
        #rules for trimming subtract function
        child1 = node.arg1.evalFunction
        child2 = node.arg2.evalFunction
        #arg1 - 0
        if(child2 == [0]):
            return node.arg1
        #0 - arg2
        elif(child1 == [0]):
            returnNode = FunctionNode("*", parent)
            returnNode.arg1 = FunctionNode([-1], returnNode)
            returnNode.arg2 = node.arg2
            return returnNode
        else:
            return node
            
    @classmethod
    def multiplyTrim(cls, node, parent):
        #rules for trimming multiply function
        child1 = node.arg1.evalFunction
        child2 = node.arg2.evalFunction
        # 0*arg
        if((child1 == [0]) or (child2 == [0])):
            return FunctionNode([0], parent)
        #1*arg
        elif(child1 == [1]):
            return node.arg2
        #arg*1
        elif(child2 == [1]):
            return node.arg1
        else:
            return node
        
    @classmethod
    def divideTrim(cls, node, parent):
        #rules for trimming divide function
        child2 = node.arg2.evalFunction
        #arg/1
        if(child2 == [1]):
            return node.arg1
        #arg/arg
        elif(node.arg1 == node.arg2):
            return FunctionNode([1], parent)
        else:
            return node
    
    @classmethod
    def getBinaryFunctions(cls):
        #creates dictionary of binary function evaluations
        return {"^": lambda x,y: x**y,
                           "+": lambda x,y: x+y,
                           "-": lambda x,y: x-y,
                           "*": lambda x,y: x*y,
                           "/": lambda x,y: x/y}
    
    @classmethod
    def getBinaryTrimFunctions(cls):
        #creates dictionary of trim functions mapped to binary operations
        return {"^": FunctionNode.powerTrim,
                           "+": FunctionNode.addTrim,
                           "-": FunctionNode.subtractTrim,
                           "*": FunctionNode.multiplyTrim,
                           "/": FunctionNode.divideTrim}
    
    def binaryTrim(self, parent, returnNode, binaryTrimFunctions, binaryFunctions):
        #trims a binary function
        
        #recursive calls
        trimmedNode1 = self.arg1.trim(parent)
        trimmedNode2 = self.arg2.trim(parent)
        if(FunctionNode.areConstants(trimmedNode1,trimmedNode2) == True):
            #evaluates the expressionif both children are constants
            arg1Constant = trimmedNode1.evalFunction[0]
            arg2Constant = trimmedNode2.evalFunction[0]
            try:
                evaluatedValue = [binaryFunctions[self.evalFunction](arg1Constant, arg2Constant)]
                return FunctionNode(evaluatedValue, parent)
            except ZeroDivisionError:
                #catches zero division
                print "Division by zero encountered."
        returnNode.arg1 = trimmedNode1
        returnNode.arg2 = trimmedNode2
        #calls appropriate trim function
        returnNode = binaryTrimFunctions[returnNode.evalFunction](returnNode, parent)
        return returnNode
        
    def trim(self, parent):
        #removes superfluous nodes from the function tree
        unaryFunctions = [np.sin,np.cos,np.tan,np.arcsin,
                                    np.arccos,np.arctan,np.log10,np.log]
        
        #dictionary of the binary operations
        binaryFunctions = FunctionNode.getBinaryFunctions()
        binaryTrimFunctions = FunctionNode.getBinaryTrimFunctions()
        
        returnNode = FunctionNode(self.evalFunction, parent)
        
        #uses recursion to call the appropriate trim function on each node
        #of the tree
        if(self.evalFunction == "x"):
            #a base case
            return FunctionNode(self.evalFunction, parent)
        
        elif(type(self.evalFunction) == list):
            #another base case
            return FunctionNode(self.evalFunction, parent)
        
        elif((self.evalFunction in unaryFunctions) == True):
            #recursive call
            trimmedNode = self.arg1.trim(parent)
            returnNode.arg1 = trimmedNode
            return returnNode
        
        elif((self.evalFunction in binaryFunctions.keys()) == True):
            return self.binaryTrim(parent,returnNode,binaryTrimFunctions, binaryFunctions)
        
    @classmethod
    def sinDerivative(cls, argument, parent):
        #defines rule for differentiating sine
        multiplicationNode = FunctionNode("*",parent)
        cosUNode = FunctionNode(np.cos, multiplicationNode)
        cosUNode.arg1 = argument
        uPrimeNode = argument.symbolicDerivative(multiplicationNode)
        multiplicationNode.arg1 = cosUNode
        multiplicationNode.arg2 = uPrimeNode
        return multiplicationNode
    
    @classmethod
    def cosDerivative(cls, argument, parent):
        #defines rule for differentiating cosine
        multiplicationNode = FunctionNode("*",parent)
        negativeOneNode = FunctionNode([-1],multiplicationNode)
        subMultiplicationNode = FunctionNode("*",multiplicationNode)
        multiplicationNode.arg1 = negativeOneNode
        multiplicationNode.arg2 = subMultiplicationNode
        sinUNode = FunctionNode(np.sin, subMultiplicationNode)
        sinUNode.arg1 = argument
        uPrimeNode = argument.symbolicDerivative(subMultiplicationNode)
        subMultiplicationNode.arg1 = sinUNode
        subMultiplicationNode.arg2 = uPrimeNode
        return multiplicationNode
    
    @classmethod
    def tanDerivative(cls, argument, parent):
        #defines rule for differentiating tangent
        multiplicationNode = FunctionNode("*",parent)
        powerNode = FunctionNode("^",multiplicationNode)
        twoNode = FunctionNode([2],powerNode)
        divideNode = FunctionNode("/",powerNode)
        oneNode = FunctionNode([1], divideNode)
        cosUNode = FunctionNode(np.cos, divideNode)
        cosUNode.arg1 = argument
        divideNode.arg1 = oneNode
        divideNode.arg2 = cosUNode
        powerNode.arg1 = divideNode
        powerNode.arg2 = twoNode
        uPrimeNode = argument.symbolicDerivative(multiplicationNode)
        multiplicationNode.arg1 = powerNode
        multiplicationNode.arg2 = uPrimeNode
        return multiplicationNode
    
    @classmethod
    def aSinDerivative(cls, argument, parent):
        #defines rule for differentiating arcsine
        multiplicationNode = FunctionNode("*", parent)
        uPrimeNode = argument.symbolicDerivative(multiplicationNode)
        uPrimeNode.arg1 = argument
        divideNode = FunctionNode("/", multiplicationNode)
        oneNode = FunctionNode([1],divideNode)
        powerNode = FunctionNode("^", divideNode)
        minusNode = FunctionNode("-", powerNode)
        oneNode2 = FunctionNode([1],divideNode)
        powerNode2 = FunctionNode("^", divideNode)
        twoNode = FunctionNode([2],powerNode2)
        powerNode2.arg1 = argument
        powerNode2.arg2 = twoNode
        minusNode.arg1 = oneNode2
        minusNode.arg2 = powerNode2
        halfNode = FunctionNode([0.5], powerNode)
        powerNode.arg1 = minusNode
        powerNode.arg2 = halfNode
        divideNode.arg1 = oneNode
        divideNode.arg2 = powerNode
        multiplicationNode.arg1 = divideNode
        multiplicationNode.arg2 = uPrimeNode
        return multiplicationNode
    
    @classmethod
    def aCosDerivative(cls, argument, parent):
        #defines rule for differentiating arccosine
        multiplicationNode = FunctionNode("*", parent)
        negOneNode = FunctionNode([-1],multiplicationNode)
        subMultiplicationNode = FunctionNode("*", multiplicationNode)
        uPrimeNode = argument.symbolicDerivative(subMultiplicationNode)
        uPrimeNode.arg1 = argument
        divideNode = FunctionNode("/", subMultiplicationNode)
        oneNode = FunctionNode([1],divideNode)
        powerNode = FunctionNode("^", divideNode)
        minusNode = FunctionNode("-", powerNode)
        oneNode2 = FunctionNode([1],divideNode)
        powerNode2 = FunctionNode("^", divideNode)
        twoNode = FunctionNode([2],powerNode2)
        powerNode2.arg1 = argument
        powerNode2.arg2 = twoNode
        minusNode.arg1 = oneNode2
        minusNode.arg2 = powerNode2
        halfNode = FunctionNode([0.5], powerNode)
        powerNode.arg1 = minusNode
        powerNode.arg2 = halfNode
        divideNode.arg1 = oneNode
        divideNode.arg2 = powerNode
        subMultiplicationNode.arg1 = divideNode
        subMultiplicationNode.arg2 = uPrimeNode
        multiplicationNode.arg1 = negOneNode
        multiplicationNode.arg2 = subMultiplicationNode
        return multiplicationNode
        
    @classmethod
    def aTanDerivative(cls, argument, parent):
        #defines rule for differentiating arctangent
        multiplicationNode = FunctionNode("*", parent)
        divideNode = FunctionNode("/", multiplicationNode)
        oneNode = FunctionNode([1], divideNode)
        addNode = FunctionNode("+", divideNode)
        oneNode = FunctionNode([1], addNode)
        powerNode = FunctionNode("^", addNode)
        twoNode = FunctionNode([2], powerNode)
        powerNode.arg1 = argument
        powerNode.arg2 = twoNode
        addNode.arg1 = oneNode
        addNode.arg2 = powerNode
        uPrimeNode = argument.symbolicDerivative(multiplicationNode)
        uPrimeNode.arg1 = argument
        divideNode.arg1 = oneNode
        divideNode.arg2 = addNode
        multiplicationNode.arg1 = divideNode
        multiplicationNode.arg2 = uPrimeNode
        return multiplicationNode
    
    @classmethod
    def logDerivative(cls, argument, parent):
        #defines rule for differentiating base ten log
        multiplicationNode = FunctionNode("*", parent)
        divideNode = FunctionNode("/",multiplicationNode)
        oneNode = FunctionNode([1],divideNode)
        multiplicationNode2 = FunctionNode("*", divideNode)
        logNode = FunctionNode(np.log10, multiplicationNode2)
        tenNode = FunctionNode([10], logNode)
        logNode.arg1 = tenNode
        multiplicationNode2.arg1 = argument
        multiplicationNode2.arg2 = logNode
        divideNode.arg1 = oneNode
        divideNode.arg2 = multiplicationNode2
        uPrimeNode = argument.symbolicDerivative(multiplicationNode)
        uPrimeNode.arg1 = argument
        uPrimeNode = argument.symbolicDerivative(multiplicationNode)
        multiplicationNode.arg1 = divideNode
        multiplicationNode.arg2 = uPrimeNode
        return multiplicationNode
    
    @classmethod
    def lnDerivative(cls, argument, parent):
        #defines rule for differentiating natural log
        multiplicationNode = FunctionNode("*",parent)
        uPrimeNode = argument.symbolicDerivative(multiplicationNode)
        divideNode = FunctionNode("/",multiplicationNode)
        oneNode = FunctionNode([1], divideNode)
        divideNode.arg1 = oneNode
        divideNode.arg2 = argument
        multiplicationNode.arg1 = divideNode
        multiplicationNode.arg2 = uPrimeNode
        return multiplicationNode
    
    @classmethod
    def polynomialDerivative(cls, arg1, arg2, parent):
        #defines rule for differentiating polynomials
        multiplicationNode = FunctionNode("*", parent)
        multiplicationNode2 = FunctionNode("*", multiplicationNode)
        powerNode = FunctionNode("^", multiplicationNode2)
        aNode = arg1
        b = arg2.evalFunction[0]
        bMinusOne = [b-1]
        bMinusOneNode = FunctionNode(bMinusOne, powerNode)
        powerNode.arg1 = aNode
        powerNode.arg2 = bMinusOneNode
        aPrimeNode = arg1.symbolicDerivative(multiplicationNode2)
        multiplicationNode2.arg1 = powerNode
        multiplicationNode2.arg2 = aPrimeNode
        bNode = arg2
        multiplicationNode.arg1 = bNode
        multiplicationNode.arg2 = multiplicationNode2
        return multiplicationNode
    
    @classmethod
    def exponentialDerivative(cls, arg1, arg2, parent):
        #defines rule for differentiating exponenetials
        multiplicationNode = FunctionNode("*", parent)
        powerNode = FunctionNode("^", multiplicationNode)
        aNode = arg1
        bNode = arg2
        powerNode.arg1 = aNode
        powerNode.arg2 = bNode
        multiplicationNode2 = FunctionNode("*", multiplicationNode)
        lnNode = FunctionNode(np.log, multiplicationNode2)
        lnNode.arg1 = arg1
        bPrimeNode = arg2.symbolicDerivative(multiplicationNode2)
        multiplicationNode2.arg1 = lnNode
        multiplicationNode2.arg2 = bPrimeNode
        multiplicationNode.arg1 = powerNode
        multiplicationNode.arg2 = multiplicationNode2
        return multiplicationNode
    
    @classmethod
    def functionRaisedToFunctionDerivative(cls, arg1, arg2, parent):
        #defines rule for differentiating a function raised to a function
        multiplicationNode = FunctionNode("*", parent)
        powerNode = FunctionNode("^", multiplicationNode)
        powerNode.arg1 = arg1
        powerNode.arg2 = arg2
        addNode = FunctionNode("+", multiplicationNode)
        multiplicationNode2 = FunctionNode("*", addNode)
        bPrimeNode = arg2.symbolicDerivative(multiplicationNode2)
        lnNode = FunctionNode(np.log, multiplicationNode2)
        lnNode.arg1 = arg1
        multiplicationNode2.arg1 = bPrimeNode
        multiplicationNode2.arg2 = lnNode
        divideNode = FunctionNode("/",addNode)
        multiplicationNode3 = FunctionNode("*", divideNode)
        aPrimeNode = arg1.symbolicDerivative(multiplicationNode3)
        multiplicationNode3.arg1 = arg2
        multiplicationNode3.arg2 = aPrimeNode
        divideNode.arg1 = multiplicationNode3
        divideNode.arg2 = arg1
        addNode.arg1 = multiplicationNode2
        addNode.arg2 = divideNode
        multiplicationNode.arg1 = powerNode
        multiplicationNode.arg2 = addNode
        return multiplicationNode
    
    @classmethod
    def isConstant(cls,argument):
        #checks if a child node is a constant
        if(type(argument.evalFunction) == list):
            return True
        else:
            return False
        
    @classmethod
    def powerDerivative(cls, arg1, arg2, parent):
        #defines rule for differentiating powers
        if((FunctionNode.isConstant(arg1) == False) and (FunctionNode.isConstant(arg2) == True)):
            return FunctionNode.polynomialDerivative(arg1,arg2,parent)
        elif((FunctionNode.isConstant(arg1) == True) and (FunctionNode.isConstant(arg2) == False)):
            return FunctionNode.exponentialDerivative(arg1,arg2,parent)
        else:
            return FunctionNode.functionRaisedToFunctionDerivative(arg1,arg2,parent)

    @classmethod
    def addDerivative(cls, arg1, arg2, parent):
        #defines rule for differentiating addition
        addNode = FunctionNode("+", parent)
        aPrimeNode = arg1.symbolicDerivative(addNode)
        bPrimeNode = arg2.symbolicDerivative(addNode)
        addNode.arg1 = aPrimeNode
        addNode.arg2 = bPrimeNode
        return addNode
        
    @classmethod
    def subtractDerivative(cls, arg1, arg2, parent):
        #defines rule for differentiating subtraction
        subtractNode = FunctionNode("+", parent)
        aPrimeNode = arg1.symbolicDerivative(subtractNode)
        bPrimeNode = arg2.symbolicDerivative(subtractNode)
        subtractNode.arg1 = aPrimeNode
        subtractNode.arg2 = bPrimeNode
        return subtractNode
    
    @classmethod
    def multiplyDerivative(cls, arg1, arg2, parent):
        #defines rule for differentiating multiplication
        addNode = FunctionNode("+", parent)
        multNode1 = FunctionNode("*", addNode)
        aPrimeNode = arg1.symbolicDerivative(addNode)
        multNode1.arg1 = aPrimeNode
        multNode1.arg2 = arg2
        multNode2 = FunctionNode("*", addNode)
        bPrimeNode = arg2.symbolicDerivative(addNode)
        multNode2.arg1 = arg1
        multNode2.arg2 = arg2.symbolicDerivative(addNode)
        addNode.arg1 = multNode1
        addNode.arg2 = multNode2
        return addNode
    
    @classmethod
    def divideDerivative(cls, arg1, arg2, parent):
        #defines rule for differentiating division
        divideNode = FunctionNode("/", parent)
        powerNode = FunctionNode("^", divideNode)
        twoNode = FunctionNode([2], powerNode)
        powerNode.arg1 = arg2
        powerNode.arg2 = twoNode
        subtractNode = FunctionNode("+", divideNode)
        multNode1 = FunctionNode("*", subtractNode)
        aPrimeNode = arg1.symbolicDerivative(subtractNode)
        multNode1.arg1 = aPrimeNode
        multNode1.arg2 = arg2
        multNode2 = FunctionNode("*", subtractNode)
        bPrimeNode = arg2.symbolicDerivative(subtractNode)
        multNode2.arg1 = arg1
        multNode2.arg2 = arg2.symbolicDerivative(subtractNode)
        subtractNode.arg1 = multNode1
        subtractNode.arg2 = multNode2
        divideNode.arg1 = subtractNode
        divideNode.arg2 = powerNode
        return divideNode
    
