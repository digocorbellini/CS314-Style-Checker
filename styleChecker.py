import re

#place all lines from the file into an array
with open('text.txt') as f:
    lines = [line.rstrip() for line in f]

problematicLines = {}

#stage checks
haveReachedFirstMethod = False
inClass = False
bracketInLine = True
nameOfClass = ""

def instanceVariableProblem(line, index):
    #if line is not a comment and has an equals then it 
    #has been instantiated outside of constructor
    if("//" not in line and "*" not in line and "=" in line):
        problematicLines[index] = ("Do not instantiate instance variables " +
            "outside of constructor")

def onlyBracket(line, index):
    for x in line:
        if(x != "{" or x != "}"):
            return False
    return True
    
#go through all of the lines in the code
index = 0
for line in  lines:
    if("class" in line):
        inClass = True
        nameOfClass = re.split(" {", line)[2]
    if(not haveReachedFirstMethod):
       instanceVariableProblem(line, index)
    if(nameOfClass != "" and nameOfClass in line or "{" in line):
        haveReachedFirstMethod = True
        if(onlyBracket):
            bracketInLine = False


    if(haveReachedFirstMethod):
        if("private" in line or "public" in line):
            lineBefore = lines[index - 1]
            if("//" not in lineBefore or "*/" not in lineBefore):
                x = 1

    index += 1





