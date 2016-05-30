import PythonToJS
import math

@PythonToJS.toJS
def add(a, b):
    return a + b

@PythonToJS.toJS
def return1(x):
    return math.sin(x)**2 + math.cos(x)**2

@PythonToJS.toJS
def main():
    return return1(10)

with open("hello.js", "w") as f:
    PythonToJS.save(f)
