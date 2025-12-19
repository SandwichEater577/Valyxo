import re
import ast
from typing import Any, Dict, List, Optional, Callable


class ValyxoScriptError(Exception):
    """Custom exception for ValyxoScript runtime errors with helpful feedback."""
    
    def __init__(self, message: str, line: int = -1, suggestion: str = "", context: str = ""):
        self.message = message
        self.line = line
        self.suggestion = suggestion
        self.context = context
    
    def __str__(self) -> str:
        error_str = f"ValyxoScript Error: {self.message}"
        if self.line >= 0:
            error_str += f" [line {self.line}]"
        if self.context:
            error_str += f"\n  Context: {self.context}"
        if self.suggestion:
            error_str += f"\n  Hint: {self.suggestion}"
        return error_str


class ValyxoScriptRuntime:
    """ValyxoScript v0.6.0 language runtime environment.
    
    Provides execution of ValyxoScript programs with safe evaluation,
    variable management, control flow, and function definitions.
    
    Features:
    - Variable assignment with type inference
    - Arithmetic and string operations
    - Control flow (if/else, for, while)
    - Function definitions and calls
    - Safe expression evaluation
    - Comprehensive error reporting
    """
    
    MAX_ITERATIONS = 10000
    
    def __init__(self):
        """Initialize runtime with empty variables and functions."""
        self.vars: Dict[str, Any] = {}
        self.functions: Dict[str, Dict[str, Any]] = {}
        self.block_stack: List[Dict[str, Any]] = []
        self.return_value: Optional[Any] = None
        self.iteration_count: int = 0
        self.line_number: int = 0
        self.file_name: str = "<interactive>"
    
    def safe_eval(self, expr: str) -> Any:
        """Safely evaluate mathematical and variable expressions.
        
        Args:
            expr: Expression to evaluate
        
        Returns:
            Result of evaluation
        
        Raises:
            ValyxoScriptError: If expression contains undefined variables or invalid syntax
        """
        expr = expr.strip()
        
        try:
            tree = ast.parse(expr, mode='eval')
            self._validate_ast(tree.body)
            
            local_vars = {k: v for k, v in self.vars.items() if isinstance(v, (int, float, str, bool, list))}
            result = eval(compile(ast.Expression(body=tree.body), '<string>', 'eval'), {"__builtins__": {}}, local_vars)
            return result
        except SyntaxError as e:
            raise ValyxoScriptError(
                f"Syntax error in expression: {e}",
                line=self.line_number,
                context=expr,
                suggestion="Check parentheses, brackets, and quotes"
            )
        except NameError as e:
            var_name = str(e).split("'")[1] if "'" in str(e) else "unknown"
            raise ValyxoScriptError(
                f"Unknown variable: '{var_name}'",
                line=self.line_number,
                context=expr,
                suggestion=f"Did you mean to set '{var_name}' first? Use: set {var_name} = value"
            )
        except ZeroDivisionError:
            raise ValyxoScriptError(
                "Division by zero",
                line=self.line_number,
                context=expr,
                suggestion="Check your division operation"
            )
        except Exception as e:
            raise ValyxoScriptError(
                f"Expression evaluation error: {e}",
                line=self.line_number,
                context=expr
            )
    
    def _validate_ast(self, node: ast.AST) -> None:
        """Validate AST node for security.
        
        Args:
            node: AST node to validate
        
        Raises:
            ValyxoScriptError: If node contains disallowed operations
        """
        if isinstance(node, ast.Call):
            raise ValyxoScriptError(
                "Function calls not allowed in expressions",
                line=self.line_number,
                suggestion="Use function definition syntax: func name(params) { ... }"
            )
        if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            raise ValyxoScriptError(
                "Imports not allowed in ValyxoScript",
                line=self.line_number,
                suggestion="ValyxoScript has no import system"
            )
        
        for child in ast.walk(node):
            if isinstance(child, (ast.Import, ast.ImportFrom)):
                raise ValyxoScriptError(
                    "Imports not allowed",
                    line=self.line_number
                )
    
    def run_line(self, line: str, line_num: int = 0) -> None:
        """Execute a single line of ValyxoScript.
        
        Args:
            line: Line to execute
            line_num: Line number for error reporting
        
        Raises:
            ValyxoScriptError: If line contains invalid syntax
        """
        self.line_number = line_num
        line = line.strip()
        
        if not line or line.startswith('#'):
            return
        
        if line == '}':
            if self.block_stack:
                self._end_block()
            else:
                raise ValyxoScriptError(
                    "Unexpected closing brace '}'",
                    line=self.line_number,
                    suggestion="Check that all blocks are properly opened"
                )
            return
        
        if line.endswith('{'):
            self._start_block(line)
            return
        
        if self.block_stack:
            self.block_stack[-1]['lines'].append(line)
            return
        
        self._execute_command(line)
    
    def run_program(self, code: str) -> None:
        """Execute a complete ValyxoScript program.
        
        Args:
            code: Program source code
        """
        lines = code.split('\n')
        for line_num, line in enumerate(lines, 1):
            try:
                self.run_line(line, line_num)
            except ValyxoScriptError:
                raise
            except Exception as e:
                raise ValyxoScriptError(
                    str(e),
                    line=line_num,
                    context=line
                )
    
    def _start_block(self, line: str) -> None:
        """Start a control flow block.
        
        Args:
            line: Block header line
        """
        if line.startswith('for '):
            match = re.match(r'for\s+(\w+)\s+in\s+(\d+)\s+to\s+(\d+)\s*{', line)
            if match:
                var_name, start, end = match.groups()
                self.block_stack.append({
                    'type': 'for',
                    'var': var_name,
                    'start': int(start),
                    'end': int(end),
                    'lines': []
                })
        elif line.startswith('while '):
            match = re.match(r'while\s+\[(.*?)\]\s*{', line)
            if match:
                condition = match.group(1)
                self.block_stack.append({
                    'type': 'while',
                    'condition': condition,
                    'lines': []
                })
        elif line.startswith('if '):
            match = re.match(r'if\s+\[(.*?)\]\s+then\s+{', line)
            if match:
                condition = match.group(1)
                self.block_stack.append({
                    'type': 'if',
                    'condition': condition,
                    'lines': [],
                    'else_lines': None
                })
        elif line.startswith('func '):
            match = re.match(r'func\s+(\w+)\((.*?)\)\s*{', line)
            if match:
                func_name, params = match.groups()
                param_list = [p.strip() for p in params.split(',')] if params else []
                self.block_stack.append({
                    'type': 'func',
                    'name': func_name,
                    'params': param_list,
                    'lines': []
                })
        elif line.startswith('else {'):
            if self.block_stack and self.block_stack[-1]['type'] == 'if':
                self.block_stack[-1]['else_lines'] = []
    
    def _end_block(self) -> None:
        """Execute and end a control flow block."""
        block = self.block_stack.pop()
        
        if block['type'] == 'for':
            self._execute_for_loop(block)
        elif block['type'] == 'while':
            self._execute_while_loop(block)
        elif block['type'] == 'if':
            self._execute_if_block(block)
        elif block['type'] == 'func':
            self._register_function(block)
    
    def _execute_for_loop(self, block: Dict[str, Any]) -> None:
        """Execute for loop.
        
        Syntax: for i in 1 to 10 { ... }
        
        Args:
            block: For loop block
        
        Raises:
            ValyxoScriptError: If loop exceeds iteration limit
        """
        var_name = block['var']
        start = block['start']
        end = block['end']
        lines = block['lines']
        
        if start > end:
            raise ValyxoScriptError(
                "Invalid loop range",
                line=self.line_number,
                suggestion=f"Loop start ({start}) cannot be greater than end ({end})"
            )
        
        for i in range(start, end + 1):
            self.iteration_count += 1
            if self.iteration_count > self.MAX_ITERATIONS:
                raise ValyxoScriptError(
                    "Loop iteration limit exceeded - possible infinite loop",
                    line=self.line_number,
                    suggestion=f"Maximum iterations: {self.MAX_ITERATIONS}"
                )
            
            self.vars[var_name] = i
            for line in lines:
                self._execute_command(line)
    
    def _execute_while_loop(self, block: Dict[str, Any]) -> None:
        """Execute while loop.
        
        Syntax: while [condition] { ... }
        
        Args:
            block: While loop block
        
        Raises:
            ValyxoScriptError: If loop exceeds iteration limit
        """
        condition = block['condition']
        lines = block['lines']
        
        while True:
            self.iteration_count += 1
            if self.iteration_count > self.MAX_ITERATIONS:
                raise ValyxoScriptError(
                    "Loop iteration limit exceeded - possible infinite loop",
                    line=self.line_number,
                    suggestion=f"Maximum iterations: {self.MAX_ITERATIONS}. Check condition: while [{condition}]"
                )
            
            try:
                result = self.safe_eval(condition)
                if not result:
                    break
            except ValyxoScriptError:
                break
            
            for line in lines:
                self._execute_command(line)
    
    def _execute_if_block(self, block: Dict[str, Any]) -> None:
        """Execute if block.
        
        Args:
            block: If block
        """
        condition = block['condition']
        lines = block['lines']
        else_lines = block.get('else_lines')
        
        try:
            result = self.safe_eval(condition)
            if result:
                for line in lines:
                    self._execute_command(line)
            elif else_lines is not None:
                for line in else_lines:
                    self._execute_command(line)
        except RuntimeError:
            pass
    
    def _register_function(self, block: Dict[str, Any]) -> None:
        """Register function definition.
        
        Args:
            block: Function definition block
        """
        self.functions[block['name']] = {
            'params': block['params'],
            'lines': block['lines']
        }
    
    def _execute_command(self, line: str) -> None:
        """Execute a single ValyxoScript command.
        
        Args:
            line: Command line to execute
        """
        line = line.strip()
        
        if not line or line.startswith('#'):
            return
        
        if line.startswith('set '):
            self._execute_set(line)
        elif line.startswith('print '):
            self._execute_print(line)
        elif line.startswith('if '):
            self._execute_inline_if(line)
        elif '(' in line and ')' in line:
            self._execute_function_call(line)
        elif line == 'vars':
            self._print_vars()
    
    def _execute_set(self, line: str) -> None:
        """Execute set command for variable assignment.
        
        Supports:
        - set x = 10
        - set name = "text"
        - set result = x + 5
        
        Args:
            line: Set command line
        """
        match = re.match(r'set\s+(\w+)\s*=\s*(.*)', line)
        if not match:
            raise ValyxoScriptError(
                "Invalid set syntax",
                line=self.line_number,
                context=line,
                suggestion="Use: set <variable> = <value>"
            )
        
        var_name, expr = match.groups()
        
        if not var_name.isidentifier():
            raise ValyxoScriptError(
                f"Invalid variable name: '{var_name}'",
                line=self.line_number,
                context=line,
                suggestion="Variable names must start with letter or underscore, contain only alphanumerics"
            )
        
        try:
            value = self.safe_eval(expr.strip())
            self.vars[var_name] = value
        except ValyxoScriptError:
            raise
    
    def _execute_print(self, line: str) -> None:
        """Execute print command with flexible output.
        
        Supports:
        - print x (variable)
        - print "Hello" (string)
        - print x + 5 (expression)
        - print x, y, z (multiple values)
        
        Args:
            line: Print command line
        """
        match = re.match(r'print\s+(.*)', line)
        if not match:
            raise ValyxoScriptError(
                "Invalid print syntax",
                line=self.line_number,
                context=line,
                suggestion="Use: print <value>"
            )
        
        expr = match.group(1).strip()
        
        if not expr:
            return
        
        parts = [p.strip() for p in expr.split(',')]
        outputs = []
        
        for part in parts:
            try:
                result = self.safe_eval(part)
                outputs.append(str(result))
            except ValyxoScriptError:
                if part in self.vars:
                    outputs.append(str(self.vars[part]))
                else:
                    outputs.append(part)
        
        print(' '.join(outputs) if len(outputs) > 1 else outputs[0] if outputs else "")
    
    def _execute_inline_if(self, line: str) -> None:
        """Execute inline if statement.
        
        Args:
            line: Inline if command
        """
        match = re.match(r'if\s+\[(.*?)\]\s+then\s+\[(.*?)\]\s+else\s+\[(.*?)\]', line)
        if match:
            condition, then_cmd, else_cmd = match.groups()
            try:
                result = self.safe_eval(condition)
                if result:
                    self._execute_command(then_cmd)
                else:
                    self._execute_command(else_cmd)
            except RuntimeError:
                pass
    
    def _execute_function_call(self, line: str) -> None:
        """Execute function call.
        
        Args:
            line: Function call line
        """
        match = re.match(r'(\w+)\((.*?)\)', line)
        if match:
            func_name, args_str = match.groups()
            if func_name in self.functions:
                args = [arg.strip() for arg in args_str.split(',')] if args_str else []
                arg_values = []
                for arg in args:
                    try:
                        arg_values.append(self.safe_eval(arg))
                    except RuntimeError:
                        arg_values.append(arg)
                
                func_def = self.functions[func_name]
                saved_vars = self.vars.copy()
                
                for param, value in zip(func_def['params'], arg_values):
                    self.vars[param] = value
                
                for func_line in func_def['lines']:
                    self._execute_command(func_line)
                
                self.vars = saved_vars
    
    def _print_vars(self) -> None:
        """Print all variables."""
        for name, value in self.vars.items():
            print(f"{name} = {value}")
