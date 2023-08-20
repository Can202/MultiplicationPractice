from os import environ
from sys import platform as _sys_platform
import json

def platform():
    if 'ANDROID_ARGUMENT' in environ:
        return "android"
    elif _sys_platform in ('linux', 'linux2','linux3'):
        return "linux"
    elif _sys_platform in ('win32', 'cygwin'):
        return 'win'
    else:
        return "else"

def getPath():
    if platform()=="android":
        return "/data/data/com.can202.multiplicationpractice/files/app/"
    else:
        return ""
    
def readFile(path):
    with open(path, 'r') as file:
        data = json.load(file)
    return data
def writeFile(path, content):
    with open(path, 'w') as file:
        json.dump(content, file)
    
def getjsondataifexists(var, jsonfile, data):
    if data in jsonfile:
        return jsonfile[data]
    else:
        return var