import re
str = "    //1"

print("//" in str or str == "")
def onlyBracket(line):
    """Checks to see if the line only contains a bracket"""
    for x in line:
        if(x != "{" and x != "}" and x != " "):
            print(x)
            return False
    return True

print(10 + -    10)