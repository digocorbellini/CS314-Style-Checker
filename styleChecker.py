import re
from typing import final

lines = []
problematicLines = {}

#stage checks
haveReachedFirstMethod = False
inClass = False
bracketInLine = True
inMethod = False
bracketStack = []
isComment = False
linesInMethod = 0
operators = "*+-/%"
operatorSpacing = 0

def resetParams():
    global haveReachedFirstMethod
    global inClass
    global bracketInLine
    global inMethod
    global bracketStack
    global isComment
    global linesInMethod
    global operatorSpacing
    global problematicLines
    global lines

    haveReachedFirstMethod = False
    inClass = False
    bracketInLine = True
    inMethod = False
    bracketStack = []
    isComment = False
    linesInMethod = 0
    operatorSpacing = 0
    problematicLines = {}
    lines = []


def instanceVariableProblem(line, index):
    """checks to see if instance variables are not instantiated outside of
    constructor"""
    #if line is not a comment and has an equals then it 
    #has been instantiated outside of constructor
    if("//" not in line and "*" not in line and "=" in line):
        problematicLines[index] = ("Do not instantiate instance variables " +
            "outside of constructor")

def onlyBracket(line):
    """Checks to see if the line only contains a bracket"""
    for x in line:
        if(x != "{" and x != "}" and x != " "):
            return False
    return True

def isLine(line):
    if("//" in line or line == "" or isComment):
        return False
    return True

def isMethod(line, index):
    """Checks to see if the line is the start of a method"""
    if(("public" in line or "private" in line) and "class" not in line):
        if("{" in line or "{" in lines[index + 1]):
            return True
    return False

def methodCommentCheck(index):
    lineBefore = lines[index - 1]
    if ("//" not in lineBefore and "*/" not in lineBefore):
        problematicLines[index] = ("All methods must be commented")

def checkMethodLength(line, index):
    global linesInMethod
    global inMethod
    if(not onlyBracket(line) and isLine(line)):
        linesInMethod += 1

    if("{" in line):
        bracketStack.append("{")
        #check bracket inconsistency 
        checkOpenBrackets(line,index)
    if("}" in line):
        bracketStack.pop()
    
    if(len(bracketStack) == 0):
        if(linesInMethod > 25):
            problematicLines[index] = ("Methods must not be longer than 25 " +
                "lines.")
        inMethod = False
        linesInMethod = 0

def checkMethodBrackets(line, index):
    nextIndex = index + 1
    if(bracketInLine and "{" in lines[nextIndex] 
        and onlyBracket(lines[nextIndex])):
        problematicLines[nextIndex] = "Inconsistency in brackets."
    if(not bracketInLine and line[len(line) - 1] == "{"):
        problematicLines[index] = "Inconsistency in brackets."

def checkOpenBrackets(line,index):
    if(bracketInLine and onlyBracket(line) or not bracketInLine 
        and not onlyBracket(line)):
        problematicLines[index] = "Inconsistency in brackets."

def checkMagicNumbers(line, index):
    acceptableNums = [0,1,-1,2]
    splitLine = re.split("&|\||\(|\)|<|>|;|\+|\-|\*|\/| ", line)
    for x in splitLine:
        if(x.isnumeric()):
            num = float(x)
            if(num not in acceptableNums):
                if("=" not in line or ("<" in line or ">" in line)):
                    problematicLines[index] = "Magic number."
                elif("final" not in line):
                    problematicLines[index] = "Magic numbers should be constant."
        
def checkOperatorSpacing(line, index):
    lineIndex = 0
    allowedChars = "+-;) "
    numOfOperators = 0
    for x in line:
        currentSpacing = 0
        if(x in operators):      
            charBefore = line[lineIndex - 1]
            charAfter =  " " if (lineIndex == len(line) - 1) else line[lineIndex + 1]
            if(charBefore in allowedChars or x == charAfter):
                currentSpacing += 1
            if(charAfter in allowedChars or x == charBefore or charAfter == "="):
                currentSpacing += 1
            if(currentSpacing != operatorSpacing):
                problematicLines[index] = "Inconsistent operator spacing."
                break
            numOfOperators += 1
        lineIndex += 1

