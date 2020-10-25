import re

htmlFile = open("templates/result.html", "w")
finalString = "{% extends 'base.html' %}\n{% block body %}{% endblock %}"
htmlFile.write(finalString)