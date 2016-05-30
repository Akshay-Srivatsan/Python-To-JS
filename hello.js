var python = {
add: function(a, b){var stack = [];
var locals = [a, b];
var constants = [undefined];
var globals = [];
var tmp_function = undefined; var tmp_function_args = [];
var tmp_vars = [];
stack.push(locals[0]);
stack.push(locals[1]);
stack.push(stack.pop() + stack.pop());
return stack.pop();
},
return1: function(x){var stack = [];
var locals = [x];
var constants = [undefined, 2];
var globals = ['math', 'sin', 'cos'];
var tmp_function = undefined; var tmp_function_args = [];
var tmp_vars = [];
stack.push(python[globals[0]]);
stack.push(stack.pop()[globals[1]]);
stack.push(locals[0]);
tmp_function_args = [stack.pop()];
tmp_function_args.reverse();
tmp_function = stack.pop();
stack.push(tmp_function(tmp_function_args[0]));

stack.push(constants[1]);
tmp_vars = [stack.pop()]; stack.push(Math.pow(stack.pop(), tmp_vars[0]));
stack.push(python[globals[0]]);
stack.push(stack.pop()[globals[2]]);
stack.push(locals[0]);
tmp_function_args = [stack.pop()];
tmp_function_args.reverse();
tmp_function = stack.pop();
stack.push(tmp_function(tmp_function_args[0]));

stack.push(constants[1]);
tmp_vars = [stack.pop()]; stack.push(Math.pow(stack.pop(), tmp_vars[0]));
stack.push(stack.pop() + stack.pop());
return stack.pop();
},
main: function(){var stack = [];
var locals = [];
var constants = [undefined, 10];
var globals = ['return1'];
var tmp_function = undefined; var tmp_function_args = [];
var tmp_vars = [];
stack.push(python[globals[0]]);
stack.push(constants[1]);
tmp_function_args = [stack.pop()];
tmp_function_args.reverse();
tmp_function = stack.pop();
stack.push(tmp_function(tmp_function_args[0]));

return stack.pop();
}}