def styleCheck():   
    global inClass
    global haveReachedFirstMethod
    global isComment
    global inMethod
    global operatorSpacing
    global bracketInLine
    #go through all of the lines in the code
    index = 0
    for line in lines:
        #check to see if lines meet 80 character requirement
        if(len(line) > 80):
            problematicLines[index] = "Lines can not exceede 80 characters."

        #Check for start of comment
        if("/*" in line):
            isComment = True


        #If in the class and have not reached first method, check instance variables
        if(inClass and not haveReachedFirstMethod):
            instanceVariableProblem(line, index)

        if(not haveReachedFirstMethod and inClass and isMethod(line,index)):
            haveReachedFirstMethod = True
            if("{" not in line and "{" in lines[index + 1]):
                bracketInLine = False


        if(haveReachedFirstMethod and isLine(line) and not isComment):
            #check for break statements
            if("break" in line):
                problematicLines[index] = "No break statements allowed."

            
            if(inMethod):
                #if in a method, count the number of lines
                checkMethodLength(line, index)
                #Check operator spacing
                if(operatorSpacing == 0):
                    lineIndex = 0
                    for x in line:
                        if(x in operators):
                            nextChar = " " if (lineIndex == len(line) - 1) else line[lineIndex + 1]
                            if(line[lineIndex - 1] == " "):
                                operatorSpacing += 1
                            if(nextChar == " "):
                                operatorSpacing += 1
                            break
                        lineIndex += 1
                else:
                    checkOperatorSpacing(line, index)

            #find the start of a method
            #Check for method comment and consistency with brackets
            if(not inMethod and isMethod(line, index)):
                inMethod = True
                #check method comment
                methodCommentCheck(index)
                #check inconsistency with brackets
                checkMethodBrackets(line, index)  
                #append bracket 
                if("{" in line):
                    bracketStack.append("{")
            
            #check magic numbers
            checkMagicNumbers(line,index)
                        
        #Only start checking lines if the class has been reached
        if("class" in line):
            inClass = True        
        #Check to see if it is the end of a comment
        if("*/" in line):
            isComment = False
            
        index += 1

def writeBasicHTML(file):
    finalString = "{% extends 'base.html' %}\n{% block head %}{% endblock %}"
    finalString += "\n{% block body %}\n"
    finalString += "<h1>Style Errors</h1>\n<p id='styleErrors'>\n"

    keys = problematicLines.keys()
    for key in keys:
        lineNum = int(key) + 1
        finalString += "Line " + str(lineNum) + ": " + problematicLines[key] + "<br>\n"
    finalString += "</p>\n"

    finalString += "<h1>Code</h1>\n<p id='code'>\n"
    keys = list(problematicLines.keys())
    linesIndex = 0
    keysIndex = 0
    for line in lines:
        if(keysIndex < len(keys) and keys[keysIndex] == linesIndex):
            finalString += "<span class='tooltip'>" + str(linesIndex + 1) + " " + line
            finalString += "<span class='tooltiptext'>" + problematicLines[keys[keysIndex]] + "</span></span>"
            finalString += "<br>\n"
            keysIndex += 1
        else:
            finalString += str(linesIndex + 1) + " " + line + "<br>\n"
        linesIndex += 1
    button = ('<form action="/back" method="POST" enctype="multipart/form-data">'
                + '<button>back</button></form>')
    finalString += "</p>\n"
    finalString += button + "\n"
    finalString += "{% endblock %}"

    file.write(finalString)

        

def infoPage():
    global lines
    resetParams()
    #place all lines from the file into an array
    with open('static/uploads/text.txt') as f:
        lines = [line.rstrip() for line in f]
    f.close
    styleCheck()

    HTMLFile = open("templates/result.html", "w")
    writeBasicHTML(HTMLFile)

    ''' finalString = ""
    keys = problematicLines.keys()
    for key in keys:
        lineNum = int(key) + 1
        finalString += "Line " + str(lineNum) + ": " + problematicLines[key] + "<br>"
    button = ('<form action="/back" method="POST" enctype="multipart/form-data">'
                + '<button>back</button></form>')
    return "<p class='error'>" + finalString + "</p>" + button '''


infoPage()
print(problematicLines)





