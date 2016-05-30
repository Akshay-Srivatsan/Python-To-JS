# Python To JS
## Description
Converts Python code into a JavaScript file. Every CPython bytecode instruction is turned into an equivalent line of JavaScript. Since libraries are not converted, they have to be replaced manually (for now, the Python `math` library is replaced with the JavaScript `Math` library).

See [the documentation for the `dis` module](https://docs.python.org/2/library/dis.html) for more information about Python bytecodes.

## Usage
Tested in Python 2.7.
### Input:
```
import PythonToJS

@PythonToJS.toJS
def add(a, b):
    return a + b

with open("hello.js", "w") as f:
    PythonToJS.save(f)
```
### Output:
```
var python = {
    add: function(a, b){
        var stack = [];
        var locals = [a, b];
        var constants = [undefined];
        var globals = [];
        var tmp_function = undefined;
        var tmp_function_args = [];
        var tmp_vars = [];
        stack.push(locals[0]);
        stack.push(locals[1]);
        stack.push(stack.pop() + stack.pop());
        return stack.pop();
    }
}
```
The output is not very efficient, but mirrors the Python bytecode.

## Bugs:
* Very few of the opcodes work:
  * Iterators don't exist yet.
  * Tuples, lists, sets, and maps don't work.
  * Conditionals and loops don't work.
  * Functions and classes can't be built yet.
