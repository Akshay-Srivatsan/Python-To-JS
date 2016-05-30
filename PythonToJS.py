import os
import opcode
definitions = []
namespace = "python"
debug = False

# def set_namespace(new_namespace):
#     namespace = new_namespace

def fake_raise(exception):
    raise exception


def save(f):
    global namespace
    f.write("var {0} = {{".format(namespace))
    for name, args, definition in definitions:
        f.write("\n{0}: function({1}){{".format(name, args))
        f.write(definition)
        f.write("},")
    f.seek(-1, os.SEEK_CUR)
    f.write("}")


def call_function(code, index):
    positional_parameters = code[index+1]
    keyword_parameters = code[index+2]
    if keyword_parameters != 0:
        raise NotImplementedError("Cannot handle keyword arguments to functions.")
    current = ""
    current += "tmp_function_args = [" + ", ".join(["stack.pop()"]*positional_parameters) + "];\n"
    current += "tmp_function_args.reverse();\n"
    current += "tmp_function = stack.pop();\n"
    current += "stack.push(tmp_function(" + ",".join(["tmp_function_args[" + str(positional_parameters - i - 1) + "]" for i in range(0, positional_parameters)]) + "));\n"
    return current



def toJS(function):
    global definitions, namespace, debug
    name_string = function.func_name
    locals_list = function.func_code.co_varnames
    args_list = locals_list[:function.func_code.co_argcount]
    constants_list = function.func_code.co_consts
    globals_list = function.func_code.co_names

    # Creates a stack.
    current = "var stack = [];\n"
    # Sets up local variable access.
    current += "var locals = [" + ", ".join(args_list) + ", undefined"*(len(locals_list) - len(args_list)) + "];\n"
    # Sets up local constant access.
    current += "var constants = [" + ", ".join(map(lambda x: repr(x) if x is not None else "undefined", constants_list)) + "];\n"
    # Sets up global variable access.
    current += "var globals = [" + ", ".join(map(repr, globals_list)) + "];\n"
    # These will be used for calling other functions.
    current += "var tmp_function = undefined; var tmp_function_args = [];\n"
    # Used to rearrange variables from the stack.
    current += "var tmp_vars = [];\n"

    index = 0
    code = map(ord, function.func_code.co_code)
    while index < len(code):
        op = code[index]
        opname = opcode.opname[op]
        # Stores a name-to-operation map, with the operation stored as a lambda that returns the js for the operation
        operations_without_argument = ['ROT_TWO', 'ROT_THREE', 'ROT_FOUR', 'DUP_TOP', 'UNARY_POSITIVE', 'UNARY_NEGATIVE', 'UNARY_NOT', 'UNARY_CONVERT', 'UNARY_INVERT', 'GET_ITER', 'BINARY_POWER', 'BINARY_MULTIPLY', 'BINARY_DIVIDE', 'BINARY_FLOOR_DIVIDE', 'BINARY_TRUE_DIVIDE', 'BINARY_MODULO', 'BINARY_ADD', 'BINARY_SUBTRACT', 'BINARY_SUBSCR', 'BINARY_LSHIFT', 'BINARY_RSHIFT', 'BINARY_AND', 'BINARY_XOR', 'BINARY_OR', 'RETURN_VALUE', 'BINARY_POWER']
        argument = None
        if opname not in operations_without_argument:
            argument = str(code[index + 1] + (code[index + 2] << 8))
        operations = {
            'LOAD_FAST': lambda: "stack.push(locals[" + argument + "]);",
            'LOAD_GLOBAL': lambda: "stack.push(" + namespace + "[globals[" + argument + "]]);",
            'LOAD_CONST': lambda: "stack.push(constants[" + argument + "]);",
            'LOAD_ATTR': lambda: "stack.push(stack.pop()[globals[" + argument + "]]);",
            'CALL_FUNCTION': lambda: call_function(code, index),
            'RETURN_VALUE': lambda: "return stack.pop();",

            'POP_TOP': lambda: "stack.pop();",
            'ROT_TWO': lambda: "tmp_vars = [stack.pop(), stack.pop()]; stack.push(tmp_vars[0]); stack.push(tmp_vars[1]);",
            'ROT_THREE': lambda: "tmp_vars = [stack.pop(), stack.pop(), stack.pop()]; stack.push(tmp_vars[0]); stack.push(tmp_vars[2], tmp_vars[1]);",
            'ROT_FOUR': lambda: "tmp_vars = [stack.pop(), stack.pop(), stack.pop(), stack.pop()]; stack.push(tmp_vars[0]); stack.push(tmp_vars[3]); stack.push(tmp_vars[2]); stack.push(tmp_vars[1]);",

            'DUP_TOP': lambda: "stack.push(stack[stack.length - 1])",

            'UNARY_POSITIVE': lambda: "",
            'UNARY_NEGATIVE': lambda: "stack.push(-1*stack.pop())",
            'UNARY_NOT': lambda: "stack.push(!stack.pop())",
            'UNARY_CONVERT': lambda: "stack.push(String(stack.pop()))",
            'UNARY_INVERT': lambda: "stack.push(~stack.pop())",

            'BINARY_POWER': lambda: "tmp_vars = [stack.pop()]; stack.push(Math.pow(stack.pop(), tmp_vars[0]));",
            'BINARY_MULTIPLY': lambda: "stack.push(stack.pop() * stack.pop())",
            'BINARY_DIVIDE': lambda: "tmp_vars = [stack.pop()]; stack.push(stack.pop()/tmp_vars[0]);",
            'BINARY_FLOOR_DIVIDE': lambda: "tmp_vars = [stack.pop()]; stack.push(Math.floor(stack.pop()/tmp_vars[0]));",
            'BINARY_TRUE_DIVIDE': lambda: "tmp_vars = [stack.pop()]; stack.push(stack.pop()/tmp_vars[0]);",
            'BINARY_MODULO': lambda: "tmp_vars = [stack.pop()]; stack.push(stack.pop() % tmp_vars[0]);",
            'BINARY_ADD': lambda: "stack.push(stack.pop() + stack.pop());",
            'BINARY_SUBTRACT': lambda: "tmp_vars = [stack.pop()]; stack.push(stack.pop() - tmp_vars[0]);",
            'BINARY_SUBSCR': lambda: "tmp_vars = [stack.pop()]; stack.push(stack.pop()[tmp_vars[0]]);",
            'BINARY_LSHIFT': lambda: "tmp_vars = [stack.pop()]; stack.push(stack.pop() << tmp_vars[0]);",
            'BINARY_RSHIFT': lambda: "tmp_vars = [stack.pop()]; stack.push(stack.pop() >> tmp_vars[0]);",
            'BINARY_AND': lambda: "tmp_vars = [stack.pop()]; stack.push(stack.pop() & tmp_vars[0]);",
            'BINARY_XOR': lambda: "tmp_vars = [stack.pop()]; stack.push(stack.pop() ^ tmp_vars[0]);",
            'BINARY_OR': lambda: "tmp_vars = [stack.pop()]; stack.push(stack.pop() | tmp_vars[0]);",

            'GET_ITER': lambda: fake_raise(NotImplementedError("Iterators aren't implemented yet.")),
            'STOP_CODE': lambda: "",
            'NOP': lambda: ""
        }
        current_operation = operations[opname]
        if debug:
            print index, name_string, opname
        current_operation_js = current_operation()
        current += current_operation_js + "\n"
        index += 1 if opname in operations_without_argument else 3
    definitions += [(name_string, ", ".join(args_list), current)]
